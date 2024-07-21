
board = [[".",".","9","7","4","8",".",".","."],["7",".",".","6",".","2",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7","9","8","6","2","4","1"],["2","6","4","3","1","7","5","9","8"],["1","9","8","5","2","4","3","6","7"],[".",".",".","8","6","3",".","2","."],[".",".",".","4","9","1",".",".","6"],[".",".",".","2","7","5","9",".","."]]
def find(x, y):
    if board[x][y] != ".":
        return
    nums = set()
    for i in range(9):
        if board[i][y] != ".":
            nums.add(int(board[i][y]))
        if board[x][i] != ".":
            nums.add(int(board[x][i]))
    a = x//3
    b = y//3
    for i in range(3):
        for j in range(3):
            num = board[3 * a + i][3 * b + j]
            if num!=".":
                nums.add(int(num))
    if len(nums) != 8:
        return
    print(nums)
    for i in range(1,10):
        if i not in nums:
            board[x][y] = str(i)
            return

for k in range(100):
    for i in range(9):
        for j in range(9):
            find(i, j)
print( board)
