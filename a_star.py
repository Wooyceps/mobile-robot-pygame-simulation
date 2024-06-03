import numpy as np
import heapq

def is_valid(row, col, ROW, COL):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

def a_star_search(grid, src, dest):
    ROW, COL = grid.shape
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    cell_details = {(i, j): {'f': float('inf'), 'g': float('inf'), 'h': 0, 'parent': None} for i in range(ROW) for j in range(COL)}
    cell_details[src]['f'] = cell_details[src]['g'] = 0
    open_list = [(0.0, src)]
    closed_list = np.zeros((ROW, COL), dtype=bool)

    while open_list:
        _, (i, j) = heapq.heappop(open_list)
        closed_list[i][j] = True

        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]
            if is_valid(new_i, new_j, ROW, COL) and grid[new_i][new_j] == 0 and not closed_list[new_i][new_j]:
                if (new_i, new_j) == dest:
                    cell_details[(new_i, new_j)]['parent'] = (i, j)
                    print("The destination cell is found")
                    path = []
                    while cell_details[(new_i, new_j)]['parent']:
                        path.append((new_i, new_j))
                        new_i, new_j = cell_details[(new_i, new_j)]['parent']
                    return path[::-1]
                else:
                    g_new = cell_details[(i, j)]['g'] + 1.0
                    h_new = ((new_i - dest[0]) ** 2 + (new_j - dest[1]) ** 2) ** 0.5
                    f_new = g_new + h_new
                    if cell_details[(new_i, new_j)]['f'] > f_new:
                        heapq.heappush(open_list, (f_new, (new_i, new_j)))
                        cell_details[(new_i, new_j)] = {'f': f_new, 'g': g_new, 'h': h_new, 'parent': (i, j)}

    print("Failed to find the destination cell")
    return []