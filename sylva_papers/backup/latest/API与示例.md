# Agent集群写稿系统 - API接口与使用示例

## 1. 命令行接口 (CLI)

### 1.1 主要命令

```bash
# Agent集群写稿系统命令行工具
# 版本: 1.0.0

# ============================================
# 工作流管理命令
# ============================================

# 创建并启动新工作流
aws workflow create \
  --topic "量子计算中的纠错码理论" \
  --requirements requirements.json \
  --config config.yaml \
  --output ./outputs/paper_001

# 查看工作流状态
aws workflow status --workflow-id wf_abc123

# 列出所有工作流
aws workflow list --status running --limit 10

# 暂停工作流
aws workflow pause --workflow-id wf_abc123

# 恢复工作流
aws workflow resume --workflow-id wf_abc123

# 取消工作流
aws workflow cancel --workflow-id wf_abc123 --reason "需求变更"

# 查看工作流详细报告
aws workflow report --workflow-id wf_abc123 --format markdown

# ============================================
# Agent管理命令
# ============================================

# 查看Agent状态
aws agent list
aws agent status --agent-id writer_0

# 手动调度Agent执行任务
aws agent dispatch \
  --agent-role writer \
  --task task.json \
  --timeout 1800

# 重启Agent
aws agent restart --agent-id writer_0

# 查看Agent日志
aws agent logs --agent-id writer_0 --tail 100

# ============================================
# 论文生成命令
# ============================================

# 快速生成论文（简化流程）
aws paper generate \
  --topic "深度学习在图像分类中的应用" \
  --style research_article \
  --target-journal "IEEE Transactions" \
  --word-count 5000 \
  --output ./my_paper.md

# 多版本写作（一文多写）
aws paper multi-write \
  --topic "对抗样本的防御机制" \
  --versions 5 \
  --styles theoretical,algorithmic,applied,historical,innovative \
  --output-dir ./multi_versions/

# 模拟审稿流程
aws paper review \
  --draft my_draft.md \
  --reviewers 3 \
  --journal-style nature \
  --output review_report.json

# 根据审稿意见修改
aws paper revise \
  --draft my_draft.md \
  --comments review_comments.json \
  --output revised_draft.md

# 完整学术生产流程
aws paper full-pipeline \
  --topic "基于Transformer的机器翻译优化" \
  --from-draft draft_v1.md \
  --target-phase published \
  --config full_config.yaml

# ============================================
# 系统管理命令
# ============================================

# 启动系统服务
aws server start --port 8000 --workers 4

# 停止系统服务
aws server stop

# 查看系统状态
aws system status

# 查看系统指标
aws system metrics --format prometheus

# 备份数据
aws system backup --destination /backup/aws_$(date +%Y%m%d).tar.gz

# 恢复数据
aws system restore --source /backup/aws_20260101.tar.gz

# 清理旧数据
aws system cleanup --keep-days 30

# ============================================
# 配置管理命令
# ============================================

# 验证配置文件
aws config validate --config my_config.yaml

# 生成默认配置
aws config init --output config.yaml

# 查看当前配置
aws config show

# 更新配置项
aws config set agents.writers.count 10
```

### 1.2 CLI实现代码示例

```python
#!/usr/bin/env python3
"""
Agent集群写稿系统 - CLI入口
"""

import click
import asyncio
import json
from typing import Optional
from pathlib import Path

from aws.core import WorkflowEngine, Coordinator
from aws.config import load_config

@click.group()
@click.option('--config', '-c', default='config.yaml', help='配置文件路径')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
@click.pass_context
def cli(ctx, config, verbose):
    """Agent集群写稿系统命令行工具"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config)
    ctx.obj['verbose'] = verbose

@cli.group()
def workflow():
    """工作流管理命令"""
    pass

@workflow.command()
@click.option('--topic', '-t', required=True, help='论文主题')
@click.option('--requirements', '-r', type=click.Path(exists=True), help='需求文件路径')
@click.option('--output', '-o', default='./outputs', help='输出目录')
@click.option('--dry-run', is_flag=True, help='干运行（不实际执行）')
@click.pass_context
def create(ctx, topic, requirements, output, dry_run):
    """创建并启动新工作流"""
    config = ctx.obj['config']
    
    # 加载需求
    reqs = {}
    if requirements:
        with open(requirements) as f:
            reqs = json.load(f)
    
    if dry_run:
        click.echo(f"[干运行] 将创建工作流: topic={topic}")
        click.echo(f"需求: {json.dumps(reqs, indent=2, ensure_ascii=False)}")
        return
    
    # 异步执行
    async def _create():
        coordinator = await Coordinator.get_instance()
        await coordinator.initialize(config)
        
        engine = WorkflowEngine(coordinator, config)
        
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        
        click.echo(f"🚀 启动工作流: {workflow_id}")
        click.echo(f"📄 主题: {topic}")
        
        result = await engine.execute_workflow(workflow_id, topic, reqs)
        
        click.echo(f"✅ 工作流完成: {result['status']}")
        click.echo(f"📁 输出目录: {output}")
        
        # 保存结果
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        with open(output_path / f"{workflow_id}_result.json", 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        if result['status'] == 'completed':
            final_draft = result.get('final_draft', {})
            content = final_draft.get('content', '')
            
            with open(output_path / f"{workflow_id}_final.md", 'w') as f:
                f.write(content)
            
            click.echo(f"📝 最终论文已保存: {output_path / f'{workflow_id}_final.md'}")
    
    asyncio.run(_create())

@workflow.command()
@click.option('--workflow-id', '-w', required=True, help='工作流ID')
@click.pass_context
def status(ctx, workflow_id):
    """查看工作流状态"""
    async def _status():
        coordinator = await Coordinator.get_instance()
        state = coordinator.workflows.get(workflow_id)
        
        if not state:
            click.echo(f"❌ 工作流 {workflow_id} 不存在")
            return
        
        click.echo(f"工作流: {workflow_id}")
        click.echo(f"状态: {state.status.value}")
        click.echo(f"当前阶段: {state.current_phase.value}")
        click.echo(f"创建时间: {state.created_at}")
        
        # 显示进度
        stats = state.to_summary_dict()
        click.echo(f"\n进度统计:")
        click.echo(f"  - 完成阶段数: {len(stats['phases_completed'])}")
        click.echo(f"  - 草稿版本数: {stats['draft_count']}")
        click.echo(f"  - 修改轮数: {stats['revision_count']}")
    
    asyncio.run(_status())

@cli.group()
def paper():
    """论文生成命令"""
    pass

@paper.command()
@click.option('--topic', '-t', required=True, help='论文主题')
@click.option('--versions', '-n', default=5, help='生成版本数量')
@click.option('--styles', '-s', default='balanced', help='写作风格（逗号分隔）')
@click.option('--output-dir', '-o', default='./multi_versions', help='输出目录')
@click.pass_context
def multi_write(ctx, topic, versions, styles, output_dir):
    """多版本并行写作（一文多写）"""
    config = ctx.obj['config']
    style_list = styles.split(',')
    
    async def _multi_write():
        coordinator = await Coordinator.get_instance()
        await coordinator.initialize(config)
        
        click.echo(f"📝 启动多版本写作: {versions} 个版本")
        click.echo(f"🎨 写作风格: {', '.join(style_list)}")
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 并行调度写作任务
        tasks = []
        for i in range(versions):
            style = style_list[i % len(style_list)]
            task = {
                "task_id": f"write_{i}",
                "topic": topic,
                "writing_style": style,
                "requirements": {"word_count": 5000}
            }
            
            click.echo(f"  → 调度写作任务 {i+1}/{versions} (风格: {style})")
            tasks.append(coordinator.dispatch_task("writer", task))
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 保存结果
        successful = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                click.echo(f"  ❌ 版本 {i+1} 失败: {result}")
            else:
                successful += 1
                draft = result.get('draft', {})
                content = draft.get('content', '')
                
                filename = f"version_{i+1}_{style}.md"
                with open(output_path / filename, 'w') as f:
                    f.write(content)
                
                click.echo(f"  ✅ 版本 {i+1} 完成: {filename}")
        
        click.echo(f"\n📊 统计: {successful}/{versions} 个版本成功生成")
        click.echo(f"📁 输出目录: {output_dir}")
    
    asyncio.run(_multi_write())

if __name__ == '__main__':
    cli()
```

---

## 2. Python SDK接口

### 2.1 核心SDK类

```python
"""
Agent集群写稿系统 - Python SDK
"""

from typing import Dict, List, Optional, Callable, AsyncIterator
from dataclasses import dataclass
import asyncio

@dataclass
class PaperRequirements:
    """论文需求配置"""
    topic: str
    word_count: int = 5000
    style: str = "research_article"
    target_journal: Optional[str] = None
    domain: str = "computer_science"
    sections: Optional[List[str]] = None
    references_required: int = 20
    figures_required: int = 3

@dataclass
class WorkflowOptions:
    """工作流选项"""
    writer_count: int = 5
    reviewer_count: int = 3
    max_iterations: int = 3
    enable_expert_review: bool = True
    enable_deep_editing: bool = True
    auto_advance: bool = True
    timeout_seconds: int = 7200

class AgentWritingSystem:
    """
    Agent集群写稿系统主类
    
    使用示例:
        aws = AgentWritingSystem(config_path="config.yaml")
        await aws.initialize()
        
        result = await aws.generate_paper(
            requirements=PaperRequirements(
                topic="量子计算纠错码",
                word_count=6000,
                style="theoretical_paper"
            )
        )
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = load_config(config_path)
        self.coordinator: Optional[Coordinator] = None
        self.engine: Optional[WorkflowEngine] = None
        self._initialized = False
    
    async def initialize(self):
        """初始化系统"""
        if self._initialized:
            return
        
        self.coordinator = await Coordinator.get_instance()
        await self.coordinator.initialize(self.config)
        
        self.engine = WorkflowEngine(self.coordinator, self.config)
        
        self._initialized = True
    
    async def generate_paper(
        self,
        requirements: PaperRequirements,
        options: Optional[WorkflowOptions] = None,
        progress_callback: Optional[Callable[[str, Dict], None]] = None
    ) -> Dict:
        """
        生成论文（完整流程）
        
        Args:
            requirements: 论文需求
            options: 工作流选项
            progress_callback: 进度回调函数(phase, progress_info)
            
        Returns:
            包含最终论文和工作流历史的字典
        """
        if not self._initialized:
            await self.initialize()
        
        options = options or WorkflowOptions()
        
        # 更新配置
        workflow_config = self.config.copy()
        workflow_config["agents"]["writers"]["count"] = options.writer_count
        workflow_config["agents"]["reviewers"]["count"] = options.reviewer_count
        workflow_config["workflow"]["max_iterations"] = options.max_iterations
        
        # 生成工作流ID
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        
        # 构建需求字典
        req_dict = {
            "topic": requirements.topic,
            "word_count": requirements.word_count,
            "style": requirements.style,
            "target_journal": requirements.target_journal,
            "domain": requirements.domain,
            "sections": requirements.sections,
            "references_required": requirements.references_required,
            "figures_required": requirements.figures_required
        }
        
        # 注册进度回调
        if progress_callback:
            self.coordinator.subscribe_to_event("phase_change", progress_callback)
        
        # 执行工作流
        result = await self.engine.execute_workflow(
            workflow_id=workflow_id,
            topic=requirements.topic,
            requirements=req_dict
        )
        
        return result
    
    async def multi_write(
        self,
        topic: str,
        versions: int = 5,
        styles: Optional[List[str]] = None,
        requirements: Optional[Dict] = None
    ) -> List[ArticleDraft]:
        """
        多版本并行写作
        
        Args:
            topic: 论文主题
            versions: 版本数量
            styles: 写作风格列表
            requirements: 额外需求
            
        Returns:
            多个草稿版本列表
        """
        if not self._initialized:
            await self.initialize()
        
        styles = styles or ["balanced", "theoretical", "applied", "historical", "innovative"]
        requirements = requirements or {}
        
        # 创建并行写作任务
        tasks = []
        for i in range(versions):
            style = styles[i % len(styles)]
            task = {
                "task_id": f"multi_write_{i}",
                "topic": topic,
                "writing_style": style,
                "requirements": requirements
            }
            tasks.append(self.coordinator.dispatch_task("writer", task))
        
        # 并行执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 提取有效草稿
        drafts = []
        for result in results:
            if not isinstance(result, Exception):
                draft = result.get('draft')
                if draft:
                    drafts.append(ArticleDraft(**draft))
        
        return drafts
    
    async def review_draft(
        self,
        draft: ArticleDraft,
        reviewer_count: int = 3,
        review_style: str = "mixed"
    ) -> List[ReviewReport]:
        """
        审稿流程
        
        Args:
            draft: 待审稿的草稿
            reviewer_count: 审稿人数量
            review_style: 审稿风格
            
        Returns:
            审稿报告列表
        """
        if not self._initialized:
            await self.initialize()
        
        # 创建审稿任务
        review_tasks = []
        for i in range(reviewer_count):
            task = {
                "manuscript": draft.to_dict(),
                "reviewer_style": f"reviewer_{i}",
                "review_type": "peer"
            }
            review_tasks.append(self.coordinator.dispatch_task("reviewer", task))
        
        # 并行审稿
        results = await asyncio.gather(*review_tasks, return_exceptions=True)
        
        reports = []
        for result in results:
            if not isinstance(result, Exception):
                report = ReviewReport(**result.get('report', {}))
                reports.append(report)
        
        return reports
    
    async def revise_draft(
        self,
        draft: ArticleDraft,
        comments: List[ReviewComment],
        revision_type: str = "major"
    ) -> ArticleDraft:
        """
        根据评论修改草稿
        
        Args:
            draft: 原草稿
            comments: 审稿评论列表
            revision_type: 修改类型（minor/major）
            
        Returns:
            修改后的草稿
        """
        if not self._initialized:
            await self.initialize()
        
        task = {
            "original_draft": draft.to_dict(),
            "comments": [c.to_dict() for c in comments],
            "revision_type": revision_type
        }
        
        result = await self.coordinator.dispatch_task("writer", task)
        
        revised = ArticleDraft(**result.get('revised_draft', {}))
        revised.version = draft.version + 1
        revised.parent_draft_id = draft.draft_id
        
        return revised
    
    async def stream_generate(
        self,
        requirements: PaperRequirements,
        options: Optional[WorkflowOptions] = None
    ) -> AsyncIterator[Dict]:
        """
        流式生成论文（实时返回进度）
        
        Yields:
            阶段进度更新
        """
        if not self._initialized:
            await self.initialize()
        
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        
        # 创建工作流
        workflow_state = WorkflowState(
            workflow_id=workflow_id,
            topic=requirements.topic,
            config=self.config,
            data_store={"requirements": requirements.__dict__}
        )
        
        await self.coordinator.register_workflow(workflow_state)
        
        # 执行并流式返回进度
        async for update in self._execute_with_streaming(workflow_state):
            yield update
    
    async def _execute_with_streaming(
        self,
        state: WorkflowState
    ) -> AsyncIterator[Dict]:
        """内部流式执行"""
        # 简化的流式执行实现
        phases = [
            WorkflowPhase.MULTI_WRITING,
            WorkflowPhase.DRAFT_SELECTION,
            WorkflowPhase.DEEP_EDITING,
            WorkflowPhase.EXPERT_REVIEW,
            WorkflowPhase.PEER_REVIEW,
            WorkflowPhase.FINAL_DECISION
        ]
        
        for phase in phases:
            yield {
                "phase": phase.value,
                "status": "started",
                "progress": 0,
                "message": f"进入阶段: {phase.value}"
            }
            
            # 模拟阶段执行
            await asyncio.sleep(0.1)
            
            yield {
                "phase": phase.value,
                "status": "completed",
                "progress": 100,
                "message": f"阶段完成: {phase.value}"
            }
        
        yield {
            "phase": "completed",
            "status": "success",
            "final_draft": state.get_data("current_draft", {})
        }
    
    def get_workflow_history(self, workflow_id: str) -> Optional[WorkflowState]:
        """获取工作流历史"""
        if self.coordinator:
            return self.coordinator.workflows.get(workflow_id)
        return None
    
    async def shutdown(self):
        """关闭系统"""
        if self.coordinator:
            await self.coordinator.shutdown()
        self._initialized = False

# 便捷的顶层函数
async def quick_generate(
    topic: str,
    word_count: int = 5000,
    config_path: str = "config.yaml"
) -> str:
    """
    快速生成论文（简化接口）
    
    Args:
        topic: 论文主题
        word_count: 字数要求
        config_path: 配置文件路径
        
    Returns:
        论文内容字符串
    """
    aws = AgentWritingSystem(config_path)
    
    result = await aws.generate_paper(
        requirements=PaperRequirements(
            topic=topic,
            word_count=word_count
        ),
        options=WorkflowOptions(
            writer_count=3,
            reviewer_count=2,
            max_iterations=2
        )
    )
    
    final_draft = result.get('final_draft', {})
    return final_draft.get('content', '')

async def compare_versions(
    topic: str,
    styles: List[str],
    config_path: str = "config.yaml"
) -> Dict[str, str]:
    """
    比较不同写作风格的版本
    
    Args:
        topic: 论文主题
        styles: 要比较的风格列表
        config_path: 配置文件路径
        
    Returns:
        风格->内容的字典
    """
    aws = AgentWritingSystem(config_path)
    await aws.initialize()
    
    drafts = await aws.multi_write(
        topic=topic,
        versions=len(styles),
        styles=styles
    )
    
    return {
        draft.writing_style: draft.content
        for draft in drafts
    }
```

### 2.2 异步上下文管理器

```python
class AWSContext:
    """
    Agent写作系统异步上下文管理器
    
    使用示例:
        async with AWSContext("config.yaml") as aws:
            result = await aws.generate_paper(requirements)
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        self.aws = AgentWritingSystem(config_path)
    
    async def __aenter__(self):
        await self.aws.initialize()
        return self.aws
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aws.shutdown()
        return False

# 使用示例
async def main():
    async with AWSContext() as aws:
        # 生成论文
        result = await aws.generate_paper(
            requirements=PaperRequirements(
                topic="基于深度学习的医学图像分割",
                word_count=6000,
                style="research_article",
                target_journal="IEEE TMI"
            ),
            progress_callback=lambda phase, info: print(f"[{phase}] {info}")
        )
        
        print(f"论文生成完成！")
        print(f"最终质量评分: {result.get('final_draft', {}).get('quality_score', 0)}")
```

---

## 3. RESTful API

### 3.1 API端点设计

```yaml
# OpenAPI 3.0 规范
openapi: 3.0.0
info:
  title: Agent集群写稿系统 API
  version: 1.0.0
  description: 基于多Agent协作的学术论文自动生成系统

servers:
  - url: http://localhost:8000/api/v1
    description: 本地开发服务器

paths:
  # 工作流管理
  /workflows:
    post:
      summary: 创建新工作流
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkflowCreateRequest'
      responses:
        201:
          description: 工作流创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkflowResponse'
    
    get:
      summary: 列出所有工作流
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, running, completed, failed]
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        200:
          description: 工作流列表
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkflowSummary'

  /workflows/{workflow_id}:
    get:
      summary: 获取工作流详情
      parameters:
        - name: workflow_id
          in: path
          required: true
          schema:
            type: string
      responses:
        200:
          description: 工作流详情
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkflowDetail'
        404:
          description: 工作流不存在

  /workflows/{workflow_id}/status:
    get:
      summary: 获取工作流状态
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkflowStatus'

  /workflows/{workflow_id}/control:
    post:
      summary: 控制工作流（暂停/恢复/取消）
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                action:
                  type: string
                  enum: [pause, resume, cancel]
      responses:
        200:
          description: 操作成功

  /workflows/{workflow_id}/result:
    get:
      summary: 获取工作流结果
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkflowResult'

  # Agent管理
  /agents:
    get:
      summary: 列出所有Agent
      responses:
        200:
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AgentInfo'

  /agents/{agent_id}/status:
    get:
      summary: 获取Agent状态
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentStatus'

  # 论文生成
  /papers/generate:
    post:
      summary: 生成论文（完整流程）
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaperGenerateRequest'
      responses:
        202:
          description: 任务已接受
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AsyncTaskResponse'

  /papers/multi-write:
    post:
      summary: 多版本并行写作
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MultiWriteRequest'
      responses:
        202:
          description: 任务已接受

  /papers/{paper_id}/review:
    post:
      summary: 提交论文审稿
      responses:
        202:
          description: 审稿任务已启动

  /papers/{paper_id}/revise:
    post:
      summary: 根据审稿意见修改
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RevisionRequest'
      responses:
        200:
          description: 修改完成

  # 系统状态
  /health:
    get:
      summary: 健康检查
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: healthy

  /metrics:
    get:
      summary: 系统指标（Prometheus格式）
      responses:
        200:
          content:
            text/plain:
              schema:
                type: string

components:
  schemas:
    WorkflowCreateRequest:
      type: object
      required:
        - topic
      properties:
        topic:
          type: string
          description: 论文主题
        requirements:
          type: object
          properties:
            word_count:
              type: integer
              default: 5000
            style:
              type: string
              enum: [research_article, theoretical_paper, survey]
            target_journal:
              type: string
        options:
          type: object
          properties:
            writer_count:
              type: integer
              default: 5
            reviewer_count:
              type: integer
              default: 3

    WorkflowResponse:
      type: object
      properties:
        workflow_id:
          type: string
        status:
          type: string
        created_at:
          type: string
          format: date-time

    WorkflowSummary:
      type: object
      properties:
        workflow_id:
          type: string
        topic:
          type: string
        status:
          type: string
        current_phase:
          type: string
        progress_percent:
          type: integer

    WorkflowDetail:
      type: object
      properties:
        workflow_id:
          type: string
        status:
          type: string
        current_phase:
          type: string
        phases_completed:
          type: array
          items:
            type: string
        drafts:
          type: array
          items:
            $ref: '#/components/schemas/DraftInfo'
        review_reports:
          type: array
          items:
            $ref: '#/components/schemas/ReviewReportInfo'

    WorkflowStatus:
      type: object
      properties:
        workflow_id:
          type: string
        status:
          type: string
        current_phase:
          type: string
        progress:
          type: object
          properties:
            current:
              type: integer
            total:
              type: integer
        estimated_completion:
          type: string
          format: date-time

    WorkflowResult:
      type: object
      properties:
        workflow_id:
          type: string
        status:
          type: string
        final_draft:
          $ref: '#/components/schemas/DraftDetail'
        all_drafts:
          type: array
          items:
            $ref: '#/components/schemas/DraftInfo'
        statistics:
          type: object

    DraftInfo:
      type: object
      properties:
        draft_id:
          type: string
        version:
          type: integer
        writing_style:
          type: string
        quality_score:
          type: number
        word_count:
          type: integer

    DraftDetail:
      type: object
      properties:
        draft_id:
          type: string
        title:
          type: string
        content:
          type: string
        sections:
          type: array
          items:
            type: object
        quality_assessment:
          type: object

    ReviewReportInfo:
      type: object
      properties:
        report_id:
          type: string
        reviewer_style:
          type: string
        verdict:
          type: string
          enum: [accept, minor_revision, major_revision, reject]
        overall_score:
          type: number

    AgentInfo:
      type: object
      properties:
        agent_id:
          type: string
        role:
          type: string
        status:
          type: string
        current_task:
          type: string
          nullable: true
        capabilities:
          type: array
          items:
            type: string

    AgentStatus:
      type: object
      properties:
        agent_id:
          type: string
        status:
          type: string
        health_metrics:
          type: object
          properties:
            cpu_usage:
              type: number
            memory_usage:
              type: number
            tasks_completed:
              type: integer

    PaperGenerateRequest:
      type: object
      required:
        - topic
      properties:
        topic:
          type: string
        requirements:
          $ref: '#/components/schemas/PaperRequirements'
        options:
          $ref: '#/components/schemas/WorkflowOptions'

    PaperRequirements:
      type: object
      properties:
        word_count:
          type: integer
        style:
          type: string
        target_journal:
          type: string
        domain:
          type: string
        sections:
          type: array
          items:
            type: string

    WorkflowOptions:
      type: object
      properties:
        writer_count:
          type: integer
        reviewer_count:
          type: integer
        max_iterations:
          type: integer
        timeout_seconds:
          type: integer

    MultiWriteRequest:
      type: object
      required:
        - topic
      properties:
        topic:
          type: string
        versions:
          type: integer
          default: 5
        styles:
          type: array
          items:
            type: string
        requirements:
          type: object

    RevisionRequest:
      type: object
      required:
        - draft_id
        - comments
      properties:
        draft_id:
          type: string
        comments:
          type: array
          items:
            type: object
        revision_type:
          type: string
          enum: [minor, major]

    AsyncTaskResponse:
      type: object
      properties:
        task_id:
          type: string
        status:
          type: string
        message:
          type: string
        websocket_url:
          type: string
```

### 3.2 FastAPI实现

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager

# 全局系统实例
aws_system: Optional[AgentWritingSystem] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动
    global aws_system
    aws_system = AgentWritingSystem()
    await aws_system.initialize()
    yield
    # 关闭
    await aws_system.shutdown()

app = FastAPI(
    title="Agent集群写稿系统",
    version="1.0.0",
    lifespan=lifespan
)

# 工作流管理端点
@app.post("/api/v1/workflows", status_code=201)
async def create_workflow(request: WorkflowCreateRequest):
    """创建新工作流"""
    workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
    
    # 异步启动工作流
    asyncio.create_task(
        aws_system.engine.execute_workflow(
            workflow_id=workflow_id,
            topic=request.topic,
            requirements=request.requirements.dict()
        )
    )
    
    return {
        "workflow_id": workflow_id,
        "status": "created",
        "message": "工作流已创建并开始执行"
    }

@app.get("/api/v1/workflows")
async def list_workflows(
    status: Optional[str] = None,
    limit: int = 10
):
    """列出工作流"""
    workflows = []
    
    for wf_id, state in aws_system.coordinator.workflows.items():
        if status and state.status.value != status:
            continue
        
        workflows.append({
            "workflow_id": wf_id,
            "topic": state.topic,
            "status": state.status.value,
            "current_phase": state.current_phase.value,
            "created_at": state.created_at.isoformat()
        })
    
    return workflows[:limit]

@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """获取工作流详情"""
    state = aws_system.coordinator.workflows.get(workflow_id)
    
    if not state:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    return {
        "workflow_id": workflow_id,
        "status": state.status.value,
        "current_phase": state.current_phase.value,
        "phases_completed": [p.phase.value for p in state.phase_history],
        "drafts": state.get_data("drafts", []),
        "statistics": state.to_summary_dict()
    }

@app.get("/api/v1/workflows/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """获取工作流状态"""
    state = aws_system.coordinator.workflows.get(workflow_id)
    
    if not state:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    # 计算进度
    phase_order = [
        "idle", "multi_writing", "draft_selection", "deep_editing",
        "expert_review", "peer_review", "revision", "final_decision", "published"
    ]
    current_idx = phase_order.index(state.current_phase.value)
    progress = int((current_idx / len(phase_order)) * 100)
    
    return {
        "workflow_id": workflow_id,
        "status": state.status.value,
        "current_phase": state.current_phase.value,
        "progress": {
            "percent": progress,
            "current_phase_index": current_idx,
            "total_phases": len(phase_order)
        }
    }

@app.post("/api/v1/workflows/{workflow_id}/control")
async def control_workflow(workflow_id: str, action: str):
    """控制工作流"""
    state = aws_system.coordinator.workflows.get(workflow_id)
    
    if not state:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    if action == "pause":
        state.status = WorkflowStatus.PAUSED
        return {"message": "工作流已暂停"}
    
    elif action == "resume":
        state.status = WorkflowStatus.RUNNING
        return {"message": "工作流已恢复"}
    
    elif action == "cancel":
        state.status = WorkflowStatus.CANCELLED
        return {"message": "工作流已取消"}
    
    else:
        raise HTTPException(status_code=400, detail=f"未知操作: {action}")

@app.get("/api/v1/workflows/{workflow_id}/result")
async def get_workflow_result(workflow_id: str):
    """获取工作流结果"""
    state = aws_system.coordinator.workflows.get(workflow_id)
    
    if not state:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    if state.status != WorkflowStatus.COMPLETED:
        return {
            "status": "not_ready",
            "message": f"工作流尚未完成，当前状态: {state.status.value}"
        }
    
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "final_draft": state.get_data("final_manuscript") or state.get_data("current_draft"),
        "all_drafts": state.get_data("drafts", []),
        "review_reports": state.get_data("review_reports", []),
        "statistics": state.to_summary_dict()
    }

# Agent管理端点
@app.get("/api/v1/agents")
async def list_agents():
    """列出所有Agent"""
    agents = []
    
    for agent_id, agent in aws_system.coordinator.agents.items():
        agents.append({
            "agent_id": agent_id,
            "role": agent.config.role.value,
            "status": aws_system.coordinator.agent_status.get(agent_id, "unknown").value,
            "capabilities": agent.config.capabilities
        })
    
    return agents

@app.get("/api/v1/agents/{agent_id}/status")
async def get_agent_status(agent_id: str):
    """获取Agent状态"""
    agent = aws_system.coordinator.agents.get(agent_id)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent不存在")
    
    return {
        "agent_id": agent_id,
        "role": agent.config.role.value,
        "status": aws_system.coordinator.agent_status.get(agent_id, "unknown").value,
        "health_metrics": {
            "tasks_completed": agent.get_data("tasks_completed", 0),
            "last_active": agent.get_data("last_active")
        }
    }

# 论文生成端点
@app.post("/api/v1/papers/generate")
async def generate_paper(
    request: PaperGenerateRequest,
    background_tasks: BackgroundTasks
):
    """生成论文（异步）"""
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    
    # 后台执行任务
    background_tasks.add_task(
        _run_paper_generation,
        task_id,
        request
    )
    
    return {
        "task_id": task_id,
        "status": "accepted",
        "message": "论文生成任务已接受，正在后台执行",
        "check_status_url": f"/api/v1/tasks/{task_id}/status",
        "websocket_url": f"/ws/tasks/{task_id}"
    }

async def _run_paper_generation(task_id: str, request: PaperGenerateRequest):
    """后台执行论文生成"""
    try:
        result = await aws_system.generate_paper(
            requirements=request.requirements,
            options=request.options
        )
        
        # 保存结果到缓存/数据库
        _save_task_result(task_id, result)
        
    except Exception as e:
        _save_task_error(task_id, str(e))

@app.post("/api/v1/papers/multi-write")
async def multi_write(request: MultiWriteRequest):
    """多版本并行写作"""
    drafts = await aws_system.multi_write(
        topic=request.topic,
        versions=request.versions,
        styles=request.styles
    )
    
    return {
        "versions_generated": len(drafts),
        "drafts": [
            {
                "draft_id": d.draft_id,
                "writing_style": d.writing_style,
                "quality_score": d.quality_assessment.overall_score if d.quality_assessment else None,
                "word_count": d.word_count
            }
            for d in drafts
        ]
    }

# WebSocket实时进度
@app.websocket("/ws/workflows/{workflow_id}")
async def workflow_websocket(websocket: WebSocket, workflow_id: str):
    """工作流实时进度WebSocket"""
    await websocket.accept()
    
    try:
        while True:
            state = aws_system.coordinator.workflows.get(workflow_id)
            
            if not state:
                await websocket.send_json({"error": "Workflow not found"})
                break
            
            await websocket.send_json({
                "workflow_id": workflow_id,
                "status": state.status.value,
                "current_phase": state.current_phase.value,
                "timestamp": datetime.now().isoformat()
            })
            
            if state.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]:
                break
            
            await asyncio.sleep(1)
            
    except Exception as e:
        await websocket.close()

# 健康检查和指标
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus指标"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return generate_latest()
```

---

## 4. 使用示例

### 4.1 示例1：学术论文全流程

```python
#!/usr/bin/env python3
"""
示例1：完整学术论文生成流程
- 多版本写作
- 自动审稿
- 多轮修改
- 最终输出
"""

import asyncio
from aws import AgentWritingSystem, PaperRequirements, WorkflowOptions

async def full_academic_pipeline():
    """完整学术生产流程示例"""
    
    # 初始化系统
    aws = AgentWritingSystem("config.yaml")
    await aws.initialize()
    
    print("=" * 60)
    print("🚀 启动学术论文生成流程")
    print("=" * 60)
    
    # 定义论文需求
    requirements = PaperRequirements(
        topic="基于Transformer的神经机器翻译优化方法研究",
        word_count=6000,
        style="research_article",
        target_journal="ACL Conference",
        domain="computer_science",
        sections=[
            "abstract",
            "introduction",
            "background",
            "methodology",
            "experiments",
            "results",
            "discussion",
            "conclusion",
            "references"
        ],
        references_required=25,
        figures_required=4
    )
    
    # 定义工作流选项
    options = WorkflowOptions(
        writer_count=5,           # 5个写作Agent并行
        reviewer_count=3,         # 3个审稿人
        max_iterations=3,         # 最多3轮修改
        enable_expert_review=True,  # 启用专家评审
        enable_deep_editing=True,   # 启用深度编辑
        auto_advance=True,          # 自动流转
        timeout_seconds=7200      # 2小时超时
    )
    
    # 进度回调
    def on_progress(phase: str, info: dict):
        print(f"[{phase}] {info.get('message', '')}")
    
    # 执行完整流程
    print("\n📋 论文需求:")
    print(f"  主题: {requirements.topic}")
    print(f"  目标期刊: {requirements.target_journal}")
    print(f"  字数要求: {requirements.word_count}")
    
    print(f"\n⚙️  工作流配置:")
    print(f"  写作Agent数量: {options.writer_count}")
    print(f"  审稿人数量: {options.reviewer_count}")
    print(f"  最大修改轮数: {options.max_iterations}")
    
    print("\n⏳ 开始执行...")
    
    result = await aws.generate_paper(
        requirements=requirements,
        options=options,
        progress_callback=on_progress
    )
    
    # 输出结果
    print("\n" + "=" * 60)
    print("✅ 论文生成完成!")
    print("=" * 60)
    
    print(f"\n📊 工作流统计:")
    print(f"  工作流ID: {result['workflow_id']}")
    print(f"  最终状态: {result['status']}")
    print(f"  总耗时: {result.get('completion_time', 0):.1f}秒")
    
    # 显示所有生成的草稿
    all_drafts = result.get('all_drafts', [])
    print(f"\n📝 生成草稿数: {len(all_drafts)}")
    
    for i, draft in enumerate(all_drafts, 1):
        print(f"  版本{i}: {draft.get('writing_style', 'unknown')} - "
              f"质量分{draft.get('quality_score', 0):.1f}")
    
    # 保存最终论文
    final_draft = result.get('final_draft', {})
    if final_draft:
        content = final_draft.get('content', '')
        filename = f"final_paper_{result['workflow_id']}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n💾 最终论文已保存: {filename}")
        print(f"   字数: {final_draft.get('word_count', 0)}")
        print(f"   质量评分: {final_draft.get('quality_score', 0):.1f}")
    
    # 审稿报告摘要
    review_reports = result.get('review_reports', [])
    if review_reports:
        print(f"\n📋 审稿意见摘要:")
        for i, report in enumerate(review_reports, 1):
            verdict = report.get('verdict', 'unknown')
            score = report.get('overall_score', 0)
            print(f"  审稿人{i}: {verdict} (评分: {score:.1f})")
    
    # 关闭系统
    await aws.shutdown()
    
    return result

if __name__ == "__main__":
    asyncio.run(full_academic_pipeline())
```

### 4.2 示例2：多版本对比写作

```python
#!/usr/bin/env python3
"""
示例2：多版本对比写作
- 同一主题，不同风格
- 自动质量评分
- 可视化对比
"""

import asyncio
from aws import AgentWritingSystem

async def compare_writing_styles():
    """对比不同写作风格"""
    
    aws = AgentWritingSystem()
    await aws.initialize()
    
    topic = "深度强化学习在游戏AI中的应用"
    
    # 定义要对比的风格
    styles = [
        "theoretical",   # 理论构建者
        "algorithmic",   # 算法设计师
        "applied",       # 应用导向者
        "historical",    # 历史回顾者
        "innovative"     # 创新突破者
    ]
    
    print(f"🎯 主题: {topic}")
    print(f"🎨 对比风格: {', '.join(styles)}")
    print("\n⏳ 启动多版本写作...")
    
    # 并行生成多个版本
    drafts = await aws.multi_write(
        topic=topic,
        versions=len(styles),
        styles=styles,
        requirements={"word_count": 3000, "include_code": True}
    )
    
    print(f"\n✅ 生成完成! 共 {len(drafts)} 个版本\n")
    
    # 质量评分对比
    print("📊 质量评分对比:")
    print("-" * 60)
    
    for draft in drafts:
        style = draft.writing_style
        quality = draft.quality_assessment
        
        if quality:
            print(f"\n📝 风格: {style}")
            print(f"   总体评分: {quality.overall_score:.1f}/100")
            print(f"   创新性: {quality.dimension_scores.get('novelty', 0):.1f}")
            print(f"   严谨性: {quality.dimension_scores.get('rigor', 0):.1f}")
            print(f"   清晰性: {quality.dimension_scores.get('clarity', 0):.1f}")
            print(f"   字数: {draft.word_count}")
        
        # 保存各版本
        filename = f"version_{style}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(draft.content)
        print(f"   💾 已保存: {filename}")
    
    # 选择最佳版本
    best_draft = max(drafts, 
                     key=lambda d: d.quality_assessment.overall_score 
                     if d.quality_assessment else 0)
    
    print(f"\n🏆 最佳版本: {best_draft.writing_style}")
    print(f"   质量评分: {best_draft.quality_assessment.overall_score:.1f}")
    
    await aws.shutdown()

if __name__ == "__main__":
    asyncio.run(compare_writing_styles())
```

### 4.3 示例3：快速审稿模式

```python
#!/usr/bin/env python3
"""
示例3：快速审稿模式
- 已有草稿，快速获取审稿意见
- 模拟顶级会议审稿流程
"""

import asyncio
import json
from aws import AgentWritingSystem
from aws.data_structures import ArticleDraft

async def quick_review_mode():
    """快速审稿模式"""
    
    aws = AgentWritingSystem()
    await aws.initialize()
    
    # 加载已有草稿（示例：从文件加载）
    draft_content = """
# 基于图神经网络的社交网络分析

## 摘要
本文提出了一种新型的图神经网络架构...

## 1. 引言
社交网络分析是当前研究的热点...

## 2. 方法
我们提出的GNN-Social模型包含三个主要组件...
"""
    
    draft = ArticleDraft(
        draft_id="existing_001",
        version=1,
        title="基于图神经网络的社交网络分析",
        content=draft_content,
        word_count=4500,
        writing_style="research_article"
    )
    
    print("📄 待审稿论文:")
    print(f"   标题: {draft.title}")
    print(f"   字数: {draft.word_count}")
    
    print("\n⏳ 启动审稿流程...")
    print("   模拟: NeurIPS 审稿流程")
    
    # 执行审稿
    review_reports = await aws.review_draft(
        draft=draft,
        reviewer_count=3,
        review_style="neurips"
    )
    
    print(f"\n✅ 审稿完成! 收到 {len(review_reports)} 份审稿报告\n")
    
    # 汇总审稿意见
    print("📋 审稿意见汇总:")
    print("=" * 60)
    
    for i, report in enumerate(review_reports, 1):
        print(f"\n📝 审稿报告 #{i}")
        print(f"   审稿风格: {report.reviewer_style}")
        print(f"   裁决: {report.overall_recommendation}")
        print(f"   置信度: {report.reviewer_confidence}")
        print(f"   总体评分: {report.overall_score:.1f}")
        
        print(f"\n   优点:")
        for strength in report.strengths[:3]:
            print(f"     + {strength}")
        
        print(f"\n   缺点:")
        for weakness in report.weaknesses[:3]:
            print(f"     - {weakness}")
        
        # 详细评论
        if report.detailed_comments:
            print(f"\n   详细评论 ({len(report.detailed_comments)} 条):")
            for comment in report.detailed_comments[:3]:
                print(f"     [{comment.severity}] {comment.category}: {comment.title}")
    
    # 计算共识
    verdicts = [r.overall_recommendation for r in review_reports]
    accept_count = verdicts.count("accept")
    revision_count = verdicts.count("minor_revision") + verdicts.count("major_revision")
    reject_count = verdicts.count("reject")
    
    print(f"\n📊 审稿共识:")
    print(f"   接受: {accept_count} 票")
    print(f"   需修改: {revision_count} 票")
    print(f"   拒稿: {reject_count} 票")
    
    if accept_count >= 2:
        consensus = "倾向于接受"
    elif revision_count >= 2:
        consensus = "需要修改"
    else:
        consensus = "存在分歧"
    
    print(f"   总体建议: {consensus}")
    
    # 保存审稿报告
    report_data = {
        "draft_id": draft.draft_id,
        "review_reports": [r.to_dict() for r in review_reports],
        "consensus": consensus
    }
    
    with open("review_report.json", 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 审稿报告已保存: review_report.json")
    
    await aws.shutdown()

if __name__ == "__main__":
    asyncio.run(quick_review_mode())
```

### 4.4 示例4：流式生成（实时反馈）

```python
#!/usr/bin/env python3
"""
示例4：流式论文生成
- 实时查看进度
- WebSocket推送
- 中间结果预览
"""

import asyncio
from aws import AgentWritingSystem, PaperRequirements

async def stream_generation():
    """流式生成示例"""
    
    aws = AgentWritingSystem()
    await aws.initialize()
    
    requirements = PaperRequirements(
        topic="量子计算中的Shor算法实现与优化",
        word_count=4000
    )
    
    print("🚀 启动流式论文生成")
    print("-" * 60)
    
    # 流式接收进度
    async for update in aws.stream_generate(requirements):
        phase = update.get("phase")
        status = update.get("status")
        progress = update.get("progress", 0)
        message = update.get("message", "")
        
        if phase == "completed":
            print(f"\n✅ 生成完成!")
            final_draft = update.get("final_draft", {})
            print(f"   最终字数: {final_draft.get('word_count', 0)}")
            break
        
        # 显示进度条
        bar_length = 30
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"\r[{bar}] {progress}% | {phase}: {message}", end="", flush=True)
        
        # 阶段完成时换行
        if status == "completed" and phase != "completed":
            print()  # 换行
    
    await aws.shutdown()

if __name__ == "__main__":
    asyncio.run(stream_generation())
```

---

## 5. 论文模板系统

### 5.1 学科模板支持

```python
class PaperTemplateManager:
    """
    论文模板管理器
    支持不同学科和期刊的格式要求
    """
    
    TEMPLATES = {
        # 计算机科学
        "cs": {
            "name": "计算机科学",
            "sections": [
                "abstract",
                "introduction",
                "related_work",
                "methodology",
                "experiments",
                "results",
                "discussion",
                "conclusion",
                "references"
            ],
            "formatting": {
                "code_blocks": True,
                "algorithm_pseudocode": True,
                "dataset_tables": True
            }
        },
        
        # 数学
        "math": {
            "name": "数学",
            "sections": [
                "abstract",
                "introduction",
                "preliminaries",
                "main_results",
                "proofs",
                "implications",
                "conclusion",
                "references"
            ],
            "formatting": {
                "theorem_environment": True,
                "proof_environment": True,
                "equation_numbering": True
            }
        },
        
        # 物理学
        "physics": {
            "name": "物理学",
            "sections": [
                "abstract",
                "introduction",
                "theoretical_framework",
                "experimental_setup",
                "results",
                "discussion",
                "conclusion",
                "acknowledgments",
                "references"
            ],
            "formatting": {
                "si_units": True,
                "data_figures": True,
                "uncertainty_notation": True
            }
        },
        
        # 生物学
        "biology": {
            "name": "生物学",
            "sections": [
                "abstract",
                "introduction",
                "materials_methods",
                "results",
                "discussion",
                "conclusion",
                "acknowledgments",
                "references",
                "supplementary_materials"
            ],
            "formatting": {
                "species_names_italics": True,
                "statistical_notation": True,
                "protocol_details": True
            }
        }
    }
    
    JOURNAL_TEMPLATES = {
        "arxiv": {
            "name": "arXiv",
            "format": "latex",
            "template_file": "templates/arxiv.tex",
            "max_length": None,
            "abstract_length": None
        },
        
        "nature": {
            "name": "Nature",
            "format": "word",
            "max_length": 3000,  # words
            "abstract_length": 150,
            "figure_limit": 6,
            "style_guide": "nature_style.md"
        },
        
        "science": {
            "name": "Science",
            "format": "word",
            "max_length": 4000,
            "abstract_length": 125,
            "reference_limit": 40
        },
        
        "ieee_tit": {
            "name": "IEEE Transactions on Information Theory",
            "format": "latex",
            "template_file": "templates/ieee_trans.tex",
            "double_column": True
        },
        
        "acl": {
            "name": "ACL Conference",
            "format": "latex",
            "template_file": "templates/acl2024.tex",
            "max_length": 5000,  # 不含参考文献
            "abstract_length": 250
        },
        
        "neurips": {
            "name": "NeurIPS",
            "format": "latex",
            "template_file": "templates/neurips2024.tex",
            "max_length": 8000,
            "anonymous": True  # 双盲审稿
        },
        
        "icml": {
            "name": "ICML",
            "format": "latex",
            "template_file": "templates/icml2024.tex",
            "max_length": 8000
        }
    }
    
    def get_template(self, domain: str, journal: Optional[str] = None) -> Dict:
        """获取论文模板"""
        base_template = self.TEMPLATES.get(domain, self.TEMPLATES["cs"])
        
        if journal:
            journal_template = self.JOURNAL_TEMPLATES.get(journal, {})
            # 合并模板
            merged = {
                **base_template,
                "journal": journal_template,
                "format": journal_template.get("format", "markdown")
            }
            return merged
        
        return base_template
    
    def apply_template(
        self, 
        content: str, 
        template: Dict,
        output_format: str = "markdown"
    ) -> str:
        """应用模板格式化论文"""
        if output_format == "latex":
            return self._to_latex(content, template)
        elif output_format == "markdown":
            return self._to_markdown(content, template)
        else:
            return content
    
    def _to_latex(self, content: str, template: Dict) -> str:
        """转换为LaTeX格式"""
        journal = template.get("journal", {})
        template_file = journal.get("template_file")
        
        if template_file:
            # 读取模板文件并填充内容
            with open(template_file, 'r') as f:
                latex_template = f.read()
            
            # 替换占位符
            latex = latex_template.replace("%CONTENT%", content)
            return latex
        
        return content
```

---

**文档生成时间：** 2026年4月16日  
**状态：** API接口与使用示例完成  
**版本：** v1.0
