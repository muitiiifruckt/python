def find_swap_operations(matrix1, matrix2, n):
    operations = []
    for i in range(n):
        for j in range(n):
            if matrix1[i][j] != matrix2[i][j]:
                # Ищем элемент в matrix1, который равен текущему элементу из matrix2
                for x in range(i, n):
                    for y in range(n):
                        if matrix1[x][y] == matrix2[i][j]:
                            operations.append((i, j, x, y))

                            # Меняем элементы местами
                            matrix1[i][j], matrix1[x][y] = matrix1[x][y], matrix1[i][j]
                            break
    return operations


def print_matrix(matrix):
    for row in matrix:
        print(row)

# Тестовые матрицы
matrix1 = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]]

matrix2 = [[9, 2, 3],
           [4, 1, 6],
           [7, 8, 5]]

n = 3

# Ожидаемый вывод
expected_operations = [(0, 0, 2, 0), (1, 1, 0, 1), (1, 0, 0, 0)]

# Вызываем функцию для нахождения операций
operations = find_swap_operations(matrix1, matrix2, n)
print_matrix(matrix1)
print_matrix(matrix2)
