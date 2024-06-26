import numpy as np
import heapq

def is_valid(row, col, ROW, COL):
    """
    Check if a cell is valid by checking if it is within the grid boundaries.

    Args:
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        ROW (int): The total number of rows in the grid.
        COL (int): The total number of columns in the grid.

    Returns:
        bool: True if the cell is valid, False otherwise.
    """
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

def a_star_search(grid, src, dest):
    """
    Perform A* search from source to destination in the grid.

    Args:
        grid (np.array): 2D numpy array representing the grid.
        src (tuple): A tuple representing the source coordinates.
        dest (tuple): A tuple representing the destination coordinates.

    Returns:
        list: A list of tuples representing the path from source to destination.
              Each tuple is a pair of (row, col) coordinates. If no path is found, returns an empty list.
    """
    # Check if source and destination are not blocked
    if grid[src[0]][src[1]] == 1:
        print("Source is blocked")
        return []
    if grid[dest[0]][dest[1]] == 1:
        print("Destination is blocked")
        return []

    ROW, COL = grid.shape
    print(f"ROW: {ROW}, COL: {COL}")
    print(f"src: {src}, dest: {dest}")

    # Define the 8 possible directions to move on the grid
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Initialize the details of each cell
    cell_details = {(i, j): {'f': float('inf'), 'g': float('inf'), 'h': 0, 'parent': None} for i in range(ROW) for j in range(COL)}

    # Initialize the source cell details
    cell_details[src]['f'] = cell_details[src]['g'] = 0

    # Initialize the open list with the source cell
    open_list = [(0.0, src)]

    # Initialize the closed list to keep track of visited cells
    closed_list = np.zeros((ROW, COL), dtype=bool)

    # Start the A* search
    while open_list:
        _, (i, j) = heapq.heappop(open_list)
        closed_list[i][j] = True

        # Explore all the neighboring cells
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