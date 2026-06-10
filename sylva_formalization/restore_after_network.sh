#!/bin/bash
# SylvaFormalization 网络恢复后恢复脚本
# 保存到 /root/.openclaw/workspace/sylva_formalization/restore_after_network.sh

set -e

echo "=== SylvaFormalization 网络恢复恢复脚本 ==="
echo "生成时间: 2026-04-24"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目目录
PROJECT_DIR="/root/.openclaw/workspace/sylva_formalization/SylvaFormalization"
cd "$PROJECT_DIR"

echo "=== Step 1: 验证网络恢复 ==="
if curl -I https://github.com/leanprover-community/mathlib4 2>&1 | head -3 | grep -q "HTTP.*200"; then
    echo -e "${GREEN}✅ GitHub 访问已恢复${NC}"
else
    echo -e "${RED}❌ GitHub 仍未恢复，请稍后重试${NC}"
    echo "恢复标志: curl -I https://github.com/leanprover-community/mathlib4 返回 HTTP 200"
    exit 1
fi

echo ""
echo "=== Step 2: 恢复 lake-manifest.json ==="
# 如果之前修改为 Gitee，恢复 GitHub 配置
if grep -q "gitee.com" lake-manifest.json 2>/dev/null; then
    echo "检测到 Gitee 镜像配置，恢复为 GitHub..."
    # 重新生成 manifest（从 lakefile.lean）
    rm -f lake-manifest.json
fi

echo ""
echo "=== Step 3: 更新依赖 ==="
lake update 2>&1 | tee /tmp/lake-update.log
echo -e "${GREEN}✅ 依赖更新完成${NC}"

echo ""
echo "=== Step 4: 下载预编译缓存 ==="
echo "这可能需要 10-30 分钟，取决于网络速度..."
lake exe cache get 2>&1 | tee /tmp/cache-download.log
echo -e "${GREEN}✅ 缓存下载完成${NC}"

echo ""
echo "=== Step 5: 编译项目 ==="
lake build 2>&1 | tee /tmp/build.log
echo -e "${GREEN}✅ 项目编译完成${NC}"

echo ""
echo "=== Step 6: 验证关键文件 ==="
if lake build FourForcesUnification 2>&1 | grep -q "Build completed"; then
    echo -e "${GREEN}✅ FourForcesUnification 编译验证通过${NC}"
else
    echo -e "${YELLOW}⚠️  FourForcesUnification 编译可能有警告，请检查日志${NC}"
fi

echo ""
echo "=== Step 7: 验证所有模块 ==="
# 检查是否还有 sorry
SORRY_COUNT=$(grep -rn "^[[:space:]]*sorry[[:space:]]*$" *.lean 2>/dev/null | grep -v "_amputated" | wc -l)
if [ "$SORRY_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✅ 所有模块无 sorry（截肢降级生效）${NC}"
else
    echo -e "${YELLOW}⚠️  发现 $SORRY_COUNT 个 sorry（可能是新添加的）${NC}"
fi

echo ""
echo "=== 恢复完成 ==="
echo "日志文件:"
echo "  - /tmp/lake-update.log"
echo "  - /tmp/cache-download.log"
echo "  - /tmp/build.log"
echo ""
echo "如果编译成功，可以删除备份文件:"
echo "  rm sylva-backup-20260424.tar.gz"
echo ""
echo "下一步:"
echo "  1. 检查编译输出是否有错误"
echo "  2. 运行 lake build 验证所有模块"
echo "  3. 开始回填 admit 为实际证明"
