# SylvaFormalization Docker 镜像构建指南

## 方案概述

在有网络的机器上构建包含完整 mathlib 预编译缓存的 Docker 镜像，然后导出并传输到受限环境。

## 优势

- **一次性构建**：镜像包含所有依赖，无需重复下载
- **版本锁定**：Lean、mathlib、依赖版本固定
- **可移植**：单个镜像文件（5-10GB）传输到任意环境
- **离线运行**：目标环境无需任何网络访问

---

## 第一步：创建 Dockerfile

```dockerfile
# ============================================
# SylvaFormalization Docker 镜像
# Lean 4.30.0-rc2 + mathlib4 完整预编译缓存
# ============================================

FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV ELAN_HOME=/root/.elan
ENV PATH="${ELAN_HOME}/bin:${PATH}"
ENV LEAN_VERSION=leanprover/lean4:v4.30.0-rc2

# 安装基础依赖
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libgmp-dev \
    cmake \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 安装 elan（Lean 版本管理器）
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
ENV PATH="${ELAN_HOME}/bin:${PATH}"

# 安装指定版本的 Lean
RUN elan toolchain install ${LEAN_VERSION} \
    && elan default ${LEAN_VERSION}

# 验证安装
RUN lean --version && lake --version

# ============================================
# 阶段 2：下载 SylvaFormalization 项目
# ============================================

WORKDIR /workspace

# 方法 A：从 GitHub 克隆（推荐）
RUN git clone https://github.com/leanprover-community/mathlib4.git /workspace/mathlib4

# 方法 B：如果 Sylva 项目有独立仓库
# RUN git clone https://github.com/your-org/SylvaFormalization.git /workspace/SylvaFormalization

# ============================================
# 阶段 3：下载依赖和预编译缓存
# ============================================

WORKDIR /workspace/mathlib4

# 下载依赖
RUN lake update

# 下载预编译缓存（关键步骤！约 5-8GB）
RUN lake exe cache get

# 编译 mathlib（验证缓存完整性）
RUN lake build

# ============================================
# 阶段 4：添加 SylvaFormalization 项目
# ============================================

WORKDIR /workspace/SylvaFormalization

# 复制本地项目文件（构建时从上下文复制）
COPY . /workspace/SylvaFormalization/

# 设置依赖为本地路径（避免网络）
# 修改 lakefile.lean 指向 /workspace/mathlib4
RUN sed -i 's|require mathlib from git.*|require mathlib from "/workspace/mathlib4"|' lakefile.lean

# 编译 Sylva 项目
RUN lake build --offline

# ============================================
# 阶段 5：配置运行时环境
# ============================================

WORKDIR /workspace/SylvaFormalization

# 设置入口点
CMD ["/bin/bash"]
```

---

## 第二步：构建镜像

### 2.1 准备构建上下文

```bash
# 创建构建目录
mkdir -p ~/docker-sylva
cd ~/docker-sylva

# 复制 Dockerfile
cp /path/to/Dockerfile .

# 复制 SylvaFormalization 项目（排除 .lake 目录）
rsync -av --exclude=.lake \
  /path/to/SylvaFormalization/ \
  ./SylvaFormalization/
```

### 2.2 执行构建

```bash
# 构建镜像（可能需要 30-60 分钟）
docker build -t sylva-formalization:v1.0 \
  --build-arg LEAN_VERSION=leanprover/lean4:v4.30.0-rc2 \
  . 2>&1 | tee /tmp/docker-build.log

# 验证构建成功
docker images | grep sylva-formalization
```

### 2.3 构建优化（减少层数）

```dockerfile
# 多阶段构建（减小最终镜像大小）
# 第一阶段：构建环境
FROM ubuntu:22.04 AS builder
# ... 安装依赖、下载缓存 ...

# 第二阶段：运行时环境
FROM ubuntu:22.04 AS runtime
COPY --from=builder /workspace /workspace
COPY --from=builder /root/.elan /root/.elan
ENV PATH="/root/.elan/bin:${PATH}"
WORKDIR /workspace/SylvaFormalization
CMD ["/bin/bash"]
```

---

## 第三步：导出镜像

### 3.1 导出为 tar 文件

```bash
# 保存镜像为 tar 文件
docker save sylva-formalization:v1.0 \
  | gzip > sylva-docker-image.tar.gz

# 查看大小
ls -lh sylva-docker-image.tar.gz
# 预期：5-15GB（取决于层数优化）
```

### 3.2 验证导出

```bash
# 测试加载（不实际加载）
docker load --input sylva-docker-image.tar.gz --dry-run 2>/dev/null || \
  echo "导出文件已生成"

# 检查文件完整性
tar tzvf sylva-docker-image.tar.gz | head -10
```

---

## 第四步：传输到目标机器

### 4.1 传输方式

| 方式 | 命令 | 适用场景 |
|------|------|---------|
| **scp** | `scp sylva-docker-image.tar.gz user@target:/path/` | 网络互通 |
| **rsync** | `rsync -avz --progress sylva-docker-image.tar.gz user@target:/path/` | 大文件/断点续传 |
| **USB** | 复制到移动硬盘 | 物理传输 |
| **云盘** | 上传后下载 | 有网盘账号 |

### 4.2 示例：rsync 传输

```bash
# 在源机器执行
rsync -avz --progress --partial \
  sylva-docker-image.tar.gz \
  root@target-ip:/root/.openclaw/workspace/

# 传输时间：取决于带宽（10GB 约 1-2 小时 @ 10MB/s）
```

---

## 第五步：在目标机器加载和运行

### 5.1 安装 Docker（如果未安装）

```bash
# 检查 Docker 是否安装
docker --version || {
    # 安装 Docker
    curl -fsSL https://get.docker.com | sh
    systemctl start docker
    systemctl enable docker
}
```

### 5.2 加载镜像

```bash
# 进入传输目录
cd /root/.openclaw/workspace

# 加载镜像（可能需要 5-10 分钟）
docker load --input sylva-docker-image.tar.gz

# 验证加载成功
docker images | grep sylva-formalization
```

### 5.3 运行容器

```bash
# 运行容器（交互模式）
docker run -it \
  --name sylva-dev \
  -v /root/.openclaw/workspace/sylva_formalization:/workspace/SylvaFormalization \
  sylva-formalization:v1.0 \
  /bin/bash

# 在容器内验证
lean --version
lake --version
cd /workspace/SylvaFormalization
lake build --offline
```

### 5.4 持久化工作目录

```bash
# 使用数据卷持久化项目文件
docker run -it \
  --name sylva-dev \
  -v sylva-data:/workspace/SylvaFormalization \
  sylva-formalization:v1.0

# 容器内修改会保存到 Docker 卷
docker volume ls | grep sylva-data
```

---

## 第六步：日常使用

### 6.1 启动已有容器

```bash
# 启动已停止的容器
docker start sylva-dev

# 进入容器
docker exec -it sylva-dev /bin/bash

# 在容器内工作
cd /workspace/SylvaFormalization
lake build
```

### 6.2 提交修改到新镜像

```bash
# 如果容器内有重要修改，保存为新镜像
docker commit sylva-dev sylva-formalization:v1.1

# 导出更新后的镜像
docker save sylva-formalization:v1.1 | gzip > sylva-docker-image-v1.1.tar.gz
```

### 6.3 清理

```bash
# 停止容器
docker stop sylva-dev

# 删除容器（保留镜像）
docker rm sylva-dev

# 删除镜像（如果需要）
docker rmi sylva-formalization:v1.0
```

---

## 故障排除

### 问题 1：镜像太大

**解决**：使用多阶段构建
```dockerfile
# 只保留运行时需要的文件
FROM ubuntu:22.04 AS runtime
COPY --from=builder /workspace/mathlib4/.lake/build /workspace/mathlib4/.lake/build
COPY --from=builder /workspace/SylvaFormalization /workspace/SylvaFormalization
```

### 问题 2：加载镜像失败

**解决**：
```bash
# 检查文件完整性
gzip -t sylva-docker-image.tar.gz

# 重新导出
docker save sylva-formalization:v1.0 | gzip > sylva-docker-image-new.tar.gz
```

### 问题 3：容器内无法访问项目文件

**解决**：
```bash
# 检查挂载路径
docker inspect sylva-dev | grep -A 5 "Mounts"

# 重新运行并正确挂载
docker run -it \
  -v /absolute/path/to/SylvaFormalization:/workspace/SylvaFormalization \
  sylva-formalization:v1.0
```

---

## 快速检查清单

- [ ] 源机器 Docker 已安装
- [ ] 源机器可访问 GitHub
- [ ] Dockerfile 配置正确
- [ ] 镜像构建成功
- [ ] 镜像导出成功
- [ ] 传输文件完整
- [ ] 目标机器 Docker 已安装
- [ ] 镜像加载成功
- [ ] 容器运行正常
- [ ] lake build --offline 成功
- [ ] FourForcesUnification 编译通过

---

## 附录：最小化镜像方案

如果完整镜像太大，可以只包含必要组件：

```dockerfile
# 最小化 Dockerfile
FROM ubuntu:22.04

# 只安装运行时依赖
RUN apt-get update && apt-get install -y libgmp10

# 复制 elan 和 Lean
COPY --from=builder /root/.elan /root/.elan
ENV PATH="/root/.elan/bin:${PATH}"

# 复制 .lake 缓存（不包含源码）
COPY --from=builder /workspace/mathlib4/.lake /workspace/mathlib4/.lake
COPY --from=builder /workspace/SylvaFormalization /workspace/SylvaFormalization

WORKDIR /workspace/SylvaFormalization
CMD ["/bin/bash"]
```

**预期大小**：3-5GB（比完整镜像小 50%）

---

## 附录：使用 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  sylva:
    image: sylva-formalization:v1.0
    container_name: sylva-dev
    volumes:
      - ./SylvaFormalization:/workspace/SylvaFormalization
      - sylva-cache:/workspace/mathlib4/.lake
    working_dir: /workspace/SylvaFormalization
    command: /bin/bash
    stdin_open: true
    tty: true

volumes:
  sylva-cache:
```

使用：
```bash
docker-compose up -d
docker-compose exec sylva /bin/bash
```

---

**版本**：v1.0  
**日期**：2026-04-24  
**作者**：Kimi Claw
