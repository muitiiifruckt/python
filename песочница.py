import heapq



def identity(numRows, numCols, val=1, rowStart=0):
   return [[(val if i == j else 0) for j in range(numCols)]
               for i in range(rowStart, numRows)]



def standardForm(cost, greaterThans=[], gtThreshold=[], lessThans=[], ltThreshold=[],
                equalities=[], eqThreshold=[], maximization=True):
   newVars = 0
   numRows = 0
   if gtThreshold != []:
      newVars += len(gtThreshold)
      numRows += len(gtThreshold)
   if ltThreshold != []:
      newVars += len(ltThreshold)
      numRows += len(ltThreshold)
   if eqThreshold != []:
      numRows += len(eqThreshold)

   if not maximization:
      cost = [-x for x in cost]

   if newVars == 0:
      return cost, equalities, eqThreshold

   newCost = list(cost) + [0] * newVars

   constraints = []
   threshold = []

   oldConstraints = [(greaterThans, gtThreshold, -1), (lessThans, ltThreshold, 1),
                     (equalities, eqThreshold, 0)]

   offset = 0
   for constraintList, oldThreshold, coefficient in oldConstraints:
      constraints += [c + r for c, r in zip(constraintList,
         identity(numRows, newVars, coefficient, offset))]

      threshold += oldThreshold
      offset += len(oldThreshold)

   return newCost, constraints, threshold


def dot(a,b):
   return sum(x*y for x,y in zip(a,b))

def column(A, j):
   return [row[j] for row in A]

def transpose(A):
   return [column(A, j) for j in range(len(A[0]))]

def isPivotCol(col):
   return (len([c for c in col if c == 0]) == len(col) - 1) and sum(col) == 1

def variableValueForPivotColumn(tableau, column):
   pivotRow = [i for (i, x) in enumerate(column) if x == 1][0]
   return tableau[pivotRow][-1]


def initialTableau(c, A, b):
   tableau = [row[:] + [x] for row, x in zip(A, b)]
   tableau.append([ci for ci in c] + [0])
   return tableau


def primalSolution(tableau):
   # столбцы с опорными элементами определяют, какие переменные используются
   columns = transpose(tableau)
   indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]
   return [(colIndex, variableValueForPivotColumn(tableau, columns[colIndex]))
            for colIndex in indices]


def objectiveValue(tableau):
   return -(tableau[-1][-1])


def canImprove(tableau):
   lastRow = tableau[-1]
   return any(x > 0 for x in lastRow[:-1])



def moreThanOneMin(L):
   if len(L) <= 1:
      return False

   x,y = heapq.nsmallest(2, L, key=lambda x: x[1])
   return x == y


def findPivotIndex(tableau):
   # выбираем минимальный положительный индекс
   column_choices = [(i,x) for (i,x) in enumerate(tableau[-1][:-1]) if x > 0]
   column = min(column_choices, key=lambda a: a[1])[0]


   if all(row[column] <= 0 for row in tableau):
      raise Exception('Линейная программа не ограничена.')

   # проверяем на вырожденность: более одного минимизатора квотиента
   quotients = [(i, r[-1] / r[column])
      for i,r in enumerate(tableau[:-1]) if r[column] > 0]


   # выбираем индекс строки, минимизирующий квотиент
   row = min(quotients, key=lambda x: x[1])[0]

   return row, column


def pivotAbout(tableau, pivot):
   i,j = pivot

   pivotDenom = tableau[i][j]
   tableau[i] = [x / pivotDenom for x in tableau[i]]

   for k,row in enumerate(tableau):
      if k != i:
         pivotRowMultiple = [y * tableau[k][j] for y in tableau[i]]
         tableau[k] = [x - y for x,y in zip(tableau[k], pivotRowMultiple)]

def simplex(c, A, b):

   tableau = initialTableau(c, A, b)
   print("Начальная таблица:")
   for row in tableau:
      row = (row[-1], *row[:-1])
      print(row)
   print()

   while canImprove(tableau):
      pivot = findPivotIndex(tableau)
      print("Следуюий индекс таблицы=%d,%d \n" % pivot)
      pivotAbout(tableau, pivot)
      index_of_basis[pivot[0]] = pivot[1] + 1
      print(index_of_basis)
      print("Таблица:")
      for row in tableau:
         row = (row[-1], *row[:-1])
         print(row)
      print()

   return tableau, primalSolution(tableau), objectiveValue(tableau)


if __name__ == "__main__":
   # Задаём значения целевой функ   ции, вектораограничений
   #    и
   #    правой
   #    стороны

   c = [3,4,5,6]
   A = [[5,6,4,1], [5,4,6,8],[1,2,1,3]]
   b = [400,500,100] # положиельные

   min_1 = False
   first_c = c.copy()

   len_of_x = len(A[0])  # Число значимых переменных

   # Вводим базис
   c_basis = list()
   for i in range(len(A)):
      basis = list()
      c_basis.append(0)

      for j in range(len(A)):
         basis.append(1 if i == j else 0)
      A[i] += basis
   # Дополняем целевую функцию
   c += c_basis
   index_of_basis = list()
   for i in range(len(b)):
      index_of_basis.append(len(c) - i)
   index_of_basis = index_of_basis[::-1]

   # ЗАПУСК РЕШЕНИЯ
   try:
      t, s, v = simplex(c, A, b)
      solution = list()  # Итоговое значения вектора значений
      for i in range(len_of_x):  # подготовка ответов
         if(i>=len(s)):
            solution.append(0)
         elif():
            solution.append(s[i][1])

      # Вывод оптимальных значений
      print(s)
      print(f"Значения вектора х : {solution}")
      print(f"Оптимальное значение функции: {(v*(-1) if min_1 else v) }")
      print(index_of_basis)
   except Exception:
      print("Нет решения")