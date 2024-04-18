import random
def generate_board_and_n():
    n = 5
    board = ["."]*n
    for i in range(n):
        board[i] = ["."]*n

    for i in range(n):
        for j in range(n):
            randomm = random.randint(0,10)
            figure = ""
            if(randomm>9):
                figure = "K"
            elif randomm<2:
                figure = "G"
            board[i][j] = figure
    rand_S_x = random.randint(0,n-1)
    rand_S_y = random.randint(0, n-1)
    rand_F_x = random.randint(0, n-1)
    rand_F_y = random.randint(0, n-1)
    board[rand_S_x][rand_S_y] = "S"
    board[rand_F_x][rand_F_y] = "F"
    print(n)
    for row in board:
        string = ""
        for s in row:
            if s:
                string +=s
            else:
                string +="."
        print(string)
generate_board_and_n()