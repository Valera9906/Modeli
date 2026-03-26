"""
АНИМАЦИЯ МОДЕЛИ ЛЕСНЫХ ПОЖАРОВ
Визуализация поля: зелёные - деревья, красные - огонь, коричневые - пепелище
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import random

class ForestFireModel:
    def __init__(self, size=100, tree_density=0.8, lightning_prob=0.0005):
        self.size = size
        self.tree_density = tree_density
        self.lightning_prob = lightning_prob

        self.grid = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                if random.random() < tree_density:
                    self.grid[i, j] = 1  # дерево

        center = size // 2
        self.grid[center, center] = 2  # огонь

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append((nx, ny))
        return neighbors

    def update(self):
        new_grid = self.grid.copy()

        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == 2:  # огонь
                    new_grid[i, j] = 0  # становится пеплом
                    for ni, nj in self.get_neighbors(i, j):
                        if self.grid[ni, nj] == 1:  # дерево
                            new_grid[ni, nj] = 2  # загорается

        # Случайная молния
        if random.random() < self.lightning_prob:
            i, j = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if new_grid[i, j] == 1:
                new_grid[i, j] = 2

        self.grid = new_grid
        return self.grid


print("=" * 60)
print("АНИМАЦИЯ: Модель лесных пожаров")
print("=" * 60)
print("Зелёный = дерево")
print("Красный = огонь")
print("Коричневый = пепелище")
print("\nЗакройте окно, чтобы завершить программу")

# Создаём модель
model = ForestFireModel(size=100, tree_density=0.8, lightning_prob=0.0005)

# Цвета: 0 - пепел (коричневый), 1 - дерево (зелёный), 2 - огонь (красный)
cmap = ListedColormap(['#8B5A2B', '#228B22', '#FF4500'])

fig, ax = plt.subplots(figsize=(8, 8))

def animate(frame):
    if frame < 200:
        model.update()

    ax.clear()
    ax.imshow(model.grid, cmap=cmap, interpolation='nearest')
    ax.set_title(f'Лесной пожар - Шаг {frame}', fontsize=14)
    ax.axis('off')

    # Статистика
    trees = np.sum(model.grid == 1)
    fire = np.sum(model.grid == 2)
    ash = np.sum(model.grid == 0)

    stats_text = f'Деревья: {trees} | Огонь: {fire} | Пепел: {ash}'
    ax.text(10, 10, stats_text, color='white', fontsize=10,
            bbox=dict(facecolor='black', alpha=0.7))

    return []

print("\nСоздание анимации...")
anim = animation.FuncAnimation(fig, animate, frames=250, interval=80, repeat=False)
plt.show()

print("\n✅ Анимация завершена!")
print("Вы наблюдали, как огонь распространяется по лесу")