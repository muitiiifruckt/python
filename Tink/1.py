
def find_special_segment(n, grades):
    if n<=6:
        return -1
    max_fives = 0
    for i in range(n - 7 +1):
        local_max_fives = how_fives(grades[i:i+7])
        max_fives = max(local_max_fives,max_fives)
        if max_fives == 7:
            return max_fives
    return max_fives if max_fives!=0 else -1
def how_fives(string):
    fives = 0
    for num in string:
        if num==5:
            fives +=1
        elif num == 3 or num == 2:
            return 0
    return fives

# # Чтение входных данных
n = int(input())
grades = list(map(int, input().split()))

# Поиск ответа и вывод результата
print(find_special_segment(n, grades))

