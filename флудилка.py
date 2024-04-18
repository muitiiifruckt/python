import copy
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
            nedostayochiy_basis.append( basis)
            index_of_basis.append(i)

    return nedostayochiy_basis
def zapolneniye_A_nedostayochimi_basisami(A,c, nedostayochiy_basis):
    # на вход матрица А  на выходе матрица А со всеми базисами
    W = 99999  # бесконечно большое число
    if nedostayochiy_basis: #  само добавление недостающего базиса
        for j in range(len(nedostayochiy_basis[0])):
            for i in range(len(nedostayochiy_basis)):
                A[j].append(nedostayochiy_basis[i][j])
            c.append(W)
        return A,c
    else: #  если базис не надо добавлять то все ок
        return A,c
def proverka_right_na_poloshitelnost(b ,A ,znaki):
    # домножение на -1 если справа отрицательное число
    for i in range(len(b)):
        if b[i]<0:
            b[i] = b[i]*(-1) # умножаем правою сторону на -1
            znaki[i] = znaki[i]*(-1) # меняем знак уравнения
            for j in range(len(A[i])):  # меняем  знаки левой части уравнения
               A[j] = A[j]*(-1)
    return b,A,znaki
def min_max(minimization,c):
    if not minimization:
        for i in range(len(c)):
            c[i] = c[i]*(-1)
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

            skal_sum +=round(table[j][1]*table[j][i+2],2)
        if i>0:
            delta_list[i] = skal_sum -c[i-1]
        else:
            delta_list[i] = skal_sum

    max_delta = max(delta_list[1:])
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
                index_of_last_basis = table[i][0]  # индекс вектора который должен уйти
    if min !=999999:
        return index_of_poloz_delta , index_of_last_basis
    else:
        Exception("Не имеет решения")
# ч и т а й  м е ж  с т р о к
# н е т  ц е л и
# е с т ь  т о л ь к о  к о д
def simplex(c,A,b,znaki,dlina_basisa):
    c = min_max(minimization,c) # 1 step
    b, A,znaki = proverka_right_na_poloshitelnost(b,A,znaki) # 2 step
    A,c  = prividenie_k_ravenstvam(A,c,znaki) # 3 step
    A,c = zapolneniye_A_nedostayochimi_basisami(A,c ,create_nedostayochiy_basis(A)) # 4 step



    table = create_first_table(A,c,b)
    index_of_poloz_delta= 0
    index_of_last_basis = 0

    while count_delta(table,c) :
        for i in range(len(table)):
            print(table[i])
        index_of_poloz_delta, index_of_last_basis = count_delta_and_index_out_and_in(table,c)
        table = perechet(table,index_of_poloz_delta , index_of_last_basis)
        if index_of_poloz_delta == index_of_last_basis:
            break
    list_of_x = [0]*dlina_basisa
    for i in range(len(znaki)):
        if  i< len(table) and table[i][0]-1 < len(list_of_x):
            list_of_x[table[i][0]-1] =  table[i][2]
    print("Table")
    for i in range(len(table)):
        print(table[i])
    print()
    for i in range(len(table)): # если в базисе останется
        if table[i][1] == 99999:
            print("Не имеет решния, искусственый базис не ушел из решения")
            return
    f_x = 0
    for i in range(len(znaki)):
        f_x +=table[i][1]*table[i][2]
    print("x ",list_of_x)
    print()
    print("f(x)=" , round(f_x,2) * 1 if minimization else round(f_x,2)*(-1))
    return list_of_x
def analize_chuyvstvitelnost(cc,A,znaki,b,x,dlina_basisa):
    n = 5 # 2 в степени n шаг
    num_to_inf =2
    inf = 99999999999
    step = pow(2,n)
    c_up_actual = copy.deepcopy(cc)
    c_down_actual = copy.deepcopy(cc)
    for i in range(len(cc)):
        list_up = list()
        list_down = list()
        # up
        step = pow(2, n)
        for j in range(n+1): # схоже на бинарный поиск ну типо иду с шагом 32 например пока все потом шагом 16 и так далее пока шаг не олин и ине найду грань
            A_copy = copy.deepcopy(A)
            b_copy = copy.deepcopy(b)
            znaki_copy = copy.deepcopy(znaki)
            count_to_infinity =0
            while True:
                c_up_actual[i] += step
                x_experimental = [0] * len(cc)
                for k in range(len(cc)):
                    x_experimental[k] = c_up_actual[i] if i == k else cc[k]
                x_current = simplex(x_experimental, A_copy, b_copy, znaki_copy, dlina_basisa)
                if not is_equal_x_lists(x,x_current):
                    break
                elif count_to_infinity ==num_to_inf:
                    c_down_actual[i] =  inf
                    break
                A_copy = copy.deepcopy(A)
                b_copy = copy.deepcopy(b)
                znaki_copy = copy.deepcopy(znaki)
                count_to_infinity += 1
            c_up_actual[i] -=step
            step /=2
            if count_to_infinity == num_to_inf:
                break
        step = pow(2, n)
        for j in range(n + 1):  # схоже на бинарный поиск ну типо иду с шагом 32 например пока все потом шагом 16 и так далее пока шаг не олин и ине найду грань
            A_copy = copy.deepcopy(A)
            b_copy = copy.deepcopy(b)
            znaki_copy = copy.deepcopy(znaki)
            count_to_infinity = 0
            while True:
                c_down_actual[i] -= step
                x_experimental = [0]*len(cc)
                for k in range( len(cc)):
                    x_experimental[k] = c_down_actual[i] if i==k else cc[k]
                x_current = simplex(x_experimental, A_copy, b_copy, znaki_copy, dlina_basisa)
                if not is_equal_x_lists(x, x_current) :
                    break
                elif count_to_infinity ==num_to_inf:
                    c_down_actual[i] =  inf*(-1)
                    break
                c_down_actual[i] -= step
                A_copy = copy.deepcopy(A)
                b_copy = copy.deepcopy(b)
                znaki_copy = copy.deepcopy(znaki)
                count_to_infinity +=1
            c_down_actual[i] += step
            step /= 2
            if count_to_infinity == num_to_inf:
                break
    return c_down_actual,c_up_actual


def is_equal_x_lists(x,current_x):
    if not current_x:
        return False
    for i in range(len(x)):
        if(round(x[i]) != round(current_x[i])):
            return False
    return True
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
        table[index_of_1_2_3][i+2] = round(table[index_of_1_2_3][2:][i]*kef,2)
    table[index_of_1_2_3][0] = index_of_poloz_delta
    table[index_of_1_2_3][1] = c[index_of_poloz_delta-1]
    rows = range(len(table))
    for i in rows:  # пересчет остальных строк
        if i!=index_of_1_2_3:
            kef = (-1)*table[i][index_of_poloz_delta+2]
            for j in range(len(table[i][2:])):
                table[i][j+2] = round(table[i][2:][j] + kef*table[index_of_1_2_3][2:][j],2)
    return table

delta_list = list()


# Задаем входные параметры  для целевой, мин/макс , ограничения, правая сторона ограничений , знаки
minimization = False

c = [3,4,5,6]           # Целевая функция
A = [ [5,6,4,1],        # Ограничения
      [5,4,6,9],
      [1,2,1,3]
      ]

b = [400,500,100]              # Вектор Р0
znaki = [-1,-1,-1]          # знаки   -1 is <=  // 0 is  =  // 1 is  >=
cc = copy.deepcopy(c)
AA = copy.deepcopy(A)
bb = copy.deepcopy(b)
znaki_znaki = copy.deepcopy(znaki)

dlina_basisa = len(A[0])
try:
    x =simplex(c, A, b, znaki, dlina_basisa)
    xx = copy.deepcopy(x)
    down_c, up_c = analize_chuyvstvitelnost(cc,AA,znaki_znaki,bb,xx,dlina_basisa)
    for i in range(len(up_c)):
        print(down_c[i],"           ",up_c[i])
except Exception:
    print("Не имееет решения")








