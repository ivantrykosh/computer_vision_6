"""
Ідентифікація номерів державної реєстрації на автомобілях
"""

import cv2
import matplotlib.pyplot as plt


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
    """ Покращення зображення """

    # Перетворюємо зображення у відтінки сірого, виконаємо операцію blackhat, яка дозволить
    # виявити темні області (текст на номерному знаку) на світлому фоні (тобто сам знак)
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rectangular_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    blackhat_transformed = cv2.morphologyEx(gray_image, cv2.MORPH_BLACKHAT, rectangular_kernel)

    # Розмиваємо зображення, застосовуємо згладжування для закриття та алгоритм OTSU для
    # визначення порогу бінаризації, щоб розділити зображення на фон та об'єкти
    blurred_image = cv2.GaussianBlur(blackhat_transformed, (5, 5), 0)
    blurred_image = cv2.morphologyEx(blurred_image, cv2.MORPH_CLOSE, rectangular_kernel)
    binary_threshold_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Ерозія та розширення для зменшення шуму
    processed_image = cv2.erode(binary_threshold_image, None, iterations=3)
    processed_image = cv2.dilate(processed_image, None, iterations=3)
    return processed_image.copy()


def find_contours(processed_image):
    """ Знаходження контурів на зображення """
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_contours(image, contours):
    """
    Малювання контурів на початковому зображенні.
    До уваги беруть ті контури, які мають 4 сторони, де ширина втричі більша за висоту і висота не є малою
    """
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
        _, _, w, h = cv2.boundingRect(approx)
        if len(approx) == 4 and w > h * 3 and h > 10:
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)

    return image


def save_result(file_name, image_in_rgb):
    """ Збереження результату у файл """
    image_in_bgr = cv2.cvtColor(image_in_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(file_name, image_in_bgr)


image_entrance = image_read("image.jpg")
show_image(image_entrance)

processed_img = image_processing(image_entrance)
show_image(processed_img)

found_contours = find_contours(processed_img)

result_image = draw_contours(image_entrance, found_contours)
save_result("image_recognition.jpg", result_image)
show_image(result_image)
