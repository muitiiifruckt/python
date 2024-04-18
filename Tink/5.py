def max_mushrooms_forest(forest):
    n = len(forest)
    if n == 0:
        return 0

    dp = [[0] * 3 for _ in range(n)]

    # Инициализируем первую строку
    for j in range(3):
        if forest[0][j] == 'C':
            dp[0][j] = 1

    # Заполняем остальные строки
    for i in range(1, n):
        for j in range(3):
            if forest[i][j] == 'C':
                dp[i][j] = max(dp[i-1][j], dp[i-1][max(j-1, 0)], dp[i-1][min(j+1, 2)]) + 1
            elif forest[i][j]==".":
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][max(j - 1, 0)], dp[i - 1][min(j + 1, 2)])

    return max(max(row) for row in dp)

# Чтение входных данных
n = int(input())
forest = [input() for _ in range(n)]

# Вызов функции и вывод результата
print(max_mushrooms_forest(forest))
