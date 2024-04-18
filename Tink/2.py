
def rotate_image_90(matrix):
    n = len(matrix)
    m = len(matrix[0])

    rotated_matrix = [[0] * n for _ in range(m)]

    for i in range(n):
        for j in range(m):
            rotated_matrix[j][n - 1 - i] = matrix[i][j]

    return rotated_matrix

while True:
    try:
        # Считываем размеры матрицы
        n, m = map(int, input().split())

        # Считываем матрицу
        matrix = []
        for _ in range(n):
            row = list(map(int, input().split()))
            matrix.append(row)

        # Поворачиваем matrix на 90 градусов
        rotated_matrix = rotate_image_90(matrix)


        # Выводим результат
        for row in rotated_matrix:
            print(*row)
        break
    except EOFError:
        break
