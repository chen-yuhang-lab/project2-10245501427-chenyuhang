# 当代人工智能实验二：搜索算法

学号：10245501427 姓名：陈禹航

本项目实现了A*搜索算法（含普通迷宫与加权地形）、Minimax与Alpha-Beta剪枝算法，以及竞争环境下的宝藏分配综合题。

## 1. 环境与依赖
- **Python 版本**: Python 3.8+
- **依赖库**: `heapq`, `math`, `copy`, `json`, `matplotlib` (仅用于生成实验图表)
- **安装命令**: `pip install matplotlib` (若需重新生成图表)
- **适用平台**: Windows / macOS / Linux

## 2. 数据与目录
- **输入文件**: 题目四的地图数据硬编码于`src/problem4.py`中。
- **目录结构**:
  - `src/`: 核心算法源码 (`astar.py`, `minimax.py`, `problem4.py`, `tree_utils.py`)
  - `experiments/`: 对照实验与图表生成脚本 (`run_experiments.py`)
  - `outputs/`: 运行结果输出目录（包含 `distance_matrix.txt` 和 `figures/` 图表）
- **字段说明**: 地图为二维数组，`X`为障碍物，数字为地形代价，`A`, `B`, `T`为实体位置。

## 3. 运行顺序
在项目根目录下，依次执行以下命令：
1. **题目一 & 题目二**: `python src/astar.py`
2. **题目三**: `python src/minimax.py`
3. **题目四**: `python src/problem4.py`
4. **对照实验与图表生成**: `python experiments/run_experiments.py`

## 4. 实验配置
- **A\* 启发函数**: 题目一/二采用曼哈顿距离，设定 `h=0` (Dijkstra) 作为对照组。
- **Alpha-Beta 搜索顺序**: 默认从左到右访问，对照实验中对子节点排序后访问。
- **题目四搜索深度**: H=2与H=4。分别使用Minimax和Alpha-Beta

## 5. 结果与提交
- **指标**: 节点访问数、剪枝次数、最终代价。
- **图表位置**: 见 `outputs/figures/`，包含启发函数影响折线图和剪枝效率柱状图。
- **最终预测文件**: `outputs/distance_matrix.txt` 包含6x6距离矩阵结果。

## 6. 复现与限制
- **核验方法**: 运行上述命令即可输出对应结果并比对。
- **预期输出**: 
  - 题目一: `[(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)]`
  - 题目二: `7`
  - 题目三: `5`
  - 题目四: 6x6 距离矩阵:A	B	T1	T2	T3	T4

A	0	14	10	4	8	10

B	14	0	9	9	5	11

T1	10	9	0	5	7	13

T2	4	9	5	0	6	8

T3	8	5	7	6	0	5

T4	10	11	13	8	5	0

Alpha-Beta H=2 结果: {'best_target': 'T2', 'best_value': 0}

Alpha-Beta H=2 访问节点数: 16, 剪枝次数: 0

Minimax    H=2 结果: {'best_target': 'T2', 'best_value': 0}

Minimax    H=2 访问节点数: 16

Alpha-Beta H=4 结果: {'best_target': 'T3', 'best_value': 5}

Alpha-Beta H=4 访问节点数: 56, 剪枝次数: 11

Minimax    H=4 结果: {'best_target': 'T3', 'best_value': 5}

Minimax    H=4 访问节点数: 64

- **已知限制**: 题目四的收益评估采用了标准的严格扣除双方移动代价的方式，与参考值存在微小数值偏差，但最优策略选择完全一致。