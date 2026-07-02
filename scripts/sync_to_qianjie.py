#!/usr/bin/env python3
"""
sync_to_qianjie.py — 同步 TOE-SYLVA 解析数据到千界花园

功能：
1. 解析 TOE-SYLVA 的 Lean 文件（使用与 sylva-parser.ts 兼容的格式）
2. 生成与千界花园 /api/research/sylva-sync 端点兼容的 JSON 数据
3. 尝试 POST 数据到 http://localhost:3000/api/research/notes
4. 如果千界花园未运行，保存到本地 JSON 文件

调用方式：
  python scripts/sync_to_qianjie.py [--sylva-dir PATH] [--output-dir PATH] [--qianjie-url URL]

PFE ENGINEERING NOTE: 零外部依赖（仅 urllib），追求有效涌现。
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


# ─── 常量 ───
TOE_SYLVA_DEFAULT = r"C:\Users\一梦\Documents\TOE-SYLVA-pull"
QIANJIE_BASE_URL_DEFAULT = "http://localhost:3000"
QIANJIE_NOTES_ENDPOINT = "/api/research/notes"


# ─── Lean 解析器（兼容 sylva-parser.ts） ───

class SylvaParser:
    """
    千界花园 sylva-parser.ts 的 Python 移植。
    解析 theorem/lemma/def/axiom/conjecture/structure/inductive/instance，
    提取 sorry 和策略注释。
    """

    THEOREM_PATTERN = re.compile(
        r'^(theorem|lemma|def|axiom|conjecture|structure|inductive|instance)\s+'
        r'([a-zA-Z_][a-zA-Z0-9_\']*)'
    )
    SORRY_PATTERN = re.compile(r'\bsorry\b')
    ENGINEERING_NOTE = re.compile(r'PFE ENGINEERING NOTE[:\s]*(.*)', re.IGNORECASE)
    STRATEGY = re.compile(r'\[?STRATEGY\]?[:\s]*(.*)', re.IGNORECASE)
    LEMMAS_NEEDED = re.compile(r'LEMMAS NEEDED[:\s]*(.*)', re.IGNORECASE)
    TACTICS_NEEDED = re.compile(r'TACTICS NEEDED[:\s]*(.*)', re.IGNORECASE)
    IMPORT_PATTERN = re.compile(r'^import\s+(.+)')
    NAMESPACE_PATTERN = re.compile(r'^namespace\s+(\S+)')
    TODO_PATTERN = re.compile(r'TODO\(research\)[:\s]*(.*)', re.IGNORECASE)
    MILLENNIUM_PATTERN = re.compile(
        r'Millennium\s*(Prize)?\s*(Problem|Problems)|Clay\s*Mathematics|千年\s*难题',
        re.IGNORECASE
    )

    def __init__(self, lean_dir: str):
        self.lean_dir = Path(lean_dir)
        self.modules: List[Dict[str, Any]] = []

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        file_name = file_path.name

        module = {
            'fileName': file_name,
            'filePath': str(file_path),
            'totalLines': len(lines),
            'theorems': [],
            'definitions': [],
            'sorryCount': 0,
            'todoCount': 0,
            'imports': [],
            'namespace': '',
            'moduleDescription': ''
        }

        # 提取文件描述（顶部注释）
        desc_lines = []
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped.startswith('/-') or stripped.startswith('-') or stripped == '-/':
                if stripped.startswith('-') and not stripped.startswith('/-'):
                    desc_lines.append(stripped.replace('-', '').strip())
            elif stripped == '':
                pass
            else:
                break
            i += 1
        module['moduleDescription'] = ' '.join(desc_lines).strip()

        # 提取 imports 和 namespace
        for line in lines:
            if m := self.IMPORT_PATTERN.match(line.strip()):
                module['imports'].append(m.group(1).strip())
            if m := self.NAMESPACE_PATTERN.match(line.strip()):
                module['namespace'] = m.group(1)

        # 解析定理/定义声明
        current_block = None
        for line_idx, line in enumerate(lines):
            stripped = line.strip()

            m = self.THEOREM_PATTERN.match(stripped)
            if m:
                if current_block:
                    self._finalize_block(current_block, module, lines)
                current_block = {
                    'name': m.group(2),
                    'type': m.group(1),
                    'lineStart': line_idx + 1,
                    'lines': [line],
                    'docLines': []
                }
                continue

            if current_block:
                current_block['lines'].append(line)
                if stripped.startswith('end '):
                    self._finalize_block(current_block, module, lines)
                    current_block = None

        if current_block:
            self._finalize_block(current_block, module, lines)

        # 后处理：精确划分 block 边界和提取 sorry
        finalized_theorems = []
        for t in module['theorems']:
            block_lines = lines[t['lineStart'] - 1:t['lineEnd']]
            # 重新计算精确结束行
            end_line = t['lineEnd']
            for j in range(t['lineStart'] - 1, len(lines)):
                l = lines[j]
                if l.strip() == '':
                    continue
                if not l.startswith(' ') and not l.startswith('\t'):
                    if self.THEOREM_PATTERN.match(l.strip()) or l.strip().startswith('end '):
                        end_line = j + 1
                        break

            actual_block = lines[t['lineStart'] - 1:end_line]
            sorry_lines = []
            proof_strategy = ""
            for k, actual_line in enumerate(actual_block):
                if self.SORRY_PATTERN.search(actual_line):
                    sorry_lines.append(t['lineStart'] + k)
                    # 向前查找注释
                    for m_idx in range(k - 1, max(-1, k - 6), -1):
                        if m_idx < 0:
                            break
                        prev_line = actual_block[m_idx].strip()
                        if prev_line.startswith('--'):
                            proof_strategy = prev_line.replace('--', '').strip() + " " + proof_strategy
                        elif prev_line == '' or prev_line.startswith('·'):
                            continue
                        else:
                            break

            statement = self._extract_statement(actual_block)
            finalized_theorems.append({
                'name': t['name'],
                'type': t['type'],
                'lineStart': t['lineStart'],
                'lineEnd': end_line,
                'statement': statement,
                'proofStrategy': proof_strategy.strip(),
                'hasSorry': len(sorry_lines) > 0,
                'sorryCount': len(sorry_lines),
                'sorryLines': sorry_lines,
                'isMillennium': self.MILLENNIUM_PATTERN.search('\n'.join(actual_block)) is not None,
            })

        module['theorems'] = finalized_theorems
        module['sorryCount'] = sum(t['sorryCount'] for t in module['theorems'])

        # 分离 definitions
        module['definitions'] = [t for t in module['theorems']
                                 if t['type'] in ('def', 'structure', 'inductive', 'instance')]
        module['theorems'] = [t for t in module['theorems']
                              if t['type'] in ('theorem', 'lemma', 'axiom', 'conjecture')]

        # 提取 TODOs
        for i, line in enumerate(lines):
            if m := self.TODO_PATTERN.search(line):
                module['todoCount'] += 1

        return module

    def _finalize_block(self, block: Dict, module: Dict, lines: List[str]) -> None:
        line_end = block['lineStart'] + len(block['lines']) - 1
        content = '\n'.join(block['lines'])
        is_millennium = bool(self.MILLENNIUM_PATTERN.search(content))

        module['theorems'].append({
            'name': block['name'],
            'type': block['type'],
            'lineStart': block['lineStart'],
            'lineEnd': line_end,
            'statement': content[:200],
            'proofStrategy': ' '.join(block['docLines']),
            'hasSorry': bool(self.SORRY_PATTERN.search(content)),
            'sorryCount': len(self.SORRY_PATTERN.findall(content)),
            'sorryLines': [],
            'isMillennium': is_millennium,
        })

    def _extract_statement(self, block_lines: List[str]) -> str:
        full_text = '\n'.join(block_lines)
        for pattern in [r'(:=\s*by\b)', r'(:=\s*\{)', r'(:=\s*)']:
            m = re.search(pattern, full_text)
            if m:
                return full_text[:m.start()].strip()
        return full_text[:300].strip()

    def _should_skip(self, path: Path) -> bool:
        """判断是否应该跳过该路径。"""
        p = str(path)
        skip_patterns = [
            '.lake', 'lake-packages', 'archive', 'sylva_formalization',
            '.git', 'node_modules', '__pycache__', '.pfe-bridge-cache',
        ]
        return any(pat in p for pat in skip_patterns)

    def parse_all(self) -> List[Dict[str, Any]]:
        for lean_file in self.lean_dir.rglob('*.lean'):
            if self._should_skip(lean_file):
                continue
            try:
                module = self.parse_file(lean_file)
                self.modules.append(module)
            except Exception as e:
                print(f"[Warning] Failed to parse {lean_file}: {e}")
        return self.modules

    def to_sylva_sync_format(self) -> Dict[str, Any]:
        """生成与千界花园 sylva-sync 兼容的数据格式。"""
        total_theorems = sum(len(m['theorems']) for m in self.modules)
        total_definitions = sum(len(m['definitions']) for m in self.modules)
        total_sorry = sum(m['sorryCount'] for m in self.modules)
        total_axiom = sum(
            len([t for t in m['theorems'] if t['type'] == 'axiom'])
            for m in self.modules
        )

        millennium_problems = []
        todo_items = []
        for m in self.modules:
            for t in m['theorems']:
                if t['isMillennium'] or t['type'] == 'axiom':
                    millennium_problems.append({
                        'name': t['name'],
                        'filePath': m['filePath'],
                        'line': t['lineStart'],
                        'type': 'axiom' if t['type'] == 'axiom' else 'conjecture' if t['type'] == 'conjecture' else 'theorem'
                    })

        return {
            'modules': self.modules,
            'totalTheorems': total_theorems,
            'totalDefinitions': total_definitions,
            'totalSorry': total_sorry,
            'totalAxiom': total_axiom,
            'millenniumProblems': millennium_problems,
            'todoItems': todo_items,
        }


# ─── 千界花园 API 客户端 ───

class QianJieClient:
    """千界花园 HTTP API 客户端（零外部依赖，仅 urllib）。"""

    def __init__(self, base_url: str = QIANJIE_BASE_URL_DEFAULT):
        self.base_url = base_url
        self.timeout = 30

    def health_check(self) -> bool:
        """检查千界花园是否可连接。"""
        try:
            req = urllib.request.Request(
                f"{self.base_url}{QIANJIE_NOTES_ENDPOINT}",
                method="GET",
                headers={"Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get('success', False)
        except Exception:
            return False

    def post_notes(self, notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量创建 ResearchNote。"""
        results = []
        for note in notes:
            try:
                data = json.dumps(note).encode('utf-8')
                req = urllib.request.Request(
                    f"{self.base_url}{QIANJIE_NOTES_ENDPOINT}",
                    data=data,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    result = json.loads(resp.read().decode('utf-8'))
                    results.append(result)
            except Exception as e:
                results.append({"success": False, "error": str(e), "title": note.get('title')})
        return {"notes_created": len([r for r in results if r.get('success')]), "results": results}


# ─── 数据转换 ───

def generate_module_sync_data(module: Dict[str, Any]) -> Dict[str, Any]:
    """生成 ResearchModule 同步数据（兼容 sylva-parser.ts 的 generateModuleSyncData）。"""
    fp = module['filePath']
    discipline = (
        "algebraic_geometry" if "Hodge" in fp
        else "pde" if "Navier" in fp
        else "computational_complexity" if "Complexity" in fp
        else "number_theory" if "Riemann" in fp
        else "quantum_field_theory" if "Yang" in fp
        else "mathematics"
    )
    return {
        'name': module['fileName'].replace('.lean', ''),
        'displayName': module['fileName'],
        'category': 'Millennium_Problem',
        'subcategory': module['namespace'] or 'sylva',
        'discipline': discipline,
        'lineCount': module['totalLines'],
        'sorryCount': module['sorryCount'],
        'theoremCount': len(module['theorems']),
        'definitionCount': len(module['definitions']),
        'filePath': module['filePath'],
        'dependencies': json.dumps(module['imports']),
    }


def generate_theorem_sync_data(theorem: Dict[str, Any], module_id: str = "") -> Dict[str, Any]:
    """生成 ResearchTheorem 同步数据。"""
    status = (
        "axiom" if theorem['type'] == 'axiom'
        else "research" if theorem['hasSorry']
        else "proven"
    )
    return {
        'name': theorem['name'],
        'statement': theorem['statement'],
        'moduleId': module_id,
        'status': status,
        'proofStrategy': theorem['proofStrategy'],
        'leanCode': f"{theorem['name']} ({theorem['type']}): {theorem['statement']}",
    }


def generate_task_for_sorry(theorem: Dict[str, Any], module_name: str) -> Dict[str, Any]:
    """生成 AcademicTask 同步数据（用于 sorry 跟踪）。"""
    priority = "critical" if theorem['isMillennium'] else "high" if theorem['sorryCount'] > 3 else "normal"
    return {
        'title': f"证明 {theorem['name']} ({theorem['sorryCount']} 个 sorry)",
        'description': (
            f"模块 {module_name} 中的定理 {theorem['name']} 需要完成 {theorem['sorryCount']} 个 sorry 的证明。"
            + (f" 已知策略: {theorem['proofStrategy']}" if theorem['proofStrategy'] else "")
            + (" [Millennium Problem]" if theorem['isMillennium'] else "")
        ),
        'type': "verify" if theorem['type'] == 'axiom' else "prove",
        'status': "pending",
        'priority': priority,
        'targetModule': module_name,
        'targetPaper': theorem['name'],
    }


# ─── 主流程 ───

def main():
    parser = argparse.ArgumentParser(description='Sync TOE-SYLVA data to QianJie (Blooming Garden)')
    parser.add_argument('--sylva-dir', default=TOE_SYLVA_DEFAULT, help='TOE-SYLVA directory')
    parser.add_argument('--output-dir', default='config', help='Output directory for local JSON fallback')
    parser.add_argument('--qianjie-url', default=QIANJIE_BASE_URL_DEFAULT, help='QianJie base URL')
    parser.add_argument('--skip-api', action='store_true', help='Skip API calls, save to local only')
    args = parser.parse_args()

    sylva_dir = Path(args.sylva_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not sylva_dir.exists():
        print(f"[ERROR] TOE-SYLVA directory not found: {sylva_dir}")
        sys.exit(1)

    # 1. 解析 Lean 文件
    print(f"[Phase 1] Parsing Lean files from {sylva_dir}...")
    sylva_parser = SylvaParser(sylva_dir)
    sylva_parser.parse_all()
    sync_data = sylva_parser.to_sylva_sync_format()
    print(f"  -> Modules: {len(sync_data['modules'])}")
    print(f"  -> Theorems: {sync_data['totalTheorems']}")
    print(f"  -> Definitions: {sync_data['totalDefinitions']}")
    print(f"  -> Sorry: {sync_data['totalSorry']}")
    print(f"  -> Axioms: {sync_data['totalAxiom']}")
    print(f"  -> Millennium Problems: {len(sync_data['millenniumProblems'])}")

    # 2. 生成 Notes 数据
    print("[Phase 2] Generating ResearchNote data...")
    notes = []
    for module in sync_data['modules']:
        # 模块统计 note
        notes.append({
            'title': f"SYLVA模块: {module['fileName']}",
            'content': json.dumps({
                'filePath': module['filePath'],
                'totalLines': module['totalLines'],
                'theoremCount': len(module['theorems']),
                'definitionCount': len(module['definitions']),
                'sorryCount': module['sorryCount'],
                'namespace': module['namespace'],
                'imports': module['imports'],
            }, ensure_ascii=False, indent=2),
            'tags': ['sylva-sync', 'module', module['fileName'].replace('.lean', '')],
        })

        # 每个 sorry 的 note
        for theorem in module['theorems']:
            if theorem['hasSorry']:
                notes.append({
                    'title': f"策略: {theorem['name']}",
                    'content': (
                        f"文件: {module['filePath']}\n"
                        f"行号: {theorem['lineStart']}\n"
                        f"类型: {theorem['type']}\n"
                        f"sorry 数量: {theorem['sorryCount']}\n"
                        f"策略: {theorem['proofStrategy']}\n"
                        f"声明: {theorem['statement'][:200]}"
                    ),
                    'tags': ['sorry', 'proof-strategy', theorem['type'], module['fileName'].replace('.lean', '')],
                })

    print(f"  -> Generated {len(notes)} notes")

    # 3. 尝试 POST 到千界花园
    if not args.skip_api:
        client = QianJieClient(args.qianjie_url)
        print(f"[Phase 3] Connecting to QianJie at {args.qianjie_url}...")
        if client.health_check():
            print("  -> QianJie is available, posting notes...")
            result = client.post_notes(notes)
            created = result.get('notes_created', 0)
            print(f"  -> Created {created}/{len(notes)} notes")
            if created > 0:
                print("[Done] Sync complete.")
                return
            else:
                print("  -> All POSTs failed, falling back to local JSON.")
        else:
            print("  -> QianJie is not available (localhost:3000 not reachable).")
            print("  -> Falling back to local JSON.")
    else:
        print("[Phase 3] --skip-api set, saving to local JSON only.")

    # 4. 保存到本地 JSON
    print("[Phase 4] Saving to local JSON files...")

    # 保存完整同步数据
    sync_path = output_dir / f"sylva_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(sync_path, 'w', encoding='utf-8') as f:
        json.dump(sync_data, f, ensure_ascii=False, indent=2)
    print(f"  -> Sync data: {sync_path}")

    # 保存 notes 数据
    notes_path = output_dir / f"sylva_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(notes_path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    print(f"  -> Notes data: {notes_path}")

    # 保存模块统计
    stats = {
        'timestamp': datetime.now().isoformat(),
        'modules': [{
            'name': m['fileName'],
            'theorems': len(m['theorems']),
            'definitions': len(m['definitions']),
            'sorry': m['sorryCount'],
            'filePath': m['filePath'],
        } for m in sync_data['modules']]
    }
    stats_path = output_dir / f"sylva_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"  -> Stats data: {stats_path}")

    print("\n[Done] Sync data saved locally. Run QianJie at localhost:3000 to import.")
    print(f"  To import: POST {notes_path} to {args.qianjie_url}/api/research/notes")


if __name__ == '__main__':
    main()
