"""
Порівняння водойм на зображеннях
"""

from matplotlib import pyplot as plt
import numpy as np
import cv2


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


def harris_corner_detector(image, segmented_image):
    """ Детектор кутів Гарріса """
    floated_image = np.float32(segmented_image)
    # Застосування детектора кутів Гарріса
    dst = cv2.cornerHarris(floated_image, 2, 3, 0.04)

    # Диляція результату для позначення кутів
    dst = cv2.dilate(dst, None)

    # Поріг для оптимального значення
    threshold_value = 0.01 * dst.max()
    image[dst > threshold_value] = [0, 0, 255]

    # Отримання координат кутів
    key_points = np.argwhere(dst > threshold_value)
    # Створення ключових точок
    key_points = [cv2.KeyPoint(float(x[1]), float(x[0]), 13) for x in key_points]
    return key_points, image


def sift_matching(image1, segmented_image1, image2, segmented_image2):
    # Знаходження кутів Гарріса для сегментованих зображень
    key_points1, harris_corner_image1 = harris_corner_detector(image1.copy(), segmented_image1)
    key_points2, harris_corner_image2 = harris_corner_detector(image2.copy(), segmented_image2)
    show_image(harris_corner_image1)
    show_image(harris_corner_image2)

    # Створення SIFT детектору
    sift = cv2.SIFT_create()

    # Обчислення дескрипторів
    key_points1, descriptors1 = sift.compute(segmented_image1, key_points1)
    key_points2, descriptors2 = sift.compute(segmented_image2, key_points2)
    show_image(cv2.drawKeypoints(image1, key_points1, image1))
    show_image(cv2.drawKeypoints(image2, key_points2, image2))

    # Параметри FLANN
    flann_index_kdtree = 1
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=100)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    # Знаходження збігів
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)
    matches = list(matches)

    # Фільтрація збігів
    for match in matches:
        m, n = match
        if m.distance < n.distance:
            matches.remove(match)

    # Параметри зображення збігів
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # Зображення збігів
    img3 = cv2.drawMatchesKnn(harris_corner_image1, key_points1, harris_corner_image2, key_points2, matches, None, **draw_params)
    matches_number = len(matches)
    probability = matches_number / len(key_points1)
    return img3, matches_number, probability


# Обробка високоякісного зображення
image_entrance_1 = image_read("low2.jpg")
show_image(image_entrance_1)
image_exit = image_processing(image_entrance_1.copy(), True)
img_segment_1 = segmentation(image_exit)
show_image(img_segment_1)

# Обробка низькоякісного зображення
image_entrance_2 = image_read("high2.jpg")
show_image(image_entrance_2)
image_exit = image_processing(image_entrance_2.copy(), False)
img_segment_2 = segmentation(image_exit)
show_image(img_segment_2)

result, matches_number, probability = sift_matching(image_entrance_1, img_segment_1, image_entrance_2, img_segment_2)
print("Кількість збігів особливих точок =", matches_number)
print("Ймовірність ідентифікації =", probability)
show_image(result)
save_result("result.jpg", result)
