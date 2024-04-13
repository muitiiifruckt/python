
def find_basis_in_first_table(A): # не нужно
    # na vhod matrix A - ogranicheniya
    # this func return the all basis , if he has
    baz_imeyuchisa = list() # this list for basis, if he had
    for i in A:
        count_0 = 0
        count_1 = 0
        for j in i:
            if (j==1):
                count_1 +=1
            elif (j==0):
                count_0
        if( count_1 == 1 and (count_0 + 1 == len(i)) ):
            # is basis and
            baz_imeyuchisa.append(i)
    return baz_imeyuchisa
def create_nedostayochiy_basis(A):
    # na vhod matrix b of founded_basis_in_first_table
    # return nedostayochiy basis
    razmer_of_basis = len(A)
    nedostayochiy_basis = list()
    index_of_basis = list()

    A_columns_s = [0]*len(A[0]) # задаем двумерный массив столбцов
    for i in range(len(A[0])):
        A_columns_s[i] = [0]*len(A)

    for i in range(len(A)): # теперь это массив столбцов
        for j in range(len(A[i])):
            A_columns_s[j][i] = A[i][j]

    for i in range(razmer_of_basis): # проверяем каких базисов нет в массиве столбцов и тех что нет добавляем в nedostayochiy_basis
        basis = list()

        for j in range(razmer_of_basis):
            basis.append(1 if i==j else 0)
        if not(basis in A_columns_s):
            nedostayochiy_basis += basis
            index_of_basis.append(i)

    return nedostayochiy_basis
def zapolneniye_A_nedostayochimi_basisami(A,c, nedostayochiy_basis):
    # на вход матрица А  на выходе матрица А со всеми базисами
    W = 99999  # бесконечно большое число
    if nedostayochiy_basis: #  само добавление недостающего базиса
        for i in range(len(nedostayochiy_basis)):
            for j in range(len(nedostayochiy_basis[0])):
                A[i].append(nedostayochiy_basis[i][j])
            c.append(W)
        return
    else: #  если базис не надо добавлять то все ок
        return A,c
def proverka_right_na_poloshitelnost(b,A,znaki):
    # домножение на -1 если справа отрицательное число
    for i in range(len(b)):
        if b[i]<0:
            b[i] = b[i]*(-1) # умножаем правою сторону на -1
            znaki[i] = znaki[i]*(-1) # меняем знак уравнения
            for j in range(len(A[i])):# меняем знаки левой части уравнения
               A[j] = A[j]*(-1)
    return b,A,znaki
def min_max(minimization,c):
    if not minimization:
        for i in c:
            i = i*(-1)
    return  c
def prividenie_k_ravenstvam(A,c,znaki):
    for i in range(len(znaki)):
        if znaki[i] == -1: #   <=
            for k in range(len(A)): # добавляем новую переменную в ограничения матрицы А
                A[k].append(1 if k==i else 0)
            c.append(0) # в целевую доп переменные идут с кэфом 0
        elif znaki[i] == 1:  #  >=
            for k in range(len(A)): # добавляем новую переменную в ограничения матрицы А
                A[k].append(-1 if k==i else 0)
            c.append(0) # в целевую доп переменные идут с кэфом 0
        elif znaki[i] ==0: #  =
            pass # все ок ниче не делаем
    return A,c
def create_first_table(A,c,b): # возвращает чисто таблицу без дельта
    # table  / b/cb/p0/p1/p2...
    #        / p3/ kef/ kef/kef
    # надо найти индексы базисов, тобишь какой Р соответсвтуует столдбк=цу (1,0,0) и так далее
    index_of_bas = list()
    A_columns_s = [0] * len(A[0])  # задаем двумерный массив столбцов
    for i in range(len(A[0])):
        A_columns_s[i] = [0] * len(A)

    for i in range(len(A)):  # теперь это массив столбцов
        for j in range(len(A[i])):
            A_columns_s[j][i] = A[i][j]

    for i in range(len(b)): # проверяем каких базисов нет в массиве столбцов и тех что нет добавляем в nedostayochiy_basis
        basis = list()
        for j in range(len(b)):
            basis.append(1 if i==j else 0)
        for k in range(len(A_columns_s)):
            if basis == A_columns_s[k]:
                index_of_bas.append(k+1)
    # получили индексы базисов по порядку, строим таблицу
    table = index_of_bas.copy() # базисы / b
    for i in range(len(table)):
        table[i]= [table[i],c[table[i]-1]]# cb / кэфы от целевой
        table[i].append(b[i]) #  P0
    for i in range(len(table)): # добавление всех Р1 Р2 и так далее
        for j in range(len(A[0])):
            table[i].append(A[i][j])
    return table
def count_delta(table,c): # возвращается индексы что на что меняем
    delta_list = [0]*(len(table[0] )- 2 ) # первые два столбец не нужен для счета дельты
    for i in range(len(table[0])-2):
        skal_sum = 0
        for j in range(len(table)):
            pp =table[j][1]
            ppp = table[j][i+2]

            skal_sum +=table[j][1]*table[j][i+2]
        if i>0:
            delta_list[i] = skal_sum -c[i-1]
        else:
            delta_list[i] = skal_sum

    max_delta = max(delta_list[1:])
    if(max_delta<=0):
        print(delta_list)
        return False
    else:
        return True
def count_delta_and_index_out_and_in(table,c): # возвращается индексы что на что меняем
    delta_list = [0]*(len(table[0] )- 2 ) # первые два столбец не нужен для счета дельты
    for i in range(len(table[0])-2):
        skal_sum = 0
        for j in range(len(table)):
            pp =table[j][1]
            ppp = table[j][i+2]

            skal_sum +=table[j][1]*table[j][i+2]
        if i>0:
            delta_list[i] = skal_sum -c[i-1]
        else:
            delta_list[i] = skal_sum

    max_delta = max(delta_list[1:])
    if(max_delta<=0):
        return -999999 # пересчетов больше не будет
    index_of_poloz_delta = delta_list.index(max_delta)
    # мы получили максимальную дельту теперь найдем индекс вeктора, который уйдет из базиса
    # ищем минимальное отношение
    min  = 999999
    index_of_last_basis = 999
    for i in range(len(table)):
        p = table[i][index_of_poloz_delta+2]
        if table[i][index_of_poloz_delta+2]>0:
            pp =table[i][2]
            if min > (table[i][2] /table[i][index_of_poloz_delta+2]):
                min = (table[i][2] /table[i][index_of_poloz_delta+2]) # отношение деления
                index_of_last_basis = table[i][0]  # индекс ветора который должен уйти
    if min:
        return index_of_poloz_delta , index_of_last_basis
def simplex(c,A,b,znaki,dlina_basisa):
    c = min_max(minimization,c) # 1 step
    b, A,znaki = proverka_right_na_poloshitelnost(b,A,znaki) # 2 step
    A,c  = prividenie_k_ravenstvam(A,c,znaki) # 3 step
    A,c = zapolneniye_A_nedostayochimi_basisami(A,c ,create_nedostayochiy_basis(A)) # 4 step



    table = create_first_table(A,c,b)
    index_of_last_basis = 0
    index_of_last_basis = 0

    while count_delta(table,c) :
        table = perechet(table, *count_delta_and_index_out_and_in(table,c))
    list_of_x = [0]*dlina_basisa
    for i in range(len(A)):
        list_of_x[table[i][0]-1] =  table[i][2]
    print(table)
    print(list_of_x)
def perechet(table,index_of_poloz_delta , index_of_last_basis):
    for i in range(len(table)):
        for j in range(len(table)):
            float(table[i][j])
    index_of_1_2_3 = 0
    for i in range(len(table)):
        if table[i][0]==index_of_last_basis:
            index_of_1_2_3 = i
    kef = 1/ table[index_of_1_2_3][index_of_poloz_delta+2] # нормаруем вектор, точнее находим кэф
    for i in range(len(table[index_of_1_2_3][2:])): # разделили нову строку на кэф чтобы базис был с 1
        p = table[index_of_1_2_3][2:][i]
        pp = table[index_of_1_2_3][2:][i]*kef
        table[index_of_1_2_3][i+2] = table[index_of_1_2_3][2:][i]*kef
    table[index_of_1_2_3][0] = index_of_poloz_delta
    table[index_of_1_2_3][1] = c[index_of_poloz_delta-1]
    rows = range(len(table))
    for i in rows:  # пересчет остальных строк
        if i!=index_of_1_2_3:
            kef = (-1)*table[i][index_of_poloz_delta+2]
            for j in range(len(table[i][2:])):
                table[i][j+2] = table[i][2:][j] + kef*table[index_of_1_2_3][2:][j]
    return table


# нужно разораться со знаками, типо сначала урегулировать вопрос со знаками (случай зависит отзнака)
# затем перейти уже к реализации симплекса самого


minimization = True
c = [2,-1,3,-10,1]
A = [ [0,1,0,2,0],
      [1,0,2,-1,0],
      [0,0,-1,-2,1]

]
dlina_basisa = len(A[0])
b = [4,4,6]
znaki = [0,0,0] #  -1 is <=   0 is  =   1 is  >=
simplex(c,A,b,znaki,dlina_basisa)




