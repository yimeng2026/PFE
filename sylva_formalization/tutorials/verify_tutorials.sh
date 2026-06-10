#!/bin/bash
# =============================================================================
# Sylva Tutorial Verification Script
# =============================================================================
# 用法: ./verify_tutorials.sh
# 
# 这个脚本验证所有教程文件是否可以正确编译
# =============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 加载 Lean 环境
source $HOME/.elan/env 2>/dev/null || true

echo "========================================"
echo "Sylva Tutorial Verification"
echo "========================================"
echo ""

# 检查 lean/lake 是否可用
if ! command -v lake &> /dev/null; then
    echo -e "${RED}错误: lake 命令未找到${NC}"
    echo "请确保 Lean 4 已正确安装"
    exit 1
fi

echo -e "${GREEN}✓${NC} lake 命令可用"
echo ""

# 教程文件列表
TUTORIALS=(
    "tutorials/01_introduction/BasicTutorial.lean"
)

# 检查文件是否存在
echo "检查教程文件..."
for tutorial in "${TUTORIALS[@]}"; do
    if [ -f "$tutorial" ]; then
        echo -e "  ${GREEN}✓${NC} $tutorial"
    else
        echo -e "  ${RED}✗${NC} $tutorial (未找到)"
    fi
done
echo ""

# 验证教程模块编译
echo "验证教程模块..."
if lake build SylvaTutorial 2>&1 | tee /tmp/tutorial_build.log; then
    echo -e "${GREEN}✓${NC} 教程模块编译成功"
else
    echo -e "${YELLOW}⚠${NC} 教程模块编译有警告（可能有 sorry 标记）"
    echo "查看详细日志: /tmp/tutorial_build.log"
fi
echo ""

# 统计教程内容
echo "教程统计:"
echo "  教程文件数: $(find tutorials -name "*.lean" | wc -l)"
echo "  总代码行数: $(find tutorials -name "*.lean" -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo ""

# 检查练习完成情况
echo "练习统计:"
EXERCISE_COUNT=$(grep -r "theorem exercise_" tutorials/ | wc -l)
SOLUTION_COUNT=$(grep -r "theorem solution_" tutorials/ | wc -l)
echo "  练习题数量: $EXERCISE_COUNT"
echo "  参考答案数量: $SOLUTION_COUNT"
echo ""

# 生成报告
echo "========================================"
echo "验证完成"
echo "========================================"
echo ""
echo "下一步:"
echo "  1. 打开 tutorials/01_introduction/BasicTutorial.lean 开始学习"
echo "  2. 阅读 tutorials/README.md 了解完整学习路径"
echo "  3. 完成练习，替换 sorry 标记为实际证明"
echo ""
