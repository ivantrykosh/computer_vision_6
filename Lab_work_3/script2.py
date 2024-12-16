"""
Виділення контору трикутника на цифровому растровому зображенні
"""

import cv2
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


def image_processing(image):
    """ Обробка зображення """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    return closed


def image_contours(image):
    """ Знаходження контурів """
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def save_result(file_name, image_in_rgb):
    """ Збереження результату у файл """
    image_in_bgr = cv2.cvtColor(image_in_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(file_name, image_in_bgr)


def image_recognition(image, contours):
    """ Розпізнавання трикутника """
    total_triangles = 0
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.05 * peri, True)
        if len(approx) == 3:
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
            total_triangles += 1
    return image, total_triangles


image_entrance = image_read("image.jpg")
show_image(image_entrance)

image_exit = image_processing(image_entrance)
show_image(image_exit)

image_contours = image_contours(image_exit)

result, total_figures = image_recognition(image_entrance, image_contours)
print(f"Знайдено {total_figures} трикутних об'єктів")
save_result("image_recognition.jpg", result)
show_image(result)
