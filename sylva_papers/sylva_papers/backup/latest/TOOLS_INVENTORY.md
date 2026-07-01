# SYLVA 项目完整工具箱清单
**日期**: 2026-04-21
**项目**: 数学物理形式化 + 熵间隙谱理论 + P≠NP研究

---

## 1. 数学工具箱

### 1.1 计算机代数系统 (CAS)
- [x] **SageMath** — 数论、代数几何、椭圆曲线（BSD猜想）
- [x] **PARI/GP** — 高精度数论计算、L函数
- [x] **Magma** — 代数几何、模形式（如有许可证）
- [x] **GAP** — 群论、表示论
- [x] **Singular** — 交换代数、代数几何
- [x] **Macaulay2** — 代数几何、同调代数

### 1.2 数值计算
- [x] **NumPy/SciPy** — 数值线性代数、优化
- [x] **SymPy** — 符号计算（Python）
- [x] **mpmath** — 任意精度算术
- [x] **Arb (FLINT)** —  rigorous数值计算、区间算术

### 1.3 数论专用
- [x] **msieve** — 大整数分解
- [x] **GGNFS** — 数域筛法
- [x] **ecm** — 椭圆曲线分解法
- [x] **primesieve** — 素数生成
- [x] **lcalc** — L函数计算

### 1.4 谱理论/泛函分析
- [x] **SpectralPython** — 谱分析
- [x] **SLEPc** — 大规模特征值问题（PETSc扩展）

---

## 2. 物理工具箱

### 2.1 量子力学/量子场论
- [x] **QuTiP** — 量子动力学、开放量子系统
- [x] **QuantumOpt.jl** — 量子光学（Julia）
- [x] **SymPy.physics.quantum** — 符号量子力学
- [x] **FeynArts/FormCalc** — 费曼图计算

### 2.2 统计物理/复杂系统
- [x] **NetLogo** — 复杂系统模拟
- [x] **Ising model solvers** — 相变模拟
- [x] **TensorNetwork (ITensor, TenPy)** — 张量网络

### 2.3 流体力学（Navier-Stokes）
- [x] **FEniCS** — 有限元方法
- [x] **OpenFOAM** — 计算流体力学
- [x] **Dedalus** — 谱方法PDE求解

### 2.4 广义相对论/宇宙学
- [x] **Einstein Toolkit** — 数值相对论
- [x] **xAct** — 张量计算（Mathematica）

---

## 3. 可视化工具箱

### 3.1 科学可视化
- [x] **Matplotlib** — 基础绘图
- [x] **Plotly/Dash** — 交互式可视化
- [x] **Bokeh** — 大规模交互可视化
- [x] **Mayavi** — 3D科学可视化
- [x] **VisPy** — GPU加速可视化

### 3.2 复杂网络/图论
- [x] **Gephi** — 网络可视化
- [x] **Cytoscape** — 生物网络（可扩展）
- [x] **NetworkX + Matplotlib** — Python网络可视化

### 3.3 数学可视化
- [x] **Manim** — 数学动画（3Blue1Brown风格）
- [x] **GeoGebra** — 几何可视化
- [x] **Complex Plot** — 复变函数可视化
- [x] **Domain Coloring** — 复数域着色

### 3.4 谱可视化
- [x] **Spectrogram tools** — 频谱图
- [x] **Eigenvalue plotting** — 特征值分布
- [x] **Heatmap tools** — 矩阵热图

---

## 4. 编程/开发工具箱

### 4.1 核心语言
- [x] **Lean 4** — 形式化证明（已有）
- [x] **Python 3.11+** — 科学计算脚本
- [x] **Julia 1.9+** — 高性能数值计算
- [x] **Haskell** — 函数式编程、类型理论
- [x] **Rust** — 高性能系统编程

### 4.2 开发环境
- [x] **VS Code** — 编辑器 + Lean/Coq插件
- [x] **JupyterLab** — 交互式笔记本
- [x] **Git + GitHub/GitLab** — 版本控制
- [x] **Docker** — 环境隔离

### 4.3 文档工具
- [x] **LaTeX (TeX Live)** — 论文排版
- [x] **Pandoc** — 格式转换
- [x] **MkDocs** — 文档网站
- [x] **Sphinx** — Python文档

---

## 5. 机器学习/AI工具箱

### 5.1 深度学习框架
- [x] **PyTorch** — 神经网络
- [x] **JAX** — 可微分编程
- [x] **TensorFlow** — 生产部署

### 5.2 符号回归/自动发现
- [x] **PySR** — 符号回归
- [x] **AI Feynman** — 物理定律发现
- [x] **SINDy** — 稀疏识别

### 5.3 形式化AI
- [x] **Tactician** — Lean证明策略学习
- [x] **HOList/Graph2Tac** — 定理证明AI

---

## 6. 数据库/知识管理

### 6.1 文献管理
- [x] **Zotero** — 文献管理
- [x] **JabRef** — BibTeX管理

### 6.2 知识图谱
- [x] **Neo4j** — 图数据库
- [x] **RDF/SPARQL** — 语义网

### 6.3 版本化数据
- [x] **DVC** — 数据版本控制
- [x] **LakeFS** — 数据湖版本

---

## 7. 协作/项目管理

- [x] **OpenClaw Agent集群** — 已有
- [x] **Taskwarrior** — 命令行任务管理
- [x] **Timewarrior** — 时间追踪
- [x] **Hledger** — 会计/预算（如需要）

---

## 8. 特殊工具

### 8.1 随机性/密码学
- [x] **Dieharder** — 随机性测试
- [x] **NIST STS** — 统计测试套件
- [x] **OpenSSL** — 密码学基础

### 8.2 复杂性理论专用
- [x] **SAT solvers** — MiniSat, Z3, CryptoMiniSat
- [x] **SMT solvers** — Z3, CVC5, Yices
- [x] **Model checkers** — nuXmv, SPIN

### 8.3 形式化验证
- [x] **Coq** — 替代证明助手
- [x] **Isabelle/HOL** — 高阶逻辑
- [x] **TLA+** — 分布式系统规范

---

## 安装优先级

### P0 (立即安装)
1. Lean 4 + mathlib4
2. Python 3.11 + NumPy/SciPy/SymPy
3. SageMath
4. LaTeX

### P1 (本周)
5. Julia + 科学计算包
6. JupyterLab
7. VS Code + 插件
8. Git配置

### P2 (本月)
9. 可视化栈 (Matplotlib, Plotly, Manim)
10. SAT/SMT求解器
11. 机器学习框架

### P3 (按需)
12. 物理专用工具
13. 形式化AI工具
14. 数据库系统

---

**总计**: 60+ 个工具/包
**核心工具**: ~15个
**完整安装时间**: 预计 4-8小时
