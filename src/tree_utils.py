class TreeNode:
    def __init__(self, value=None, children=None, is_maximizing_player=False):
        self.value = value
        self.children = children if children is not None else []
        self.is_maximizing_player = is_maximizing_player

def build_test_tree():
    """构建题目三的测试树"""
    leaf1 = TreeNode(value=3)
    leaf2 = TreeNode(value=5)
    leaf3 = TreeNode(value=6)
    leaf4 = TreeNode(value=9)
    leaf5 = TreeNode(value=1)
    leaf6 = TreeNode(value=2)
    
    max1 = TreeNode(children=[leaf1, leaf2], is_maximizing_player=True)
    max2 = TreeNode(children=[leaf3, leaf4], is_maximizing_player=True)
    max3 = TreeNode(children=[leaf5, leaf6], is_maximizing_player=True)
    
    min1 = TreeNode(children=[max1, max2], is_maximizing_player=False)
    min2 = TreeNode(children=[max2, max3], is_maximizing_player=False)
    
    root = TreeNode(children=[min1, min2], is_maximizing_player=True)
    return root