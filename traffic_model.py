import numpy as np
import random

class TrafficModel:
    def __init__(self, size=200, density=0.6, max_speed=5, slowdown_prob=0.3):
        self.size = size
        self.density = density
        self.max_speed = max_speed
        self.slowdown_prob = slowdown_prob

        positions = []
        speeds = []

        # Расставляем машины
        for i in range(size):
            if random.random() < density:
                positions.append(i)
                speeds.append(random.randint(1, max_speed))

        # Переводим в быстрые массивы numpy для Streamlit
        self.positions = np.array(positions)
        self.speeds = np.array(speeds)

        # Сортируем машины по порядку на дороге
        sort_idx = np.argsort(self.positions)
        self.positions = self.positions[sort_idx]
        self.speeds = self.speeds[sort_idx]

    def update(self):
        n_cars = len(self.positions)
        if n_cars == 0:
            return 0

        new_positions = []
        new_speeds = []

        # Высчитываем движение для каждой машины
        for i in range(n_cars):
            # Ищем дистанцию до следующей машины
            if i < n_cars - 1:
                distance = (self.positions[i + 1] - self.positions[i] - 1) % self.size
            else:
                distance = (self.positions[0] + self.size - self.positions[i] - 1) % self.size

            # 1. Ускорение
            speed = min(self.speeds[i] + 1, self.max_speed)
            # 2. Торможение (чтобы не врезаться)
            speed = min(speed, distance)

            # 3. Случайность (человеческий фактор)
            if speed > 0 and random.random() < self.slowdown_prob:
                speed -= 1

            # 4. Движение
            new_pos = (self.positions[i] + speed) % self.size
            new_positions.append(new_pos)
            new_speeds.append(speed)

        # Проверка на случайные коллизии
        for i in range(n_cars):
            for j in range(i + 1, n_cars):
                if new_positions[i] == new_positions[j]:
                    new_positions[j] = (new_positions[j] + 1) % self.size

        # Сохраняем новые позиции и скорости
        self.positions = np.array(new_positions)
        self.speeds = np.array(new_speeds)

        # Снова сортируем, чтобы не нарушать порядок
        sort_idx = np.argsort(self.positions)
        self.positions = self.positions[sort_idx]
        self.speeds = self.speeds[sort_idx]

        # Возвращаем среднюю скорость потока
        avg_speed = np.mean(self.speeds) if n_cars > 0 else 0
        return avg_speed
