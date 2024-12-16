"""
--------------------- 2D - геометричні перетворення ---------------------------
Завдання:
Програма повинна будувати 2D графічний об’єкт (квадрат) та реалізовувати його перетворення у матричній формі:
1. Переміщення + масштабування в режимі анімації;
2. Переміщення.

"""

from graphics import *
import time
import numpy as np

# Параметри вікна
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Розмір сторони квадрата
SQUARE_SIZE = 35

# Крок переміщення
dx = 35
dy = 35

# Коефіцієнти масштабування
s_x = 1.05
s_y = 1.05


def get_default_square_coordinates():
    """ Отримати координати стартового квадрату """
    x_1 = SQUARE_SIZE
    y_1 = WINDOW_HEIGHT - 2 * SQUARE_SIZE
    x_2 = 2 * SQUARE_SIZE
    y_2 = WINDOW_HEIGHT - SQUARE_SIZE
    return (x_1, y_1), (x_2, y_2)


def move_point(x_1, y_1):
    """ Перемістити точку """
    p = np.array([[x_1, y_1, 1]])
    t = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
    tt = t.T
    total = p.dot(tt)
    x11 = total[0, 0]
    y11 = total[0, 1]
    return x11, y11


def scale_point(x_1, y_1):
    """ Масштабувати точку """
    p = np.array([[x_1, y_1, 1]])
    s = np.array([[s_x, 0, 0], [0, s_y, 0], [0, 0, 1]])
    total = p.dot(s)
    x11 = total[0, 0]
    y11 = total[0, 1]
    return x11, y11


def stop_animation():
    """Зупинити анімацію"""
    time.sleep(0.2)


# ----------------    I. ПЕРЕМІЩЕННЯ ТА МАСШТАБУВАННЯ КВАДРАТА З АНІМАЦІЄЮ     ------------------------
win = GraphWin("Переміщення та масштабування квадрата", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('white')

(x1, y1), (x2, y2) = get_default_square_coordinates()

steps = 10
for i in range(steps):
    stop_animation()

    # Намалювати квадрат
    obj = Rectangle(Point(x1, y1), Point(x2, y2))
    obj.draw(win)

    # Перемістити точки квадрата
    x1, y1 = move_point(x1, y1)
    x2, y2 = move_point(x2, y2)

    # Масштабувати точки квадрата
    x1, y1 = scale_point(x1, y1)
    x2, y2 = scale_point(x2, y2)

win.getMouse()
win.close()


# ----------------    II. ПЕРЕМІЩЕННЯ КВАДРАТА     ------------------------
win = GraphWin("Переміщення квадрата", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('white')

(x1, y1), (x2, y2) = get_default_square_coordinates()

# Намалювати квадрат
obj = Rectangle(Point(x1, y1), Point(x2, y2))
obj.draw(win)

stop_animation()

# Перемістити точки квадрата
x1, y1 = move_point(x1, y1)
x2, y2 = move_point(x2, y2)

# Намалювати квадрат
obj = Rectangle(Point(x1, y1), Point(x2, y2))
obj.draw(win)

win.getMouse()
win.close()
