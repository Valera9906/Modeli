"""
АНИМАЦИЯ МОДЕЛИ ТРАНСПОРТНОГО ПОТОКА
Визуализация движения автомобилей по дороге
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class TrafficModel:
    def __init__(self, size=200, density=0.6, max_speed=5, slowdown_prob=0.3):
        self.size = size
        self.density = density
        self.max_speed = max_speed
        self.slowdown_prob = slowdown_prob

        self.positions = []
        self.speeds = []

        for i in range(size):
            if random.random() < density:
                self.positions.append(i)
                self.speeds.append(random.randint(1, max_speed))

        self.positions.sort()

    def update(self):
        n_cars = len(self.positions)
        if n_cars == 0:
            return 0

        new_positions = []
        new_speeds = []

        for i in range(n_cars):
            if i < n_cars - 1:
                distance = (self.positions[i + 1] - self.positions[i] - 1) % self.size
            else:
                distance = (self.positions[0] + self.size - self.positions[i] - 1) % self.size

            speed = min(self.speeds[i] + 1, self.max_speed)
            speed = min(speed, distance)

            if speed > 0 and random.random() < self.slowdown_prob:
                speed -= 1

            new_pos = (self.positions[i] + speed) % self.size
            new_positions.append(new_pos)
            new_speeds.append(speed)

        for i in range(n_cars):
            for j in range(i + 1, n_cars):
                if new_positions[i] == new_positions[j]:
                    new_positions[j] = (new_positions[j] + 1) % self.size

        self.positions = new_positions
        self.speeds = new_speeds

        avg_speed = sum(self.speeds) / n_cars if n_cars > 0 else 0
        return avg_speed

    def get_grid(self):
        grid = np.zeros(self.size)
        for pos in self.positions:
            grid[pos] = 1
        return grid


print("=" * 60)
print("АНИМАЦИЯ: Модель транспортного потока")
print("=" * 60)
print("Синие полоски = автомобили")
print("Пустое пространство = свободная дорога")
print("\nЗакройте окно, чтобы завершить программу")

# Создаём модель с высокой плотностью (чтобы увидеть пробки)
model = TrafficModel(size=200, density=0.65, max_speed=5, slowdown_prob=0.3)

fig, ax = plt.subplots(figsize=(12, 4))


def animate(frame):
    if frame < 300:
        avg_speed = model.update()

    grid = model.get_grid()

    ax.clear()
    # Рисуем дорогу
    ax.bar(range(len(grid)), grid, color='blue', width=1.0)
    ax.set_xlim(0, len(grid))
    ax.set_ylim(0, 1.5)
    ax.set_title(f'Транспортный поток - Шаг {frame}', fontsize=14)
    ax.set_xlabel('Позиция на дороге')
    ax.set_ylabel('Автомобили')

    # Статистика
    n_cars = len(model.positions)
    avg_speed = sum(model.speeds) / n_cars if n_cars > 0 else 0

    info_text = f'Автомобилей: {n_cars} | Средняя скорость: {avg_speed:.2f}'
    ax.text(0.02, 0.95, info_text, transform=ax.transAxes, fontsize=12,
            bbox=dict(facecolor='white', alpha=0.8))

    return []


print("\nСоздание анимации...")
anim = animation.FuncAnimation(fig, animate, frames=350, interval=50, repeat=False)
plt.show()

print("\n✅ Анимация завершена!")
print("Вы наблюдали, как при высокой плотности возникают пробки")