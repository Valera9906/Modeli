import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
import time

# --- НАСТРОЙКИ СТРАНИЦЫ И СТИЛИЗАЦИЯ ---
st.set_page_config(page_title="Моделирование сложных систем", layout="wide", initial_sidebar_state="expanded")

# Кастомный CSS для темной темы и компактности
st.markdown("""
    <style>
    .stApp { background-color: #1e1e1e; color: #ffffff; }
    .sidebar .sidebar-content { background-color: #2d2d2d; }
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    h1 { margin-bottom: 0rem; padding-bottom: 10px; color: #00d4ff !important; font-size: 2.2rem; }
    .stSlider > div > div > div > div { color: #00d4ff; }
    .stButton>button { 
        width: 100%; 
        background-color: #00d4ff; 
        color: #1e1e1e; 
        font-weight: bold; 
        border: none; 
        padding: 12px;
        margin-top: 15px;
        font-size: 1.1rem;
    }
    .stButton>button:hover { background-color: #00a3cc; color: white; }
    .legend-box { 
        padding: 10px; 
        border-radius: 5px; 
        border: 1px solid #444; 
        margin-bottom: 15px; 
        text-align: center; 
        font-size: 1.1em; 
        background-color: #2a2a2a;
    }
    </style>
    """, unsafe_allow_html=True)


# --- КЛАССЫ МОДЕЛЕЙ ---

class EpidemicModel:
    def __init__(self, size=60, density=0.5):
        self.size = size
        # 3 - это пустое пространство
        self.grid = np.full((size, size), 3, dtype=int)
        self.recovery_counter = np.zeros((size, size), dtype=int)

        for i in range(size):
            for j in range(size):
                if random.random() < density:
                    self.grid[i, j] = 0  # 0 - здоровый человек

        # Очаг заражения (1 - больной)
        center = size // 2
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= center + i < size and 0 <= center + j < size:
                    self.grid[center + i, center + j] = 1
                    self.recovery_counter[center + i, center + j] = 8

    def update(self, infection_prob):
        new_grid = self.grid.copy()
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == 1:
                    self.recovery_counter[i, j] -= 1
                    if self.recovery_counter[i, j] <= 0:
                        new_grid[i, j] = 2  # 2 - выздоровевший
                elif self.grid[i, j] == 0:
                    infected_neighbors = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0: continue
                            nx, ny = i + dx, j + dy
                            if 0 <= nx < self.size and 0 <= ny < self.size:
                                if self.grid[nx, ny] == 1:
                                    infected_neighbors += 1
                    if infected_neighbors > 0:
                        chance = 1 - (1 - infection_prob) ** infected_neighbors
                        if random.random() < chance:
                            new_grid[i, j] = 1
                            self.recovery_counter[i, j] = 8
        self.grid = new_grid


class ForestFireModel:
    def __init__(self, size=60, tree_density=0.7):
        self.size = size
        # 0 - это пустая земля (будет сливаться с фоном)
        self.grid = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                if random.random() < tree_density:
                    self.grid[i, j] = 1  # 1 - живое дерево
        self.grid[size // 2, size // 2] = 2  # 2 - огонь

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


class TrafficModel:
    def __init__(self, size=100, density=0.4):
        self.size = size
        self.positions = []
        self.speeds = []
        for i in range(size):
            if random.random() < density:
                self.positions.append(i)
                self.speeds.append(random.randint(1, 5))
        self.positions = np.array(self.positions)
        self.speeds = np.array(self.speeds)

    def update(self):
        n = len(self.positions)
        if n == 0: return
        for i in range(n):
            dist = (self.positions[(i + 1) % n] - self.positions[i]) % self.size
            if dist == 0: dist = self.size
            if self.speeds[i] < 5: self.speeds[i] += 1
            if self.speeds[i] >= dist: self.speeds[i] = dist - 1
            if self.speeds[i] > 0 and random.random() < 0.3:
                self.speeds[i] -= 1
        self.positions = (self.positions + self.speeds) % self.size
        idx = np.argsort(self.positions)
        self.positions = self.positions[idx]
        self.speeds = self.speeds[idx]


# --- ИНТЕРФЕЙС ---

st.sidebar.title("🛠 Настройки")
model_type = st.sidebar.selectbox("Выберите систему:",
                                  ["Эпидемия (SIR)", "Лесной пожар", "Транспортный поток"])

st.title(f" {model_type}")

# Выравниваем графики по центру для красоты
col1, col2, col3 = st.columns([1, 2, 1])

if model_type == "Эпидемия (SIR)":
    pop_density = st.sidebar.slider("Плотность населения", 0.1, 1.0, 0.6)
    inf_prob = st.sidebar.slider("Вероятность заражения", 0.05, 1.0, 0.3)
    steps = st.sidebar.slider("Шаги анимации", 50, 200, 100)

    st.markdown("""
    <div class="legend-box">
    🟢 <b>Здоровые</b> &nbsp;|&nbsp; 🔴 <b>Больные</b> &nbsp;|&nbsp; ⚪ <b>Выздоровевшие</b> &nbsp;|&nbsp; ⚫ <b>Пусто</b>
    </div>
    """, unsafe_allow_html=True)

    with col2:
        plot_spot = st.empty()

    if st.sidebar.button("▶ Запустить симуляцию"):
        model = EpidemicModel(size=60, density=pop_density)
        # Цвета: 0-Зеленый, 1-Красный, 2-Серый, 3-Фон сайта (#1e1e1e)
        cmap = ListedColormap(['#2ecc71', '#e74c3c', '#95a5a6', '#1e1e1e'])

        for s in range(steps):
            model.update(inf_prob)
            fig, ax = plt.subplots(figsize=(6, 6))
            fig.patch.set_facecolor('#1e1e1e')
            # Фиксируем диапазоны цветов vmin=0, vmax=3
            ax.imshow(model.grid, cmap=cmap, vmin=0, vmax=3)
            ax.axis('off')
            plot_spot.pyplot(fig)
            plt.close(fig)
            time.sleep(0.02)

elif model_type == "Лесной пожар":
    tree_density = st.sidebar.slider("Плотность леса", 0.1, 1.0, 0.7)
    steps = st.sidebar.slider("Шаги анимации", 50, 200, 100)

    # ВОТ ЗДЕСЬ ИСПРАВЛЕНА ЛЕГЕНДА: ДОБАВЛЕНА ПУСТОШЬ
    st.markdown("""
    <div class="legend-box">
    🌳 <b>Живой лес</b> &nbsp;|&nbsp; 🔥 <b>Огонь</b> &nbsp;|&nbsp; 🟫 <b>Пепелище</b> &nbsp;|&nbsp; ⚫ <b>Пустошь</b>
    </div>
    """, unsafe_allow_html=True)

    with col2:
        plot_spot = st.empty()

    if st.sidebar.button("▶ Запустить симуляцию"):
        model = ForestFireModel(size=60, tree_density=tree_density)
        # Цвета: 0-Фон сайта (#1e1e1e), 1-Зеленый, 2-Оранжевый, 3-Коричневый
        cmap = ListedColormap(['#1e1e1e', '#27ae60', '#e67e22', '#5d4037'])

        for s in range(steps):
            model.update()
            fig, ax = plt.subplots(figsize=(6, 6))
            fig.patch.set_facecolor('#1e1e1e')
            # Фиксируем диапазоны цветов vmin=0, vmax=3
            ax.imshow(model.grid, cmap=cmap, vmin=0, vmax=3)
            ax.axis('off')
            plot_spot.pyplot(fig)
            plt.close(fig)
            time.sleep(0.02)

elif model_type == "Транспортный поток":
    car_density = st.sidebar.slider("Плотность машин", 0.1, 0.9, 0.4)
    steps = st.sidebar.slider("Шаги анимации", 50, 300, 150)

    st.markdown("""
    <div class="legend-box">
    🟦 <b>Автомобиль</b> &nbsp;|&nbsp; ⬛ <b>Свободная дорога</b>
    </div>
    """, unsafe_allow_html=True)

    plot_spot = st.empty()

    if st.sidebar.button("▶ Запустить симуляцию"):
        model = TrafficModel(size=100, density=car_density)

        for s in range(steps):
            model.update()
            grid = np.zeros(100)
            grid[model.positions.astype(int)] = 1

            fig, ax = plt.subplots(figsize=(12, 1.5))
            fig.patch.set_facecolor('#1e1e1e')
            ax.bar(range(100), grid, color='#00d4ff', width=1.0)
            ax.set_ylim(0, 1)
            ax.axis('off')
            plot_spot.pyplot(fig)
            plt.close(fig)
            time.sleep(0.03)
