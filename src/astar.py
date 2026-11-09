import heapq
def a_star_search(start, goal, grid, is_weighted=False, heuristic_type="manhattan"):
    rows, cols = len(grid), len(grid[0])
    
    def heuristic(r, c):
        if heuristic_type == "zero":
            return 0
        return abs(r - goal[0]) + abs(c - goal[1])
    open_list = [(heuristic(start[0], start[1]), 0, start[0], start[1], [start])]
    g_costs = {start: 0}
    visited_nodes = 0 
    while open_list:
        f, g, r, c, path = heapq.heappop(open_list)
        visited_nodes += 1
        if (r, c) == goal:
            if is_weighted:
                return g, visited_nodes
            return path, visited_nodes
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'X':
                if is_weighted:
                    if (nr, nc) == goal and grid[nr][nc] == 'E':
                        step_cost = 0
                    elif grid[nr][nc] in ['A', 'B', 'T', 'S']:
                        step_cost = 1
                    else:
                        step_cost = int(grid[nr][nc])
                else:
                    step_cost = 1
                new_g = g + step_cost
                
                if (nr, nc) not in g_costs or new_g < g_costs[(nr, nc)]:
                    g_costs[(nr, nc)] = new_g
                    new_f = new_g + heuristic(nr, nc)
                    heapq.heappush(open_list, (new_f, new_g, nr, nc, path + [(nr, nc)]))
                    
    return (-1, visited_nodes) if is_weighted else ([], visited_nodes)

if __name__ == "__main__":
    print("题目一：迷宫寻路")
    maze = [
        ['S', ' ', ' ', 'X', ' '],
        [' ', 'X', ' ', ' ', ' '],
        [' ', 'X', ' ', ' ', ' '],
        [' ', 'X', ' ', ' ', ' '],
        [' ', 'X', ' ', ' ', ' ']
    ]
    path, _ = a_star_search((0,0), (3,4), maze)
    print(f"路径: {path}")
    
    print("\n题目二：加权地形")
    weighted_grid = [
        [5, 1, 1, 8, 1],
        [1, 8, 3, 1, 1],
        [1, 8, 1, 8, 1],
        [1, 1, 1, 8, 1],
        [8, 8, 1, 1, 'E']
    ]
    cost, _ = a_star_search((0,0), (4,4), weighted_grid, is_weighted=True)
    print(f"最小总代价: {cost}")