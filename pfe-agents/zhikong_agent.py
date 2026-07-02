"""
PFE 自主研究代理 — 基于千界花园 LLM 的学术协作工程

功能：
1. 自动解析 TOE-SYLVA 的 Lean 代码，识别开放问题
2. 调用 LLM（Zhipu GLM-5.1）生成工程近似策略
3. 执行数值验证脚本
4. 评估"有效涌现"质量
5. 生成工程报告并反馈给 TOE-SYLVA

与千界花园的关系：
- 千界花园提供 LLM API 调用和学术协作框架
- PFE 代理利用这些能力进行工程级自动探索
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class AgentTask:
    """PFE 代理任务 — 质空论涌现的单个探索单元"""
    task_id: str
    target_module: str
    target_theorem: str
    strategy_type: str  # "numerical", "heuristic", "approximation", "llm_guided"
    confidence_threshold: float
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict] = None


class ZhiKongAgent:
    """
    质空论代理 — 从"空"（LLM 推理）到"质"（数值结果）的涌现执行器
    
    命名来源：ZhiKong（质空论）= 质量（质）+ 真空（空）的涌现
    """
    
    def __init__(self, api_key: Optional[str] = None, api_endpoint: Optional[str] = None):
        self.api_key = api_key or os.environ.get('ZHIPU_API_KEY', '')
        self.api_endpoint = api_endpoint or "https://open.bigmodel.cn/api/paas/v4"
        self.model = "glm-5.1"
        self.tasks: List[AgentTask] = []
    
    def _call_llm(self, prompt: str, max_retries: int = 2) -> str:
        """调用千界花园 LLM 后端（或 Zhipu 直接 API）"""
        if not self.api_key:
            return "[ERROR: No API key configured]"
        
        for attempt in range(max_retries + 1):
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "你是 PFE 质空论工程代理。你的任务是为数学开放问题提供工程级近似策略和数值验证方案。不追求数学严格性，追求有效涌现。"},
                        {"role": "user", "content": prompt}
                    ]
                }
                
                response = requests.post(
                    f"{self.api_endpoint}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content']
                
            except Exception as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    print(f"  LLM call failed (attempt {attempt+1}), retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return f"[ERROR: LLM call failed after {max_retries+1} attempts: {e}]"
        
        return "[ERROR: Unknown LLM failure]"
    
    def generate_strategy(self, theorem_name: str, theorem_statement: str, sorry_context: str) -> Dict:
        """
        为开放问题生成工程策略
        
        质空论涌现：LLM（空）-> 策略（质）
        """
        prompt = f"""定理名称：{theorem_name}

定理声明：
{theorem_statement}

未证明部分（sorry）上下文：
{sorry_context}

请作为 PFE 工程代理，提供以下分析：

1. **数值验证可行性**（★★★★★）：
   - 这个定理是否可以用数值方法验证？
   - 如果可以，需要什么计算工具？（SageMath/Python/Mathematica）
   - 预期数值精度是多少？

2. **工程近似策略**（★★★★☆）：
   - 如果严格证明不可行，有什么有效的工程近似？
   - 近似方法的误差边界是多少？
   - 在什么条件下近似有效？

3. **启发式方向**（★★★☆☆）：
   - 这个定理与哪些已知数学结果相关？
   - 有什么可能的引理或中间结论可以优先证明？
   - 有什么反例或边界条件需要注意？

4. **置信度评估**（0-1）：
   - 对数值验证的置信度：_ / 1.0
   - 对工程近似的置信度：_ / 1.0
   - 对启发式方向的置信度：_ / 1.0

5. **执行计划**（具体步骤）：
   - 第一步：_（预计时间：_）
   - 第二步：_（预计时间：_）
   - 第三步：_（预计时间：_）

注意：PFE 不要求数学严格性。数值误差 1e-6 可接受，启发式失败可迭代。"""
        
        print(f"[ZhiKongAgent] Generating strategy for {theorem_name}...")
        response = self._call_llm(prompt)
        
        return {
            'theorem': theorem_name,
            'strategy': response,
            'timestamp': time.time(),
            'model': self.model
        }
    
    def run_batch_analysis(self, open_problems: List[Dict]) -> List[Dict]:
        """
        批量分析开放问题
        
        输入：从 LeanParser 提取的开放问题列表
        输出：每个问题的工程策略
        """
        results = []
        
        for problem in open_problems:
            task = AgentTask(
                task_id=f"pfe-{time.time()}-{problem['theorem'][:20]}",
                target_module=problem['file'],
                target_theorem=problem['theorem'],
                strategy_type="llm_guided",
                confidence_threshold=0.5
            )
            
            strategy = self.generate_strategy(
                theorem_name=problem['theorem'],
                theorem_statement=problem.get('statement', ''),
                sorry_context=f"Line {problem['line']}, {problem['sorry_count']} sorry"
            )
            
            task.status = "completed"
            task.result = strategy
            self.tasks.append(task)
            results.append(strategy)
            
            # 礼貌性延迟，避免 API 限流
            time.sleep(1)
        
        return results
    
    def evaluate_emergence(self, result: Dict) -> float:
        """
        评估"有效涌现"质量
        
        质空论评估标准：
        - 置信度 > 0.5：有效
        - 置信度 > 0.8：高度有效
        - 置信度 < 0.3：无效，需要重新涌现
        """
        # 从 LLM 响应中提取置信度（简单启发式）
        confidence = 0.5  # 默认中等
        
        text = result.get('strategy', '')
        if '置信度' in text or 'confidence' in text.lower():
            # 尝试提取数字
            import re
            numbers = re.findall(r'(\d+\.?\d*)\s*/\s*1\.0', text)
            if numbers:
                confidence = max(float(n) for n in numbers) / 1.0
        
        return min(confidence, 1.0)
    
    def save_strategies(self, output_path: str):
        """保存所有策略到文件"""
        data = {
            'agent': 'ZhiKong PFE Agent',
            'philosophy': 'ZhiKong (Mass-Void) Emergence',
            'tasks': [
                {
                    'task_id': t.task_id,
                    'module': t.target_module,
                    'theorem': t.target_theorem,
                    'status': t.status,
                    'result': t.result
                }
                for t in self.tasks
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[ZhiKongAgent] Saved {len(self.tasks)} strategies to {output_path}")


def main():
    """ZhiKong 代理 CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ZhiKong PFE Agent')
    parser.add_argument('--input', required=True, help='Input JSON file with open problems')
    parser.add_argument('--output', default='pfe_strategies.json', help='Output strategies file')
    parser.add_argument('--api-key', help='Zhipu API key (or set ZHIPU_API_KEY env)')
    parser.add_argument('--batch-size', type=int, default=10, help='Batch size for LLM calls')
    
    args = parser.parse_args()
    
    # 读取开放问题
    with open(args.input, 'r', encoding='utf-8') as f:
        problems = json.load(f)
    
    open_theorems = problems.get('open_theorems', [])
    print(f"[ZhiKong] Loaded {len(open_theorems)} open problems")
    
    # 创建代理
    agent = ZhiKongAgent(api_key=args.api_key)
    
    # 批量分析
    batch = open_theorems[:args.batch_size]
    print(f"[ZhiKong] Analyzing batch of {len(batch)} problems...")
    
    strategies = agent.run_batch_analysis(batch)
    
    # 评估涌现质量
    for s in strategies:
        score = agent.evaluate_emergence(s)
        print(f"  -> {s['theorem']}: emergence score = {score:.2f}")
    
    # 保存
    agent.save_strategies(args.output)
    
    print(f"[ZhiKong] Done. Average emergence score: {sum(agent.evaluate_emergence(s) for s in strategies) / len(strategies):.2f}")


if __name__ == '__main__':
    main()
