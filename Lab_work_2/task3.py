"""
Цифрова обробка зображень: корекція кольору цифрового растрового зображення (негатив) в градієнтах:
діагональ (верхній лівий до нижнього правого кута); від центру; до центру.
"""

import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt


def print_center(width, height, pixels, name):
    """ Вивід RGB центру зображення """
    center_x, center_y = width // 2, height // 2
    print(f"Image - {name}; coordinates - {center_x}, {center_y}; RGB - {pixels[center_x, center_y]}")


def image_read(file_name):
    """ Завантаження зображення """
    image = Image.open(file_name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pixels = image.load()

    plt.imshow(image)
    plt.title("Start image")
    plt.show()
    print_center(width, height, pixels, "Start image")

    image_info = {"image_file": image, "image_draw": draw, "image_width": width, "image_height": height, "image_pixels": pixels}
    return image_info


def get_default_gradient(img_width, img_height):
    """ Без градієнта (він дорівнює 1) """
    return np.full((img_width, img_height), 1)


def get_upper_left_to_bottom_right_gradient(img_width, img_height):
    """ Значення градієнта варіюється від 0 (лівий верхній кут) до 1 (нижній правий кут) """
    gradient = np.zeros((img_width, img_height))
    max_value = img_width + img_height
    for i in range(img_width):
        for j in range(img_height):
            gradient[i, j] = (i + j) / max_value
    return gradient


def get_from_center_gradient(img_width, img_height):
    """ Значення градієнта варіюється від 0 (центр) до 1 (кути зображення) """
    center_x, center_y = img_width // 2, img_height // 2
    max_distance = np.sqrt((img_width - center_x) ** 2 + (img_height - center_y) ** 2)
    gradient = np.zeros((img_width, img_height))
    for i in range(img_width):
        for j in range(img_height):
            distance = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
            gradient[i, j] = distance / max_distance
    return gradient


def get_to_center_gradient(img_width, img_height):
    """ Значення градієнта варіюється від 0 (кути зображення) до 1 (центр) """
    center_x, center_y = img_width // 2, img_height // 2
    max_distance = np.sqrt((img_width - center_x) ** 2 + (img_height - center_y) ** 2)
    gradient = np.zeros((img_width, img_height))
    for i in range(img_width):
        for j in range(img_height):
            distance = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
            gradient[i, j] = 1 - distance / max_distance
    return gradient


def apply_negative(value, gradient):
    """ Розрахувати негатив """
    return int(255 - value * gradient)


def negative(file_name_init, gradient_function, window_title):
    """ Негатив """
    image_info = image_read(file_name_init)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pixels = image_info["image_pixels"]

    gradient = gradient_function(width, height)
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]

            gradient_value = gradient[i, j]

            modified_r = apply_negative(r, gradient_value)
            modified_g = apply_negative(g, gradient_value)
            modified_b = apply_negative(b, gradient_value)
            draw.point((i, j), (modified_r, modified_g, modified_b))

    plt.imshow(image)
    plt.title(window_title)
    plt.show()
    print_center(width, height, pixels, window_title)

    result_file_name = window_title + ".jpg"
    image.save(result_file_name, "JPEG")
    return


if __name__ == "__main__":
    init_file = "ferrari-sf-24-1.jpg"
    # init_file = "start.jpg"
    # init_file = "sentinel_2023.jpg"
    negative(init_file, lambda width, height: get_default_gradient(width, height), "Negative without gradient")
    negative(init_file, lambda width, height: get_upper_left_to_bottom_right_gradient(width, height), "Negative with diagonal (upper left to bottom right) gradient")
    negative(init_file, lambda width, height: get_from_center_gradient(width, height), "Negative with from center gradient")
    negative(init_file, lambda width, height: get_to_center_gradient(width, height), "Negative with to center gradient")
