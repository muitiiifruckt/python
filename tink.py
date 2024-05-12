import random
import math
from tkinter import *
from tkinter import filedialog, messagebox

def power(x, y, p):
    # Быстрое возведение в степень по модулю
    res = 1
    x = x % p

    while y > 0:
        if y & 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p

    return res

def miller_rabin_test(n, r=None):
    if n <= 1:
        return False
    if n <= 3:
        return True

    if r is None:
        r = max(1, int(math.log10(n)))

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(r):
        a = random.randint(2, n - 2)
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(l):
    sym = l//8
    left = 10**(sym-1)
    right = 10**sym
    while True:
        p = random.randrange(left+1, right, 2)
        if miller_rabin_test(p):
            break

def check_prime(n, r):
    if n == '':
        messagebox.showinfo("Ошибка!", "Введите число в поле")
        textbox1.delete("1.0", "end")
        textbox2.delete("1.0", "end")
    else:
        n = int(n.strip())
        if r == '':
            r = None
        else: r = int(r.strip())

        result = miller_rabin_test(n, r)
        if result:
            messagebox.showinfo("Результат", f"{n} - вероятно простое")
        else:
            messagebox.showinfo("Результат", f"{n} - составное")

def check_prime_with_rounds(p, n):
    result = miller_rabin_test(p, n)
    if result:
        return f"{p} - возможно простое"
    else:
        return f"{p} - составное"

def check_file():
    filename = filedialog.askopenfilename()
    if not filename:
        return

    output_filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if not output_filename:
        return

    with open(filename, 'r') as file:
        with open(output_filename, 'w') as output_file:
            for line in file:
                nums = line.strip().split()
                if len(nums) == 1:
                    p = int(nums[0])
                    n = int(math.log2(p))
                elif len(nums) == 2:
                    p = int(nums[0])
                    n = int(nums[1])
                else:
                    messagebox.showerror("Ошибка", "Неверный формат файла")
                    return

                result = check_prime_with_rounds(p, n)
                output_file.write(result + '\n')

    messagebox.showinfo("Готово", f"Результаты сохранены в файле: {output_filename}")



window = Tk()  # создание окна
window.title('Алгоритм Миллера-Рабина')  # название окна
window.geometry('300x300')  # размеры окна
window.resizable(False, False)  # растягивание окна

label1 = Label(window, text="Введите число для проверки:", height=2)
label1.place(x=50, y=10)

label2 = Label(window, text="Введите количество итераций:", height=2)
label2.place(x=50, y=80)

label3 = Label(window, text="Выберите файл для проверки", height=2)
label3.place(x=50, y=200)

textbox1 = Text(window, wrap=WORD, width=20, height=1, padx=5, pady=5)
textbox1.place(x=50, y=40)

textbox2 = Text(window, wrap=WORD, width=20, height=1, padx=5, pady=5)
textbox2.place(x=50, y=110)

button1 = Button(window, text='Проверить', width=10, command=lambda: check_prime(textbox1.get("1.0", "end-1c"), textbox2.get("1.0", "end-1c")), padx=5)
button1.place(x=80, y=160)


button2 = Button(window, text='Выбор файла', width=10, command=lambda: check_file())
button2.place(x=80, y=240)

window.mainloop()
