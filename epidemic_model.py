import numpy as np
import random

class EpidemicModel:
    def __init__(self, size=100, density=0.5, infection_prob=0.3, recovery_time=8):
        self.size = size
        self.density = density
        self.infection_prob = infection_prob
        self.recovery_time = recovery_time

        # 0 - здоров, 1 - болен, 2 - выздоровел, 3 - пусто (сделали 3 вместо -1 для турбо-режима)
        self.grid = np.full((size, size), 3, dtype=int)
        self.recovery_counter = np.zeros((size, size), dtype=int)

        # Расставляем здоровых людей
        for i in range(size):
            for j in range(size):
                if random.random() < density:
                    self.grid[i, j] = 0  

        # Создаем очаг заражения в центре
        center = size // 2
        for i in range(-3, 4):
            for j in range(-3, 4):
                if 0 <= center + i < size and 0 <= center + j < size:
                    self.grid[center + i, center + j] = 1
                    self.recovery_counter[center + i, center + j] = recovery_time

    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    neighbors.append(self.grid[nx, ny])
        return neighbors

    def update(self, inf_prob=None):
        # Эта строчка позволяет менять вероятность прямо с ползунка Streamlit
        if inf_prob is not None:
            self.infection_prob = inf_prob
            
        new_grid = self.grid.copy()
        new_counter = self.recovery_counter.copy()

        for i in range(self.size):
            for j in range(self.size):
                # Если человек болен, уменьшаем счетчик болезни
                if self.grid[i, j] == 1:
                    new_counter[i, j] = self.recovery_counter[i, j] - 1
                    if new_counter[i, j] <= 0:
                        new_grid[i, j] = 2 # Выздоравливает

                # Если человек здоров, проверяем соседей
                elif self.grid[i, j] == 0:
                    neighbors = self.get_neighbors(i, j)
                    infected_neighbors = sum(1 for n in neighbors if n == 1)
                    if infected_neighbors > 0:
                        infection_chance = 1 - (1 - self.infection_prob) ** infected_neighbors
                        if random.random() < infection_chance:
                            new_grid[i, j] = 1 # Заражается
                            new_counter[i, j] = self.recovery_time

        self.grid = new_grid
        self.recovery_counter = new_counter
        return self.grid
