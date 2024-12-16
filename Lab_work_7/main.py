"""
Розпізнавання літералів з допомогою 'сирої' нейромережі
"""

import numpy as np
import matplotlib.pyplot as plt


# Літерали
A = [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1]
B = [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0]
C = [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
D = [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0]
E = [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
F = [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
G = [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0]
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


def generate_weights(in_neurons, out_neurons):
    """ Випадкова генерація ваг """
    return np.random.randn(in_neurons, out_neurons)


def sigmoid(value):
    """ Сигмоїдна функція активації """
    return 1 / (1 + np.exp(-value))


def loss(out, y, out_number):
    """ Обчислення MSE для виводу мережі """
    s = (np.square(out - y))
    s = np.sum(s) / out_number
    return s


class NeuralNetwork:
    """ Нейронна мережа """

    def __init__(self, neurons_numbers):
        """ Ініціалізація ваг """
        self.weights = [generate_weights(neurons_numbers[index], neurons_numbers[index + 1]) for index in range(len(neurons_numbers) - 1)]

    def feed_forward(self, x):
        """ Рух мережею """
        a = x
        for weight in self.weights:
            z = a.dot(weight)
            a = sigmoid(z)
        return a

    def back_propagation(self, x, y, alpha):
        """ Зворотне поширення помилки """

        # Обчислення виходів мережі на різних шарах
        activations = [x]
        for weight in self.weights:
            z = activations[-1].dot(weight)
            a = sigmoid(z)
            activations.append(a)

        # Обчислення похибок
        deltas = [(activations[-1] - y)]
        for i in range(len(self.weights) - 1, 0, -1):
            val = 1 - activations[i]
            d = np.multiply(self.weights[i].dot(deltas[0].transpose()).transpose(),
                            np.multiply(activations[i], 1 - activations[i]))
            deltas.insert(0, d)

        # Обчислення градієнтів
        weight_adjustments = [activations[i].transpose().dot(d) for i, d in enumerate(deltas)]

        # Оновлення ваг
        for i in range(len(self.weights)):
            self.weights[i] -= alpha * weight_adjustments[i]

        return

    def train(self, X, Y, alpha=0.01, epoch=10):
        """ Тренування моделі """
        acc = []
        losses = []
        for j in range(1, epoch + 1):
            l = []
            for i in range(len(X)):
                out = self.feed_forward(X[i])
                l.append(loss(out, Y[i], len(Y)))
                self.back_propagation(X[i], y[i], alpha)
            if j % 10 == 0:
                print('epochs:', j, '======== acc:', (1 - (sum(l) / len(X))) * 100)
            acc.append((1 - (sum(l) / len(X))) * 100)
            losses.append(sum(l) / len(X))
        return acc, losses, self.weights

    def predict(self, x):
        """ Виконання передбачення та відображення результатів """
        out = self.feed_forward(x)

        fig, axs = plt.subplots(1, 2, figsize=(12, 6))

        axs[0].imshow(np.array(x).reshape(5, 6))
        axs[0].set_title('Літера')

        axs[1].bar(range(len(out[0])), out[0])
        axs[1].set_xlabel('Літери')
        axs[1].set_ylabel('Ймовірність ідентифікації')
        axs[1].set_title('Ймовірність ідентифікації літери')
        axs[1].set_xticks(range(len(out[0])), letters)

        plt.show()
        return out


def visualize_letters(letters):
    """ Відображення літер """
    for index in range(len(letters)):
        plt.subplot(3, 3, index + 1)
        plt.imshow(np.array(letters[index]).reshape(5, 6))
    plt.show()


dataset = [A, B, C, D, E, F, G]
visualize_letters(dataset)
x = [np.array(letter).reshape(1, 30) for letter in dataset]
y = np.eye(len(dataset), dtype=int)

# Ініціалізація нейронної мережі
# Перший (вхідний) шар - 30 нейронів, другий (прихований) шар - 9 нейронів, третій (вихідний) шар - 7 нейронів
neurons = [30, 9, 7]
neural_network = NeuralNetwork(neurons)

# Тренування мережі
acc, losses, weights = neural_network.train(x, y, 0.1, 1000)
# Натреновані ваги
print('Ваги', weights, sep='\n')

# Візуалізація точності та втрат мережі під час навчання
plt.plot(acc)
plt.title('Точність по епохах')
plt.ylabel('Точність')
plt.xlabel('Епохи')
plt.show()

plt.plot(losses)
plt.title('Втрати по епохах')
plt.ylabel('Втрати')
plt.xlabel('Епохи')
plt.show()

# Ідентифікація літер
for index in range(len(x)):
    result = neural_network.predict(x[index])
    print(f'Ідентифікація літери {letters[index]}: [{" ".join(["{:.4f}".format(item) for item in result[0]])}], очікуваний результат: {y[index]}')
