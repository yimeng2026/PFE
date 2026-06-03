# SylvaFormalization 外部缓存传输指南

## 方案概述

在当前环境（GitHub受限）无法完成编译的情况下，通过另一台有网络的机器获取完整预编译缓存，然后传输到当前环境。

## 前提条件

- **源机器**：能访问 GitHub 和 Azure Blob Storage
- **目标机器**：当前受限环境（已有 Lean 4.30.0-rc2 和项目源码）
- **传输方式**：USB、scp、rsync、云盘等

---

## 第一步：在源机器准备缓存

### 1.1 安装 Lean 和 Elan

```bash
# 安装 elan（Lean 版本管理器）
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
source $HOME/.elan/env

# 验证安装
elan --version
lean --version
```

### 1.2 克隆 SylvaFormalization 项目

```bash
# 方法 A：从 GitHub 克隆（如果源机器有 GitHub 访问）
git clone https://github.com/your-repo/SylvaFormalization.git
cd SylvaFormalization

# 方法 B：从当前环境复制源码（如果无法访问 GitHub）
# 在当前环境执行：
# tar czvf sylva-src.tar.gz --exclude=.lake SylvaFormalization/
# 然后传输到源机器
```

### 1.3 同步 Lean 版本

```bash
# 确保 Lean 版本与目标机器一致（4.30.0-rc2）
cat lean-toolchain
# 输出应为：leanprover/lean4:v4.30.0-rc2

# 如果不一致，安装对应版本
elan toolchain install leanprover/lean4:v4.30.0-rc2
elan override set leanprover/lean4:v4.30.0-rc2
```

### 1.4 下载依赖和缓存

```bash
# 更新依赖（下载 mathlib 等）
lake update

# 下载预编译缓存（关键步骤！约 5-8GB）
lake exe cache get

# 验证缓存下载成功
find .lake -name "*.olean" | wc -l
# 预期输出：4000+（mathlib 完整缓存）
```

### 1.5 编译项目

```bash
# 编译整个项目（使用缓存后很快）
lake build

# 验证编译成功
echo $?  # 应为 0
```

---

## 第二步：打包缓存

### 2.1 打包 .lake 目录

```bash
# 进入项目目录
cd SylvaFormalization

# 打包 .lake 目录（包含所有依赖和缓存）
tar czvf sylva-cache-full.tar.gz .lake/

# 查看大小
ls -lh sylva-cache-full.tar.gz
# 预期：5-10GB
```

### 2.2 验证打包完整性

```bash
# 测试解压
tar tzvf sylva-cache-full.tar.gz | head -20

# 检查关键文件是否存在
tar tzvf sylva-cache-full.tar.gz | grep "Mathlib.olean" | head -5
tar tzvf sylva-cache-full.tar.gz | grep "Cache/Init.olean" | head -5
```

---

## 第三步：传输到目标机器

### 3.1 传输方式选择

| 方式 | 适用场景 | 命令 |
|------|---------|------|
| **scp** | 两台机器网络互通 | `scp sylva-cache-full.tar.gz user@target:/path/` |
| **rsync** | 大文件/断点续传 | `rsync -avz --progress sylva-cache-full.tar.gz user@target:/path/` |
| **USB** | 物理接触 | 复制到 U 盘 |
| **云盘** | 有网盘账号 | 上传到云盘后下载 |
| **nc** | 同一局域网 | `nc -l 1234 > sylva-cache-full.tar.gz` |

### 3.2 示例：使用 scp

```bash
# 在源机器执行
scp sylva-cache-full.tar.gz root@target-ip:/root/.openclaw/workspace/sylva_formalization/

# 输入密码后等待传输完成
```

### 3.3 示例：使用 rsync（推荐大文件）

```bash
# 在源机器执行
rsync -avz --progress --partial sylva-cache-full.tar.gz \
  root@target-ip:/root/.openclaw/workspace/sylva_formalization/

# --partial 支持断点续传
```

---

## 第四步：在目标机器恢复

### 4.1 解压缓存

```bash
# 进入项目目录
cd /root/.openclaw/workspace/sylva_formalization/SylvaFormalization

# 备份现有 .lake（以防万一）
mv .lake .lake.backup.$(date +%Y%m%d)

# 解压缓存
tar xzvf /path/to/sylva-cache-full.tar.gz

# 验证解压成功
ls -la .lake/packages/mathlib/.lake/build/lib/lean/ | head -10
```

### 4.2 验证 Lean 版本匹配

```bash
# 检查 Lean 版本
lean --version
# 输出：Lean (version 4.30.0-rc2, ...)

# 检查缓存版本（从 .olean 文件）
strings .lake/packages/mathlib/.lake/build/lib/lean/Cache/Init.olean | grep "4.30.0"
# 应输出：4.30.0-rc2
```

### 4.3 编译项目

```bash
# 使用离线模式编译（不再尝试网络）
lake build --offline

# 或标准编译（如果网络已恢复）
lake build
```

### 4.4 验证编译结果

```bash
# 检查编译成功
echo $?  # 应为 0

# 验证关键文件
lake build FourForcesUnification

# 检查无 sorry
grep -rn "^[[:space:]]*sorry[[:space:]]*$" *.lean | grep -v "_amputated" | wc -l
# 应为 0
```

---

## 第五步：清理和优化

### 5.1 删除备份

```bash
# 确认编译成功后删除备份
rm -rf .lake.backup.20260424
rm -f sylva-cache-full.tar.gz  # 删除传输文件
```

### 5.2 验证项目完整性

```bash
# 运行所有测试（如果有）
lake test 2>/dev/null || echo "无测试配置"

# 检查所有模块编译状态
lake build 2>&1 | tail -20
```

---

## 故障排除

### 问题 1：ABI 不匹配

**现象**：`unknown declaration` 或 `corrupt olean file`

**解决**：
```bash
# 检查版本
lean --version  # 目标机器
# 与源机器对比，确保一致

# 如果不一致，统一版本
elan toolchain install leanprover/lean4:v4.30.0-rc2
elan default leanprover/lean4:v4.30.0-rc2
```

### 问题 2：缓存不完整

**现象**：编译时仍需要下载文件

**解决**：
```bash
# 重新在源机器执行
lake exe cache get!
# 注意：get! 会强制重新下载

# 重新打包传输
```

### 问题 3：路径问题

**现象**：`unknown package` 或 `unknown module`

**解决**：
```bash
# 检查 lake-manifest.json
# 确保与源机器一致

# 重新生成 manifest
rm -f lake-manifest.json
lake update --offline
```

---

## 快速检查清单

- [ ] 源机器 Lean 版本：4.30.0-rc2
- [ ] 目标机器 Lean 版本：4.30.0-rc2
- [ ] 源机器 `lake exe cache get` 成功
- [ ] 源机器 `lake build` 成功
- [ ] 打包文件大小：5-10GB
- [ ] 传输完成无损坏
- [ ] 目标机器解压成功
- [ ] 目标机器 `lake build --offline` 成功
- [ ] FourForcesUnification 编译通过
- [ ] 无 sorry 残留

---

## 附录：最小化传输方案

如果 5-10GB 太大，可以尝试只传输关键缓存：

```bash
# 在源机器：只打包关键 .olean 目录
tar czvf sylva-cache-minimal.tar.gz \
  .lake/packages/mathlib/.lake/build/lib/lean/ \
  .lake/packages/batteries/.lake/build/lib/lean/ \
  .lake/packages/Qq/.lake/build/lib/lean/ \
  .lake/packages/aesop/.lake/build/lib/lean/ \
  .lake/packages/proofwidgets/.lake/build/lib/lean/ \
  .lake/packages/importGraph/.lake/build/lib/lean/

# 然后在目标机器：
# 1. 先执行 lake update（获取源码）
# 2. 解压缓存到对应位置
# 3. lake build --offline
```

**注意**：最小化方案可能需要目标机器有 GitHub 访问（用于 lake update），否则仍需完整传输。

---

**版本**：v1.0  
**日期**：2026-04-24  
**作者**：Kimi Claw
