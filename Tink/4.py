def rotate_matrix(n, direction, matrix):
    operations = []
    if direction == 'L':
        operations = find_swap_operations(matrix,rotate_L(n,matrix),n)
    elif direction == 'R':
        operations = find_swap_operations(matrix, rotate_R(n, matrix),n)
    return operations
def rotate_L(n,matrix):
    rotated_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rotated_matrix[n-1-j][ i] = matrix[i][j]
    return rotated_matrix
def rotate_R(n,matrix):
    rotated_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rotated_matrix[j][n-1-i] = matrix[i][j]
    return rotated_matrix
def find_swap_operations(matrix1, matrix2, n):
    operations = []
    for i in range(n):
        for j in range(n):
            if matrix1[i][j] != matrix2[i][j]:
                for x in range(i, n):
                    for y in range(n):
                        if matrix1[x][y] == matrix2[i][j]:
                            operations.append((i, j, x, y))
                            matrix1[i][j], matrix1[x][y] = matrix1[x][y], matrix1[i][j]
                            break
    return operations

# Ввод данных
n, direction = input().split()
n = int(n)
matrix = []
for _ in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)


# Получение операций
operations = rotate_matrix(n, direction, matrix)

# Вывод результата
print(len(operations))
for op in operations:
    print(*op)

