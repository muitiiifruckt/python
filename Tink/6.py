from collections import deque


def is_valid(x, y, n):
    return 0 <= x < n and 0 <= y < n

def bfs(board, n):
    directions_King = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    directions_Kon = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
    start = None
    end = None

    for i in range(n):
        for j in range(n):
            if board[i][j] == 'S':
                start = (i, j, 'K')  # Начальная позиция считается как конь
            elif board[i][j] == 'F':
                end = (i, j)

    visited_King = set()
    visited_Kon = set()
    queue = deque([(start, 0)])

    while queue:
        (x, y, piece), steps = queue.popleft()

        if (x, y) == end:
            return steps
        if piece == "G":
            for dx, dy in directions_King:
                nx, ny = x + dx, y + dy

                if is_valid(nx, ny, n) and (nx, ny) not in visited_King:
                    visited_King.add((nx, ny))
                    if board[nx][ny] == 'F':
                        return steps+1
                    elif board[nx][ny] == '.' or board[nx][ny] == '':
                        queue.append(((nx, ny, piece), steps + 1))
                    elif board[nx][ny] == 'K':
                        queue.append(((nx, ny, 'K'), steps + 1))
                    elif board[nx][ny] == 'G':
                        queue.append(((nx, ny, 'G'), steps + 1))
        else:
            for dx, dy in directions_Kon:
                nx, ny = x + dx, y + dy

                if is_valid(nx, ny, n) and (nx, ny) not in visited_Kon:
                    visited_Kon.add((nx, ny))
                    if board[nx][ny] == 'F':
                        return steps+1
                    elif board[nx][ny] == '.' or board[nx][ny] == '':
                        queue.append(((nx, ny, piece), steps + 1))
                    elif board[nx][ny] == 'K':
                        queue.append(((nx, ny, 'K'), steps + 1))
                    elif board[nx][ny] == 'G':
                        queue.append(((nx, ny, 'G'), steps + 1))
    return -1




n = int(input())
board = [input() for _ in range(n)]
print(bfs(board,n))

