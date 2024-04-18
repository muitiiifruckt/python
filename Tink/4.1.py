def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        for j in range(i + 1, cols):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            print(i,j,j,i)
    return matrix
def reflect_matrix_vertical(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows // 2):
        for j in range(cols):
            matrix[i][j], matrix[rows - 1 - i][j] = matrix[rows - 1 - i][j], matrix[i][j]
            print(i,j,rows-1-i,j)
    return matrix

def reflect_matrix_horizontal(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows // 2):
        for j in range(cols):
            matrix[i][j], matrix[rows - 1 - i][j] = matrix[rows - 1 - i][j], matrix[i][j]
            print(i,j,rows-1-i,j)
    return matrix


def zzzz(n, direction, matrix):
    if direction == "L":
        matrix= transpose_matrix(matrix)
        matrix = reflect_matrix_vertical(matrix)
    else:
        matrix = reflect_matrix_horizontal(matrix)
        matrix = transpose_matrix(matrix)
    return matrix





n, direction = input().split()
n = int(n)
matrix = []
for _ in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)
print(int((n*((n)//2)+((1+n-1)/2*(n-1)))))
matrix = zzzz(n,direction,matrix)


