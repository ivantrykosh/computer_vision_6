"""
Переміщення та обертання з допомогою OpenGL:
    3D багатокутника (куб)
    3D моделі поверхні другого порядку (параболоїд)
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import numpy as np

# Розмір вікна
width, height = 800, 600

# Параметри для повороту фігур
angle_cube = 0
angle_surface = 0

# Параметр для руху об'єктів
time = 0.0


def init():
    """ Ініціалізація параметрів OpenGL """
    glClearColor(0.1, 0.1, 0.2, 1.0)  # Колір фону
    glEnable(GL_DEPTH_TEST)  # Тест глибини
    glEnable(GL_LIGHTING)  # Освітлення
    glEnable(GL_LIGHT0)  # Джерело світла

    # Налаштування джерела світла
    light_pos = [-10, -10, 10, 100]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    # Налаштування матеріалів об'єктів
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50)


def draw_polygon():
    """ Малювання куба по гранях """
    glBegin(GL_QUADS)

    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)

    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)

    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)

    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glEnd()


def draw_surface():
    """ Малювання параболоїда """
    glBegin(GL_QUADS)
    for x in np.arange(-1.0, 1.0, 0.1):
        for y in np.arange(-1.0, 1.0, 0.1):
            z = x ** 2 + y ** 2
            glVertex3f(x, y, z)
            glVertex3f(x + 0.1, y, (x + 0.1) ** 2 + y ** 2)
            glVertex3f(x + 0.1, y + 0.1, (x + 0.1) ** 2 + (y + 0.1) ** 2)
            glVertex3f(x, y + 0.1, x ** 2 + (y + 0.1) ** 2)
    glEnd()


def display():
    """ Відображення сцени """
    global angle_cube, angle_surface, time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Камера
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)

    # Переміщення та обертання куба
    glPushMatrix()
    cube_position = 2.0 * np.sin(time)
    glTranslatef(-3.0, cube_position, 1.0)
    glRotatef(angle_cube, 1, 1, 0)
    draw_polygon()
    glPopMatrix()

    # Переміщення та обертання параболоїда
    glPushMatrix()
    surface_position = 1.5 * np.sin(time)
    glTranslatef(surface_position, 0.0, -1.0)
    glRotatef(angle_surface, 0, 1, 0)
    draw_surface()
    glPopMatrix()

    glutSwapBuffers()
    angle_cube += 0.3  # Швидкість обертання куба
    angle_surface += 0.5  # Швидкість обертання поверхні другого порядку
    time += 0.01  # Зміна часу для руху об'єктів


def reshape(w, h):
    """ Налаштування сцени у вікні """
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    """ Запуск програми """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"3D Scene with OpenGL")
    init()
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()


if __name__ == "__main__":
    main()
