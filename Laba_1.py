
from tabulate import tabulate
def init_basis(A):
    A_сol = [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]
    len_A = len(A)
    dop_bas = []
    ind_bas = []
    for i in range(len_A):
        basis = []
        for j in range(len_A): #генири базис
            basis.append(1 if i == j else 0)
        if not(basis in A_сol): # провер если такой базис в матрице A
            dop_bas.append(basis)
            ind_bas.append(i)
    return dop_bas
def check_basis(A, c, dop_bas):
    if dop_bas:
        for j in range(len(dop_bas[0])):
            for i in range(len(dop_bas)):
                A[j].append(dop_bas[i][j])
            c.append(BIG_NUM) # добавл в целевую функ омега
    return A, c
def check_P0(b, A, signs):# проверка B на не отриц
    for i, val in enumerate(b):
        if val < 0:
            b[i] = abs(val)  # Получаем абсолютное значение
            signs[i] *= -1  # Меняем знак уравнения
            A[i] = [-x for x in A[i]]  # Меняем знаки левой части уравнения
    return b, A, signs
def type(MIN, c):
    if not MIN:
        for i in range(len(c)):
            c[i] = c[i]*(-1)
    return c
def check_signs(A, c, signs):
    for i in range(len(signs)):
        if signs[i] == -1: #   <=
            for k in range(len(A)): # добавляем новую переменную в ограничения матрицы А
                A[k].append(1 if k == i else 0) # с положительном кэфом
            c.append(0) # в целевую доп переменные идут с кэфом 0
        elif signs[i] == 1:  #  >=
            for k in range(len(A)): # добавляем новую переменную в ограничения матрицы А
                A[k].append(-1 if k == i else 0) #с отрицательным кэфом
            c.append(0) # в целевую доп переменные идут с кэфом 0
    return A,c
def init_table(A, c, b): # возвращает чисто таблицу без дельта
    ind_bas = []
    A_col = [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]
    for i in range(len(b)):
        basis = list()
        for j in range(len(b)):# ген баз
            basis.append(1 if i==j else 0)
        for k in range(len(A_col)):# находим базис и индекс
            if basis == A_col[k]:
                ind_bas.append(k+1)
    # получили индексы базисов по порядку, строим таблицу
    table = ind_bas.copy() # индексы базиса в итоговую таблицу
    for i in range(len(table)):
        table[i]= [table[i],c[table[i]-1]]# добавл cb
        table[i].append(b[i]) #  P0
    for i in range(len(table)): #добавл все что после P0
        for j in range(len(A[0])):
            table[i].append(A[i][j])
    return table
def exists_poz_delt(table, c):# проверка что нужно делать следующию итерацию
    delta = [sum(table[j][1] * table[j][i + 2] for j in range(len(table))) - (c[i - 1] if i > 0 else 0)
                  for i in range(len(table[0]) - 2)]
    max_delta = max(delta[1:], default=0)
    return max_delta >= 0 #возрат true or false
def ind_in_ind_out(table, c): # возвращается индексы что на что меняем
    delta = [sum(table[j][1] * table[j][i + 2] for j in range(len(table))) - (c[i - 1] if i > 0 else 0)
                  for i in range(len(table[0]) - 2)]
    max_delta = max(delta[1:], default=0)
    ind_in = delta.index(max_delta)
    min = BIG_NUM
    ind_out = BIG_NUM
    for i in range(len(table)):# находим минимальное отношение и индес
        if table[i][ind_in+2]>0:
            if min > (table[i][2] /table[i][ind_in+2]):# ищем min
                min = (table[i][2] /table[i][ind_in+2]) # отношение деления
                ind_out = table[i][0]  # индекс вектора который должен уйти
    if min !=BIG_NUM:
        return ind_in , ind_out
    else:
        Exception("Не имеет решения")
def simplex(c, A, b, signs):
    len_A = len(A[0])
    c = type(MIN, c) # 1 step
    b, A, signs = check_P0(b, A, signs) # 2 step
    A,c  = check_signs(A, c, signs) # 3 step
    A,c = check_basis(A, c, init_basis(A)) # 4 step
    table = init_table(A, c, b)
    # Получаем количество столбцов в таблице
    num_columns = len(table[0])
    # Создаем заголовки динамически
    headers = ["b", "Cb"] + [f"P{i}" for i in range(num_columns - 2)]
    # Выводим таблицу
    print("First table:")
    print(tabulate(table, headers=headers, tablefmt="pipe"))
    while exists_poz_delt(table, c) :
        ind_in, ind_out = ind_in_ind_out(table, c)
        table = recount(table, ind_in, ind_out)
        if ind_in == ind_out:
            break
    x_list = [0]*len_A
    for i in range(len(signs)):
        if  i< len(table) and table[i][0]-1 < len(x_list):
            x_list[table[i][0]-1] = table[i][2]
    #///////////////////////////
    # Получаем количество столбцов в таблице
    num_columns = len(table[0])

    # Создаем заголовки динамически
    headers = ["b", "Cb"] + [f"P{i}" for i in range(num_columns - 2)]

    # Выводим таблицу
    print("Last table:")
    print(tabulate(table, headers=headers, tablefmt="pipe"))

    print()


    if any(row[1] == BIG_NUM for row in table):
        print("Искусственный базис не ушел из решения")
        return

    f_x = sum(row[1] * row[2] for row in table)
    print("x =", x_list)
    print("f(x) =", round(f_x, 2) * (1 if MIN else -1))
    return x_list


def recount(table, ind_in, ind_out):
    # Находим индекс базиса который ибираем
    ind_bas = next(i for i, row in enumerate(table) if row[0] == ind_out)

    # Находим коэффициент для нормирования вектора
    kef = 1 / table[ind_bas][ind_in + 2]

    # Обновляем значения в строке с помощью list comprehension
    table[ind_bas][2:] = [round(val * kef, 2) for val in table[ind_bas][2:]]

    # Обновляем значения индекса и коэффициента в строке
    table[ind_bas][0] = ind_in # индекс базиса b
    table[ind_bas][1] = c[ind_in - 1]   # Cb

    # Пересчитываем остальные строки
    for i, row in enumerate(table):
        if i != ind_bas:
            kef = (-1) * row[ind_in + 2]
            table[i][2:] = [round(row_val + kef * index_row_val, 2) for row_val, index_row_val in
                            zip(row[2:], table[ind_bas][2:])]#кортеж из массивов

    return table


delta = []
BIG_NUM = 99999  # бесконечно большое число

MIN = False

c = [3,4,5,6]           # Целевая функция
A = [
    [5, 6, 4, 1],  # Ограничения
    [5, 4, 6, 9],
    [1, 2, 1, 3]
]

b = [400,500,100]              # Вектор Р0
signs = [-1, -1, -1]          # знаки   -1 is <=  // 0 is  =  // 1 is  >=



try:
    x = simplex(c, A, b, signs)
except ValueError as e:
    print("Ошибка: ", e)







