from tree_utils import build_test_tree
def alpha_beta(node, alpha, beta, is_maximizing, stats):
    stats['visited'] += 1
    if not node.children:
        return node.value
    if is_maximizing:
        max_eval = float('-inf')
        for child in node.children:
            eval = alpha_beta(child, alpha, beta, False, stats)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                stats['pruned'] += 1
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child in node.children:
            eval = alpha_beta(child, alpha, beta, True, stats)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                stats['pruned'] += 1
                break
        return min_eval

if __name__ == "__main__":
    print("题目三：Alpha-Beta剪枝")
    root = build_test_tree()
    stats = {'visited': 0, 'pruned': 0}
    result = alpha_beta(root, float('-inf'), float('inf'), True, stats)
    print(f"最佳得分: {result}")
    print(f"访问节点数: {stats['visited']}, 剪枝次数: {stats['pruned']}")