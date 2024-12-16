"""
Ідентифікація водойм на зображеннях різної якості
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


def show_image(image):
    """ Показ зображення """
    plt.imshow(image)
    plt.show()


def image_read(file_image):
    """ Зчитування зображення з файлу """
    image = cv2.imread(file_image)
    image_in_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_in_rgb


def image_processing(image, is_blurred=False):
    """ Обробка зображення """
    # Конвертуємо зображення у відтінки сірого
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Застосовуємо Гаусівське розмиття, якщо потрібно
    if is_blurred:
        gray = cv2.GaussianBlur(gray, (5, 5), 5)

    # Виділяємо темні області на зображенні
    _, threshold_image = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Застосуємо згладжування
    threshold_image = cv2.medianBlur(threshold_image, 5)

    return threshold_image


def image_contours(image):
    """ Знаходження контурів """
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def save_result(file_name, image_in_rgb):
    """ Збереження результату у файл """
    image_in_bgr = cv2.cvtColor(image_in_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(file_name, image_in_bgr)


def image_recognition(image, contours):
    """ Відображення контурів на зображенні """
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    return image


def segmentation(image):
    """ Сегментація з допомогою k-means """
    # Перетворюємо зображення у двовимірний масив
    two_dimension = image.reshape((-1, 3))
    two_dimension = np.float32(two_dimension)

    # Критерії зупинки для алгоритму k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Кількість кластерів та спроб
    k = 2
    attempts = 10

    # Застосовуємо алгоритм k-means
    ret, label, center = cv2.kmeans(two_dimension, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)

    # Отримуємо сегментаційні результати та відновлюємо форму зображення
    res = center[label.flatten()]
    edged_img = res.reshape(image.shape)
    return edged_img


# Обробка високоякісного зображення
image_entrance = image_read("high.jpg")
show_image(image_entrance)
image_exit = image_processing(image_entrance, True)
show_image(image_exit)
img_segment = segmentation(image_exit)
show_image(img_segment)
img_contours = image_contours(img_segment)
result = image_recognition(image_entrance, img_contours)
save_result("high_recognition.jpg", result)
show_image(result)


# Обробка низькоякісного зображення
image_entrance = image_read("low.jpg")
show_image(image_entrance)
image_exit = image_processing(image_entrance, False)
show_image(image_exit)
img_segment = segmentation(image_exit)
show_image(img_segment)
img_contours = image_contours(img_segment)
result = image_recognition(image_entrance, img_contours)
save_result("low_recognition.jpg", result)
show_image(result)
