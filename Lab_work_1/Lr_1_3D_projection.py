"""
--------------------- 3D - геометричні перетворення ---------------------------
Завдання:
Синтез 3D об'єкту (піраміда з чотирикутною основою) та його геометричне перетворення:
1. Аксонометрична проєкція будь-якого типу;
2. Циклічне обертання 3D об'єкту навколо будь-якої обраної внутрішньої осі.

"""

import random

from graphics import *
import numpy as np
import math

# Параметри вікна
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Параметри піраміди
PYRAMID_WIDTH = 150
PYRAMID_HEIGHT = 300

# Координати піраміди. Перша - вершина
pyramid = np.array([[0, 0, 0, 1],
                    [-PYRAMID_WIDTH//2, PYRAMID_HEIGHT, -PYRAMID_WIDTH//2, 1],
                    [+PYRAMID_WIDTH//2, PYRAMID_HEIGHT, -PYRAMID_WIDTH//2, 1],
                    [-PYRAMID_WIDTH//2, PYRAMID_HEIGHT, +PYRAMID_WIDTH//2, 1],
                    [+PYRAMID_WIDTH//2, PYRAMID_HEIGHT, +PYRAMID_WIDTH//2, 1]])


def project_on_x_y(figure):
    """ Спроєктувати на площину XY """
    t = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
    projection_x_y = figure.dot(t)
    return projection_x_y


def shift_figure(figure, l, m, n):
    """ Змістити фігуру """
    t = np.array([[1, 0, 0, l], [0, 1, 0, m], [0, 0, 1, n], [0, 0, 0, 1]])
    tt = t.T
    shifted_figure = figure.dot(tt)
    return shifted_figure


def degrees_to_radians(angle):
    """ Конвертувати градуси в радіани """
    return (math.pi * angle) / 180


def to_axonometric_view(figure, theta_d_1, theta_d_2):
    """ Зробити аксонометричну проєкцію """
    theta_r_1 = degrees_to_radians(theta_d_1)
    theta_r_2 = degrees_to_radians(theta_d_2)

    t1 = np.array([[math.cos(theta_r_1), 0, -math.sin(theta_r_1), 0],
                   [0, 1, 0, 0],
                   [math.sin(theta_r_1), 0, math.cos(theta_r_1), 0],
                   [0, 0, 0, 1]])
    view_y = figure.dot(t1)

    t2 = np.array([[1, 0, 0, 0],
                   [0, math.cos(theta_r_2), math.sin(theta_r_2), 0],
                   [0, -math.sin(theta_r_2), math.cos(theta_r_2), 0],
                   [0, 0, 0, 1]])
    view_y_x = view_y.dot(t2)
    return view_y_x


def rotate_y(figure, theta_d):
    """ Виконати поворот по осі Y """
    theta_r = degrees_to_radians(theta_d)
    t = np.array([[math.cos(theta_r), 0, -math.sin(theta_r), 0],
                  [0, 1, 0, 0],
                  [math.sin(theta_r), 0, math.cos(theta_r), 0],
                  [0, 0, 0, 1]])
    f_y = figure.dot(t)
    return f_y


class Figure:
    def __init__(self, window):
        self.window = window

        self.side1 = Polygon()
        self.side2 = Polygon()
        self.side3 = Polygon()
        self.side4 = Polygon()
        self.side5 = Polygon()

        self.counter = 0

    def __clear_figure(self):
        """ Очистити попередню фігуру """
        self.side1.undraw()
        self.side2.undraw()
        self.side3.undraw()
        self.side4.undraw()
        self.side5.undraw()

    def __set_color(self):
        """
        Встановити колір фігури на кожні 10 кроків.
        З ймовірністю 0.2 фігура буде білого кольору, інакше буде випадковий колір заливки та каркасу.
        """
        colors = ["black", "blue", "red", "gray", "yellow", "silver", "navy", "orange", "cyan"]

        if self.counter % 10 == 0:
            self.outline_color = "white"
            self.fill_color = "white"
            if random.random() < 0.8:
                self.outline_color = random.choice(colors)
                self.fill_color = random.choice(colors)

        self.side1.setOutline(self.outline_color)
        self.side1.setFill(self.fill_color)
        self.side2.setOutline(self.outline_color)
        self.side2.setFill(self.fill_color)
        self.side3.setOutline(self.outline_color)
        self.side3.setFill(self.fill_color)
        self.side4.setOutline(self.outline_color)
        self.side4.setFill(self.fill_color)
        self.side5.setOutline(self.outline_color)
        self.side5.setFill(self.fill_color)

        self.counter += 1

    def __draw_figure(self):
        """ Намалювати фігуру """
        self.side1.draw(self.window)
        self.side2.draw(self.window)
        self.side3.draw(self.window)
        self.side4.draw(self.window)
        self.side5.draw(self.window)

    def visualize(self, figure):
        """ Візуалізувати фігуру """
        e_x, e_y = figure[0, 0], figure[0, 1]
        a_x, a_y = figure[1, 0], figure[1, 1]
        b_x, b_y = figure[2, 0], figure[2, 1]
        c_x, c_y = figure[3, 0], figure[3, 1]
        d_x, d_y = figure[4, 0], figure[4, 1]

        self.__clear_figure()

        self.side1 = Polygon(Point(a_x, a_y), Point(b_x, b_y), Point(d_x, d_y), Point(c_x, c_y))
        self.side2 = Polygon(Point(a_x, a_y), Point(b_x, b_y), Point(e_x, e_y))
        self.side3 = Polygon(Point(a_x, a_y), Point(c_x, c_y), Point(e_x, e_y))
        self.side4 = Polygon(Point(b_x, b_y), Point(d_x, d_y), Point(e_x, e_y))
        self.side5 = Polygon(Point(c_x, c_y), Point(d_x, d_y), Point(e_x, e_y))

        self.__set_color()
        self.__draw_figure()


win = GraphWin("Обертання 3D піраміди з чотирикутною основою", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('white')

pyramid_figure = Figure(win)

# Кут повороту фігури
rotate_angle = 10
# Точка зсуву фігури
shift_point = [325, 75, 0]
# Кут проєкції
theta = 30

while True:
    pyramid = rotate_y(pyramid, rotate_angle)
    shifted_pyramid = shift_figure(pyramid, *shift_point)
    axonometric_pyramid = to_axonometric_view(shifted_pyramid, theta, theta)
    pyramid_projection = project_on_x_y(axonometric_pyramid)
    pyramid_figure.visualize(pyramid_projection)
    time.sleep(0.1)
