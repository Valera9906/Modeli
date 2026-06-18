import numpy as np
import random

class ForestFireModel:
    def __init__(self, size=60, tree_density=0.7):
        self.size = size
        # 0 - это пустая земля
        self.grid = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                if random.random() < tree_density:
                    self.grid[i, j] = 1  # 1 - живое дерево
        self.grid[size // 2, size // 2] = 2  # 2 - огонь в центре

    def update(self):
        new_grid = self.grid.copy()
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == 2:
                    new_grid[i, j] = 3  # 3 - пепелище
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            if self.grid[nx, ny] == 1:
                                new_grid[nx, ny] = 2
        self.grid = new_grid
