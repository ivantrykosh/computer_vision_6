"""
--------------------- Алгоритми над 3D фігурами ---------------------------
Завдання:
Синтез 3D об'єкту (піраміда з чотирикутною основою) та наступні дії над ним:
1. Застосувати алгоритм інтерполяції методом Лагранжа;
2. Застосувати алгоритм видалення невидимих ліній методом плаваючого обрію.
"""

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


def lagrange_interpolation(x, x1, y1, x2, y2):
    """
    Інтерполяція за допомогою методу Лагранжа.
    Формула для обчислення за двома точками: y - y1 = (y2-y1) / (x2-x1) * (x-x1)
    """
    return (y2 - y1) / (x2 - x1) * (x - x1) + y1


def apply_interpolation(x1, y1, x2, y2, num_points):
    """ Застосувати інтерполяцію для відрізка між точками (x1, y1) та (x2, y2) """
    interpolated_points = []
    for k in range(num_points):
        x = x1 + (x2 - x1) * k / num_points
        y = lagrange_interpolation(x, x1, y1, x2, y2)
        interpolated_points.append([x, y])
    return interpolated_points


class Figure:
    def __init__(self, window):
        self.window = window

        self.side1 = Polygon()
        self.side2 = Polygon()
        self.side3 = Polygon()
        self.side4 = Polygon()
        self.side5 = Polygon()

    def __clear_figure(self):
        """ Очистити попередню фігуру """
        self.side1.undraw()
        self.side2.undraw()
        self.side3.undraw()
        self.side4.undraw()
        self.side5.undraw()

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

        self.__draw_figure()

    def visualize_interpolation(self, figure, num_points=1000):
        """ Виконати інтерполяцію та візуалізувати фігуру """
        e_x, e_y = figure[0, 0], figure[0, 1]
        a_x, a_y = figure[1, 0], figure[1, 1]
        b_x, b_y = figure[2, 0], figure[2, 1]
        c_x, c_y = figure[3, 0], figure[3, 1]
        d_x, d_y = figure[4, 0], figure[4, 1]

        # Отримати інтерпольовані точки між вершиною та точками основи
        interpolated_points = []
        interpolated_points.extend(apply_interpolation(e_x, e_y, a_x, a_y, num_points))
        interpolated_points.extend(apply_interpolation(e_x, e_y, b_x, b_y, num_points))
        interpolated_points.extend(apply_interpolation(e_x, e_y, c_x, c_y, num_points))
        interpolated_points.extend(apply_interpolation(e_x, e_y, d_x, d_y, num_points))
        # Отримати інтерпольовані точки між точками основи
        interpolated_points.extend(apply_interpolation(a_x, a_y, b_x, b_y, num_points))
        interpolated_points.extend(apply_interpolation(a_x, a_y, c_x, c_y, num_points))
        interpolated_points.extend(apply_interpolation(d_x, d_y, b_x, b_y, num_points))
        interpolated_points.extend(apply_interpolation(d_x, d_y, c_x, c_y, num_points))

        self.__clear_figure()

        # Намалювати кожну інтерпольовану точку
        for i in range(len(interpolated_points)):
            point = Point(*interpolated_points[i])
            point.draw(self.window)

    def clear_window(self):
        clear = Rectangle(Point(0, 0), Point(WINDOW_WIDTH, WINDOW_HEIGHT))
        clear.setFill('white')
        clear.setOutline('white')
        clear.draw(self.window)

    def visualize_removing(self, figure, projection, x_max, y_max, z_max):
        """ Видалення невидимих граней та відображення фігури """
        e_x, e_y, e_z = figure[0, 0], figure[0, 1], figure[0, 2]
        a_x, a_y, a_z = figure[1, 0], figure[1, 1], figure[1, 2]
        b_x, b_y, b_z = figure[2, 0], figure[2, 1], figure[2, 2]
        c_x, c_y, c_z = figure[3, 0], figure[3, 1], figure[3, 2]
        d_x, d_y, d_z = figure[4, 0], figure[4, 1], figure[4, 2]

        # Визначення передньої/задньої грані по координаті z
        if (abs(a_z - z_max) > abs(c_z - z_max)) and (abs(b_z - z_max) > abs(d_z - z_max)):
            is_ab_front = True
        else:
            is_ab_front = False

        # Визначення лівої/правої грані по координаті x
        if (abs(b_x - x_max) > abs(a_x - x_max)) and (abs(d_x - x_max) > abs(c_x - x_max)):
            is_bd_left = True
        else:
            is_bd_left = False

        # Визначення нижньої грані по координаті y
        if abs(a_y - y_max) > abs(e_y - y_max):
            is_bottom = True
        else:
            is_bottom = False

        e_x, e_y = projection[0, 0], projection[0, 1]
        a_x, a_y = projection[1, 0], projection[1, 1]
        b_x, b_y = projection[2, 0], projection[2, 1]
        c_x, c_y = projection[3, 0], projection[3, 1]
        d_x, d_y = projection[4, 0], projection[4, 1]

        self.clear_window()

        self.side1 = Polygon(Point(a_x, a_y), Point(b_x, b_y), Point(d_x, d_y), Point(c_x, c_y))
        self.side2 = Polygon(Point(a_x, a_y), Point(b_x, b_y), Point(e_x, e_y))
        self.side3 = Polygon(Point(a_x, a_y), Point(c_x, c_y), Point(e_x, e_y))
        self.side4 = Polygon(Point(b_x, b_y), Point(d_x, d_y), Point(e_x, e_y))
        self.side5 = Polygon(Point(c_x, c_y), Point(d_x, d_y), Point(e_x, e_y))

        if is_bottom:
            self.side1.setFill('black')
            self.side1.draw(self.window)

        if is_ab_front:
            self.side2.setFill('green')
            self.side2.draw(self.window)
        else:
            self.side5.setFill('yellow')
            self.side5.draw(self.window)

        if is_bd_left:
            self.side3.setFill('red')
            self.side3.draw(self.window)
        else:
            self.side4.setFill('blue')
            self.side4.draw(self.window)


win = GraphWin("3D піраміда з чотирикутною основою", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('white')

pyramid_figure = Figure(win)

# Точка зсуву фігури
shift_point = [325, 75, 0]
# Кут проєкції
theta = 30

axonometric_pyramid = to_axonometric_view(pyramid, theta, theta)
shifted_pyramid = shift_figure(axonometric_pyramid, *shift_point)
pyramid_projection = project_on_x_y(shifted_pyramid)
# Звичайна піраміда
pyramid_figure.visualize(pyramid_projection)
win.getMouse()
# Інтерполяція
pyramid_figure.visualize_interpolation(pyramid_projection, 1000)
win.getMouse()
# Видалення невидимих граней
pyramid_figure.visualize_removing(axonometric_pyramid, pyramid_projection, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_HEIGHT)
win.getMouse()
