"""
АНИМАЦИЯ МОДЕЛИ ЭПИДЕМИИ SIR
Визуализация поля клеток: зелёные - здоровые, красные - больные, серые - выздоровевшие
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import random

class EpidemicModel:
    def __init__(self, size=100, density=0.5, infection_prob=0.3, recovery_time=8):
        self.size = size
        self.density = density
        self.infection_prob = infection_prob
        self.recovery_time = recovery_time

        self.grid = np.zeros((size, size), dtype=int)
        self.recovery_counter = np.zeros((size, size), dtype=int)

        for i in range(size):
            for j in range(size):
                if random.random() < density:
                    self.grid[i, j] = 0  # здоров
                else:
                    self.grid[i, j] = -1  # пусто

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

    def update(self):
        new_grid = self.grid.copy()
        new_counter = self.recovery_counter.copy()

        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == 1:
                    new_counter[i, j] = self.recovery_counter[i, j] - 1
                    if new_counter[i, j] <= 0:
                        new_grid[i, j] = 2

                elif self.grid[i, j] == 0:
                    neighbors = self.get_neighbors(i, j)
                    infected_neighbors = sum(1 for n in neighbors if n == 1)
                    if infected_neighbors > 0:
                        infection_chance = 1 - (1 - self.infection_prob) ** infected_neighbors
                        if random.random() < infection_chance:
                            new_grid[i, j] = 1
                            new_counter[i, j] = self.recovery_time

        self.grid = new_grid
        self.recovery_counter = new_counter
        return self.grid


print("=" * 60)
print("АНИМАЦИЯ: Модель эпидемии SIR")
print("=" * 60)
print("Зелёный = здоровый")
print("Красный = больной")
print("Серый = выздоровевший")
print("Чёрный = пусто")
print("\nЗакройте окно, чтобы завершить программу")

# Создаём модель
model = EpidemicModel(size=100, density=0.6, infection_prob=0.3, recovery_time=8)

# Настройка цветов
cmap = ListedColormap(['lightgreen', 'red', 'gray', 'black'])
# 0 - здоров (lightgreen), 1 - болен (red), 2 - выздоровел (gray), -1 - пусто (black)

fig, ax = plt.subplots(figsize=(8, 8))

def animate(frame):
    if frame < 200:
        model.update()

    # Преобразуем -1 в 3 для отображения
    display_grid = model.grid.copy()
    display_grid[display_grid == -1] = 3

    ax.clear()
    ax.imshow(display_grid, cmap=cmap, interpolation='nearest')
    ax.set_title(f'Эпидемия SIR - Шаг {frame}', fontsize=14)
    ax.axis('off')

    # Статистика
    healthy = np.sum(model.grid == 0)
    infected = np.sum(model.grid == 1)
    recovered = np.sum(model.grid == 2)
    empty = np.sum(model.grid == -1)

    stats_text = f'Здоровые: {healthy} | Больные: {infected} | Выздоровевшие: {recovered}'
    ax.text(10, 10, stats_text, color='white', fontsize=10,
            bbox=dict(facecolor='black', alpha=0.7))

print("\nСоздание анимации...")
anim = animation.FuncAnimation(fig, animate, frames=250, interval=100, repeat=False)
plt.show()

print("\n✅ Анимация завершена!")
print("Вы наблюдали, как инфекция распространяется от центра")