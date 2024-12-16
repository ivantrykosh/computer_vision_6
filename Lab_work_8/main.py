"""
Реконструкція 3D просторових об'єктів за їх 2D зображеннями
"""

import numpy as np
import cv2
import open3d as o3d

# Формат заголовка PLY файлу
ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''


def write_ply(filename, vertices, vertices_colors):
    """ Записування точок та їх кольорів у файл """
    vertices = vertices.reshape(-1, 3)
    vertices_colors = vertices_colors.reshape(-1, 3)
    vertices = np.hstack([vertices, vertices_colors])
    with open(filename, 'wb') as file:
        file.write((ply_header % dict(vert_num=len(vertices))).encode('utf-8'))
        np.savetxt(file, vertices, fmt='%f %f %f %d %d %d ')


# Зчитування зображень
imgL = cv2.imread('img1.jpg')
imgR = cv2.imread('img2.jpg')

# Параметри для алгоритму зіставлення стереоблоків
window_size = 4
min_disp = 4
num_disp = 18 - min_disp
stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                               numDisparities=num_disp,
                               blockSize=16,
                               P1=8 * 3 * window_size**2,
                               P2=32 * 3 * window_size**2,
                               disp12MaxDiff=0,
                               uniquenessRatio=10,
                               speckleWindowSize=100,
                               speckleRange=32)

# Обчислення невідповідностей
disparities = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

# Розміри зображення
h, w = imgL.shape[:2]
# Фокусна відстань
f = 0.5 * w
# Обчислення матриці для проєктування невідповідностей у 3D просторі
Q = np.float32([[1,  0,  0, -0.5*w],
                [0, -1,  0,  0.5*h],
                [0,  0,  0,     -f],
                [0,  0,  1,      0]])
# Проєктування невідповідностей на 3D точки
points = cv2.reprojectImageTo3D(disparities, Q)
# Отримання кольорів із зображення
colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
# Записування точок у файл
write_ply('out.ply', points, colors)

# Вивід зображень та невідповідностей
cv2.imshow('left', imgL)
cv2.imshow('right', imgR)
cv2.imshow('disparity', (disparities - min_disp) / num_disp)

# Завантаження хмари точок з файлу
pcd = o3d.io.read_point_cloud('out.ply')
# Візуалізація хмари точок
o3d.visualization.draw_geometries([pcd], width=500, height=500, left=20, top=20)

# Закриття вікон
cv2.waitKey()
cv2.destroyAllWindows()
