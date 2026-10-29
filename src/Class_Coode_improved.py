
# Lab 2 (Improved): Path finding for Super Mario Bros Project
# Algorithms: BFS, DFS, and A*

import numpy as np
import matplotlib.pyplot as plt
import heapq
from collections import deque

# --- 1. Setup the Mario Map ---
ROWS, COLS = 5, 10          # A smaller map tailored for our Mario project
START = (4, 0)              # Mario starts at bottom-left
GOAL = (0, 9)               # Flag is at top-right
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right

# Creating a custom map for Mario
# 0 = Empty path, 1 = Wall/Enemy
grid = np.zeros((ROWS, COLS))
# Add some obstacles (walls/enemies)
grid[1, 2] = 1
grid[2, 2] = 1
grid[3, 2] = 1
grid[2, 5] = 1
grid[1, 5] = 1
grid[3, 7] = 1

grid[START] = 0
grid[GOAL] = 0

plt.imshow(grid, cmap="Greys")
plt.title("Mario Map (black = Wall/Enemy)")
plt.show()

# --- 2. BFS and DFS ---
def blind_search(grid, start, goal, mode):
    frontier = deque([start])
    came_from = {start: None}
    expanded = []
    
    while frontier:
        if mode == "bfs":
            cell = frontier.popleft()
        else:
            cell = frontier.pop()
            
        expanded.append(cell)
        if cell == goal:
            break
            
        for dr, dc in MOVES:
            nxt = (cell[0] + dr, cell[1] + dc)
            inside = 0 <= nxt[0] < ROWS and 0 <= nxt[1] < COLS
            if inside and grid[nxt] == 0 and nxt not in came_from:
                came_from[nxt] = cell
                frontier.append(nxt)
                
    if goal not in came_from:
        return None, expanded
        
    path = []
    cell = goal
    while cell is not None:
        path.append(cell)
        cell = came_from[cell]
    return path[::-1], expanded

# --- 3. A* ---
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    heap = [(manhattan(start, goal), 0, start)]
    came_from = {start: None}
    best_g = {start: 0}
    expanded = []
    closed = set()
    
    while heap:
        f, g, cell = heapq.heappop(heap)
        if cell in closed:
            continue
        closed.add(cell)
        expanded.append(cell)
        if cell == goal:
            break
            
        for dr, dc in MOVES:
            nxt = (cell[0] + dr, cell[1] + dc)
            inside = 0 <= nxt[0] < ROWS and 0 <= nxt[1] < COLS
            if inside and grid[nxt] == 0:
                new_g = g + 1
                if nxt not in best_g or new_g < best_g[nxt]:
                    best_g[nxt] = new_g
                    came_from[nxt] = cell
                    heapq.heappush(heap, (new_g + manhattan(nxt, goal), new_g, nxt))
                    
    if goal not in came_from:
        return None, expanded
        
    path = []
    cell = goal
    while cell is not None:
        path.append(cell)
        cell = came_from[cell]
    return path[::-1], expanded

# --- 4. Run Algorithms ---
results = {}
for name in ["bfs", "dfs", "astar"]:
    if name == "astar":
        path, expanded = astar(grid, START, GOAL)
    else:
        path, expanded = blind_search(grid, START, GOAL, name)
    results[name] = (path, expanded)
    print(f"{name:6s} path length = {len(path) - 1:3d}   expanded cells = {len(expanded):3d}")

# --- 5. Visualizing the results for Mario ---
fig, axes = plt.subplots(1, 3, figsize=(12, 3))
for ax, name in zip(axes, ["bfs", "dfs", "astar"]):
    path, expanded = results[name]
    picture = grid.astype(float)
    
    for cell in expanded:
        picture[cell] = 0.4    # Explored cells
    for cell in path:
        picture[cell] = 0.8    # Final path
        
    # Custom colors: 0=White, 1=Black(walls), 0.4=Blue(expanded), 0.8=Yellow(path)
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["white", "black", "#93c5fd", "#f59e0b"])
    
    ax.imshow(picture, cmap=cmap)
    ax.set_title(f"{name}: steps {len(path) - 1}, explored {len(expanded)}")
    ax.axis("off")
plt.show()

# Note: I removed the 100-map loop and animation parts to keep the code clean 
# and focused on demonstrating the core logic for our specific Mario map.
