# SylvaFormalization 替代工具链探索报告

## 生成时间：2026-04-24

## 一、Docker 镜像方案

### 1.1 搜索结果
- **官方状态**：leanprover-community 未提供官方 Docker 镜像
- **社区实践**：用户通常自行构建或从源码编译
- **Gitee 镜像**：多个 Gitee 仓库提供 mathlib4 源码镜像，但不包含预编译缓存

### 1.2 可行性评估
| 方案 | 可行性 | 说明 |
|------|--------|------|
| 官方 Docker 镜像 | ❌ 不存在 | leanprover 未发布官方镜像 |
| 社区 Docker 镜像 | ⚠️ 可能 | 需搜索 Docker Hub 或自建 |
| 自建镜像 | ✅ 可行 | 在有网络机器构建后复制 |

### 1.3 推荐做法
```bash
# 在有网络的机器上构建 Docker 镜像
# Dockerfile 示例：
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl git
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
RUN elan toolchain install leanprover/lean4:v4.30.0-rc2
RUN elan default leanprover/lean4:v4.30.0-rc2
RUN git clone https://github.com/leanprover-community/mathlib4.git /mathlib
WORKDIR /mathlib
RUN lake update && lake exe cache get && lake build
```

## 二、预编译缓存获取方案

### 2.1 缓存服务器信息
- **主服务器**：Azure Blob Storage (`lakecache.blob.core.windows.net`)
- **可达性**：✅ 当前环境可达（返回 HTTP 400）
- **问题**：Lake 工具链在尝试缓存下载前执行 Git 检查，导致超时

### 2.2 直接下载方案
```bash
# 获取 mathlib commit hash
MATHLIB_REV=$(cd .lake/packages/mathlib && git rev-parse HEAD)

# 构造缓存 URL（需确认确切格式）
# 可能的格式：
# https://lakecache.blob.core.windows.net/mathlib4/${MATHLIB_REV}/...

# 直接下载（需进一步研究 URL 格式）
```

### 2.3 外部传输方案
```bash
# 在有网络的机器上
# 1. 下载完整缓存
cd /path/to/SylvaFormalization
lake exe cache get

# 2. 打包 .lake 目录
tar czvf sylva-full-cache.tar.gz .lake/

# 3. 传输到受限环境并解压
tar xzvf sylva-full-cache.tar.gz
```

## 三、Lean 版本兼容性

### 3.1 当前版本
- **Lean**：4.30.0-rc2
- **mathlib 源码**：完整（Mathlib/ 目录存在）
- **.olean 缓存**：严重不足（仅 111 个文件，需 4000+）

### 3.2 版本匹配确认
- ✅ ABI 匹配：缓存和编译器均为 4.30.0-rc2
- ✅ 源码完整：34 个子模块
- ❌ 缓存缺失：无法编译

## 四、Gitee 镜像状态

### 4.1 可用镜像
| 仓库 | URL | 状态 |
|------|-----|------|
| mathlib4 | https://gitee.com/huangshangwu/mathlib4 | 源码镜像 |
| mathlib4 | https://gitee.com/stchai/mathlib4 | 源码镜像 |
| mathlib4 | https://gitee.com/HyappStolz2/mathlib4 | 源码镜像 |

### 4.2 限制
- Gitee 镜像仅包含源码，无预编译缓存
- lake update 仍可能因工具链初始化超时

## 五、推荐解决方案

### 方案 1：外部缓存传输（最可行）
```bash
# 步骤 1：在有网络的环境准备缓存
# （另一台机器、虚拟机、或网络恢复后的本机）

# 步骤 2：执行标准流程
lake update
lake exe cache get  # 下载 5-8GB 缓存
lake build          # 编译项目

# 步骤 3：打包传输
tar czvf sylva-cache-$(date +%Y%m%d).tar.gz .lake/

# 步骤 4：在受限环境解压
tar xzvf sylva-cache-*.tar.gz
lake build --offline
```

### 方案 2：等待网络恢复
- 当前状态：GitHub 特定被限制
- 恢复标志：`curl -I https://github.com/leanprover-community/mathlib4` 返回 HTTP 200
- 恢复后执行：标准 lake update + cache get + build 流程

### 方案 3：降级 Lean 版本（不推荐）
- 风险：可能引入 API 不兼容
- 需要：找到与现有缓存匹配的 Lean 版本
- 当前缓存版本：4.30.0-rc2（已匹配）

## 六、当前环境限制总结

| 限制 | 影响 | 解决方案 |
|------|------|----------|
| GitHub 访问受限 | Lake 初始化超时 | 外部传输缓存 |
| 本地缓存不足 | 无法编译 | 获取完整缓存 |
| cache 工具路径硬编码 | 无法直接调用 | 从 mathlib 目录调用 |
| Lake 离线模式不完善 | --offline 仍尝试网络 | 等待修复或绕过 |

## 七、立即行动建议

1. **保存当前状态**（已完成）
   - ✅ 代码备份：sylva-backup-20260424.tar.gz (35MB)
   - ✅ 状态报告：PROJECT_STATUS_REPORT.md

2. **获取外部缓存**
   - 寻找有网络的环境（其他机器、虚拟机、云服务器）
   - 执行 lake update + lake exe cache get
   - 打包 .lake 目录并传输

3. **验证编译**
   - 解压缓存后执行 lake build --offline
   - 验证 FourForcesUnification.lean 编译成功

---
**结论**：当前环境无法独立完成编译，需要外部缓存传输或网络恢复。代码层面工作已全部完成。
