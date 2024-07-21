def calculate_gradient(coefficients, x, y):

    df_dx = 2 * coefficients[0] * x + coefficients[3] + coefficients[2] * y
    df_dy = coefficients[2] * x + 2 * coefficients[1] * y + coefficients[4]
    return (df_dx, df_dy)

def max_abs_value(numbers):

    num1, num2 = numbers
    if abs(num1) > abs(num2):
        return (-1, 0) if num1 > 0 else (1, 0)
    else:
        return (0, -1) if num2 > 0 else (0, 1)

def calculate_lambda(coefficients, x, y, direction):

    s1, s2 = direction
    a = 2 * coefficients[0] * s1 ** 2 + 2 * coefficients[1] * s2 ** 2 + coefficients[2] * s1 * s2
    b = 2 * coefficients[0] * x * s1 + 2 * coefficients[1] * y * s2 + coefficients[2] * (x * s2 + y * s1) + coefficients[3] * s1 + coefficients[4] * s2
    return -b / a if a != 0 else 0  # Обработка случая деления на ноль

def calculate_next_point(x, y, direction, lamda):

    s1, s2 = direction
    return (x + lamda * s1, y + lamda * s2)

def func_value(coefficients, x, y):

    return coefficients[0] * x ** 2 + coefficients[1] * y ** 2 + coefficients[2] * x * y + coefficients[3] * x + coefficients[4] * y + coefficients[5]

# Пример использования
keff = [0.5, 1, -1, -3, 2, 0]  # Коэффициенты: c1, c2, c3, c4, c5, c6
x_0 = [2, 5]
epsilon = 0.01 # Порог для остановки алгоритма
max_iterations = 15


ct = 0
while True:
    ct += 1
    f_val = func_value(keff, x_0[0], x_0[1])
    print()
    print(f"f(x) = {f_val}")
    print(f"Точки: {x_0[0]}, {x_0[1]}")

    # Шаг 1: Вычисляем градиент
    gradient = calculate_gradient(keff, x_0[0], x_0[1])
    print(f"Градиент: {gradient[0]}, {gradient[1]}")

    # Условие остановки
    if abs(gradient[0]) < epsilon and abs(gradient[1]) < epsilon:
        print("Градиент близок к нулю, алгоритм завершен.")
        break

    # Шаг 2: Определяем направление
    direction = max_abs_value(gradient)
    print(f"Направление: {direction[0]}, {direction[1]}")

    # Шаг 3: Вычисляем шаг лямбда
    lamda = calculate_lambda(keff, x_0[0], x_0[1], direction)
    print(f"Лямбда: {lamda}")

    # Шаг 4: Обновляем точку
    x_0 = calculate_next_point(x_0[0], x_0[1], direction, lamda)
    print(f"Следующая итерационная точка: ({x_0[0]}, {x_0[1]})")

    # Проверка дополнительных условий остановки
    if abs(lamda) < epsilon or ct >= max_iterations:
        print()
        print(f"Остановка, lamda:{lamda}")
        print(f"iteration:  {max_iterations}")
        break

# Вывод конечных результатов
print(f"Конечное значение функции: {func_value(keff, x_0[0], x_0[1])} в точке ({x_0[0]}, {x_0[1]})")
print(f"Количество итераций: {ct}")
