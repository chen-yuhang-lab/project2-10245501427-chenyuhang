import sys
import os
import random
import matplotlib.pyplot as plt
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_dir not in sys.path:
    sys.path.append(src_dir)
from src.astar import a_star_search
from src.tree_utils import TreeNode, build_test_tree
from src.minimax import alpha_beta
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'figures')
os.makedirs(OUT_DIR, exist_ok=True)
def generate_random_maze(size, obstacle_prob=0.2):
    """生成随机迷宫用于对照实验"""
    maze = [[' ' for _ in range(size)] for _ in range(size)]
    for r in range(size):
        for c in range(size):
            if (r, c) != (0, 0) and (r, c) != (size-1, size-1):
                if random.random() < obstacle_prob:
                    maze[r][c] = 'X'
    maze[0][0] = 'S'
    maze[size-1][size-1] = 'E'
    return maze
def exp1_astar_heuristics():
    """对比h=0与曼哈顿距离的搜索节点数"""
    sizes = [5, 10, 15, 20]
    manhattan_nodes = []
    zero_nodes = []
    for size in sizes:
        random.seed(42) #固定随机种子
        maze = generate_random_maze(size)
        goal = (size-1, size-1)
        _, nodes_h0 = a_star_search((0,0), goal, maze, heuristic_type="zero")
        _, nodes_h_man = a_star_search((0,0), goal, maze, heuristic_type="manhattan")
        zero_nodes.append(nodes_h0)
        manhattan_nodes.append(nodes_h_man)
        print(f"迷宫大小 {size}x{size}: h=0 访问 {nodes_h0} 节点, h=Manhattan 访问 {nodes_h_man} 节点")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, zero_nodes, marker='o', label='h=0 (Dijkstra)')
    plt.plot(sizes, manhattan_nodes, marker='s', label='h=Manhattan')
    plt.xlabel('迷宫边长')
    plt.ylabel('访问节点数')
    plt.title('启发函数对 A* 搜索节点数的影响')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(OUT_DIR, 'exp1_heuristic_comparison.png'))
    plt.close()
    print("已生成图表: exp1_heuristic_comparison.png\n")

def create_tree_with_order(order_list):
    """根据指定的叶子节点顺序构建题目三的树"""
    leaves = [TreeNode(value=v) for v in order_list]
    max1 = TreeNode(children=[leaves[0], leaves[1]], is_maximizing_player=True)
    max2 = TreeNode(children=[leaves[2], leaves[3]], is_maximizing_player=True)
    max3 = TreeNode(children=[leaves[4], leaves[5]], is_maximizing_player=True)
    min1 = TreeNode(children=[max1, max2], is_maximizing_player=False)
    min2 = TreeNode(children=[max2, max3], is_maximizing_player=False)
    return TreeNode(children=[min1, min2], is_maximizing_player=True)
def exp2_pruning_order():
    """比较不同访问顺序的搜索开销"""
    original_order = [3, 5, 6, 9, 1, 2]
    #最优顺序
    sorted_order = sorted(original_order)
    
    results = {}
    
    for name, order in [("Original", original_order), ("Sorted", sorted_order)]:
        root = create_tree_with_order(order)
        stats = {'visited': 0, 'pruned': 0}
        val = alpha_beta(root, float('-inf'), float('inf'), True, stats)
        results[name] = {'value': val, 'visited': stats['visited'], 'pruned': stats['pruned']}
        print(f"顺序 {name}: 最佳得分={val}, 访问节点数={stats['visited']}, 剪枝次数={stats['pruned']}")

    #绘制柱状图
    labels = ['Original Order', 'Sorted Order']
    visited = [results['Original']['visited'], results['Sorted']['visited']]
    pruned = [results['Original']['pruned'], results['Sorted']['pruned']]
    x = range(len(labels))
    plt.figure(figsize=(8, 5))
    plt.bar([i - 0.2 for i in x], visited, width=0.4, label='Visited Nodes', color='skyblue')
    plt.bar([i + 0.2 for i in x], pruned, width=0.4, label='Pruned Branches', color='salmon')
    plt.xticks(x, labels)
    plt.ylabel('Count')
    plt.title('Alpha-Beta剪枝：不同访问顺序的效率对比')
    plt.legend()
    plt.savefig(os.path.join(OUT_DIR, 'exp2_pruning_efficiency.png'))
    plt.close()
    print("已生成图表: exp2_pruning_efficiency.png\n")

def main():
    print("开始运行对照实验\n")
    print("实验1：A* 启发函数对比")
    exp1_astar_heuristics()
    print("实验2：Alpha-Beta剪枝顺序对比")
    exp2_pruning_order()

if __name__ == "__main__":
    main()