import copy
from astar import a_star_search
TREASURE_MAP = [
    ['A', 1, 1, 'X', 2, 1, 'T'],
    [1, 1, 'X', 6, 'X', 1, 'X'],
    [1, 2, 'T', 1, 1, 1, 3],
    ['X', 1, 'X', 8, 'X', 1, 'X'],
    [4, 1, 1, 1, 'T', 3, 1],
    [1, 5, 1, 'X', 9, 'X', 1],
    ['T', 1, 1, 'X', 1, 1, 'B']
]

TREASURE_VALUES = {'T1': 9, 'T2': 6, 'T3': 7, 'T4': 7}
TREASURE_POS = {'T1': (0, 6), 'T2': (2, 2), 'T3': (4, 4), 'T4': (6, 0)}
A_START = (0, 0)
B_START = (6, 6)
#计算距离矩阵
def compute_distance_matrix():
    points = {'A': A_START, 'B': B_START, **TREASURE_POS}
    matrix = {}
    for p1_name, p1_pos in points.items():
        matrix[p1_name] = {}
        for p2_name, p2_pos in points.items():
            if p1_name == p2_name:
                matrix[p1_name][p2_name] = 0
            else:
                grid_copy = copy.deepcopy(TREASURE_MAP)
                r, c = p2_pos
                grid_copy[r][c] = 'E'  # 将终点视为 E，代价为0
                cost, _ = a_star_search(p1_pos, p2_pos, grid_copy, is_weighted=True)
                matrix[p1_name][p2_name] = cost
    return matrix

class GameState:
    def __init__(self, a_pos, b_pos, remaining, score_a, score_b, is_a_turn):
        self.a_pos = a_pos
        self.b_pos = b_pos
        self.remaining = remaining
        self.score_a = score_a
        self.score_b = score_b
        self.is_a_turn = is_a_turn

#核心搜索函数（通过传入的alpha/beta自动适配Minimax或Alpha-Beta）
def minimax_alpha_beta(state, depth, alpha, beta, matrix, stats):
    stats['visited'] += 1
    #终止条件：深度为0或宝藏取完
    if depth == 0 or not state.remaining:
        return state.score_a - state.score_b
    if state.is_a_turn:
        max_eval = float('-inf')
        for target in list(state.remaining):
            v = TREASURE_VALUES[target]
            current_a_pos = A_START if state.a_pos == 'A' else state.a_pos
            d = matrix[current_a_pos][target] if current_a_pos in matrix else matrix['A'][target]
            gain = v - d
            new_remaining = tuple([t for t in state.remaining if t != target])
            new_state = GameState(target, state.b_pos, new_remaining, 
                                  state.score_a + gain, state.score_b, False)
            
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, matrix, stats)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            #剪枝条件
            if beta <= alpha:
                stats['pruned'] += 1
                break
        return max_eval
    else:
        min_eval = float('inf')
        for target in list(state.remaining):
            v = TREASURE_VALUES[target]
            current_b_pos = B_START if state.b_pos == 'B' else state.b_pos
            d = matrix[current_b_pos][target] if current_b_pos in matrix else matrix['B'][target]
            
            gain = v - d
            new_remaining = tuple([t for t in state.remaining if t != target])
            new_state = GameState(state.a_pos, target, new_remaining, 
                                  state.score_a, state.score_b + gain, True)
            
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, matrix, stats)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            
            #剪枝条件
            if beta <= alpha:
                stats['pruned'] += 1
                break
        return min_eval
def solve_problem4(depth, use_pruning=True):
    matrix = compute_distance_matrix()
    initial_state = GameState(A_START, B_START, tuple(TREASURE_VALUES.keys()), 0, 0, True)
    stats = {'visited': 0, 'pruned': 0}
    
    best_target = None
    best_value = float('-inf')
    
    for target in initial_state.remaining:
        v = TREASURE_VALUES[target]
        d = matrix['A'][target]
        gain = v - d
        new_remaining = tuple([t for t in initial_state.remaining if t != target])
        new_state = GameState(target, B_START, new_remaining, gain, 0, False)
        
        if use_pruning:
            val = minimax_alpha_beta(new_state, depth - 1, float('-inf'), float('inf'), matrix, stats)
        else:
            val = minimax_alpha_beta(new_state, depth - 1, float('-inf'), float('inf'), matrix, stats)
            
        if val > best_value:
            best_value = val
            best_target = target
            
    return matrix, {"best_target": best_target, "best_value": best_value}, stats


if __name__ == "__main__":
    print("题目四：竞争环境下的宝藏分配")
    #打印6x6距离矩阵
    matrix, _, _ = solve_problem4(2, use_pruning=True) 
    print("6x6 距离矩阵:")
    keys = ['A', 'B', 'T1', 'T2', 'T3', 'T4']
    print("\t" + "\t".join(keys))
    for k1 in keys:
        row = [str(matrix[k1][k2]) for k2 in keys]
        print(f"{k1}\t" + "\t".join(row))
    for depth in [2, 4]:
        #Alpha-Beta剪枝
        _, ab_res, ab_stats = solve_problem4(depth, use_pruning=True)
        print(f"Alpha-Beta H={depth} 结果: {ab_res}")
        print(f"Alpha-Beta H={depth} 访问节点数: {ab_stats['visited']}, 剪枝次数: {ab_stats['pruned']}")
        # 纯Minimax（禁用剪枝）
        def pure_minimax(state, depth, matrix, stats):
            stats['visited'] += 1
            if depth == 0 or not state.remaining:
                return state.score_a - state.score_b
            
            if state.is_a_turn:
                max_eval = float('-inf')
                for target in state.remaining:
                    v = TREASURE_VALUES[target]
                    d = matrix['A'][target]
                    gain = v - d
                    new_rem = tuple([t for t in state.remaining if t != target])
                    eval = pure_minimax(GameState(target, state.b_pos, new_rem, state.score_a + gain, state.score_b, False), depth-1, matrix, stats)
                    max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = float('inf')
                for target in state.remaining:
                    v = TREASURE_VALUES[target]
                    d = matrix['B'][target]
                    gain = v - d
                    new_rem = tuple([t for t in state.remaining if t != target])
                    eval = pure_minimax(GameState(state.a_pos, target, new_rem, state.score_a, state.score_b + gain, True), depth-1, matrix, stats)
                    min_eval = min(min_eval, eval)
                return min_eval

        initial_state = GameState(A_START, B_START, tuple(TREASURE_VALUES.keys()), 0, 0, True)
        mm_stats = {'visited': 0, 'pruned': 0}
        mm_best_target = None
        mm_best_value = float('-inf')
        for target in initial_state.remaining:
            v = TREASURE_VALUES[target]
            d = matrix['A'][target]
            gain = v - d
            new_rem = tuple([t for t in initial_state.remaining if t != target])
            val = pure_minimax(GameState(target, B_START, new_rem, gain, 0, False), depth-1, matrix, mm_stats)
            if val > mm_best_value:
                mm_best_value = val
                mm_best_target = target
                
        print(f"Minimax    H={depth} 结果: {{'best_target': '{mm_best_target}', 'best_value': {mm_best_value}}}")
        print(f"Minimax    H={depth} 访问节点数: {mm_stats['visited']}")