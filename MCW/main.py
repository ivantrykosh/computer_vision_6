"""
Ідентифікація облич з допомогою алгоритму каскадів Хаара
"""

import cv2

# Завантаження класифікатора каскадів Хаара для облич
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Завантаження зображення
image_path = '2.jpg'
image = cv2.imread(image_path)
result_image = image.copy()
gray_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)

# Виявлення облич
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

# Малювання прямокутників навколо виявлених облич
for (x, y, w, h) in faces:
    cv2.rectangle(result_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Збереження результату
output_path = f'output_{image_path[:image_path.rfind(".")]}.jpg'
cv2.imwrite(output_path, result_image)

# Відображення результату
cv2.imshow('Image', image)
cv2.imshow('Detected Faces', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
