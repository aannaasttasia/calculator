from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from math import *
import re

# створюємо вікно нашого калькулятора

root = Tk()
root.title("Calculator")
root.geometry("646x848+200+200")

# прописуємно назви наших майбутніх кнопок
btns = [
    "C", "DEL", "Exit", "!", "%", "=",
    "MC", "MS", "MR", "M+", "M-", "ln",
    "1", "2", "3", "/", "sin", "lg",
    "4", "5", "6", "+", "cos", "e",
    "7", "8", "9", "-", "tan", "π",
    "(", "0", ")", "*", "file", "save",
    ".", ",", "√", "xⁿ", "[", "]",
    "sum", "arith", "vid", "+const", "const", "attention"
]
# за допомогою цикла прописуємо розміщення наших кнопок у вікні Tk

x = 10
y = 110
for bt in btns:
    com = lambda x = bt: calc(x)
    Button(text=bt, bg="SkyBlue1",
           font=("Times New Roman", 30),
           command=com).place(x=x, y=y,
                              width=102,
                              height=62)

    x += 100
    if x > 600:
        x = 15
        y += 71

# створюємо текстове поле, в якому будуть записуватися значення, які нам потрібно буде обрахувати
calc_entry = Entry(root, width=43, font=("Times New Roman", 28, "bold"), bg="snow")
# задаємо розташування нашого текстового поля
calc_entry.grid(row=5, column=3, columnspan=4)



def replace(a):
    """дана функція заміняє вигляд операцій в полі для вводу тексту(текстове поле)  """
    return a.replace('^', '**').replace('%', '*0.1').replace('ln',
                    'log').replace('lg', 'log10').replace('√', 'sqrt').replace('π', 'pi')


def add_factorial(a):
    """дана функція знаходить факторіал, число, факторіал якого потрібно знайти і обраховує його """
    if '!' in a:
        index = a.index('!')
        i = index
        b = 0
        str = '+-*/^'
        while i >= 0:
            i -= 1
            if a[i] == ')':
                b += 1
            if a[i] == '(':
                b -= 1
            if a[i] in str and not b:
                break
        a = a[:i + 1] + 'factorial(' + a[i + 1:index] + ')' + a[index + 1:]
        print(a)
        return add_factorial(a)
    else:
        return a


def obrahynki(c):
    """дана функція обраховує середнє арифметичне,середньоквадратичне відхилення і суму  значень,
    які задані в квадратних дужках"""
    if 'arith' in c:
        suma = 0
        index = c.index('h') + 2
        i = index
        s = c.index('a')
        lst = []
        n = c[index:]
        last = n.index(']')
        new = str(n[:last])
        lst = new.split(',')
        lst1 = [float(x) for x in lst]
        suma = str(sum(lst1) / int(len(lst1)))
        c = c[:s] + str(suma) + n[last + 1:]
        print(c)
        return obrahynki(c)

    elif 'sum' in c:
        suma = 0
        index = c.index('m') + 2
        i = index
        n = c[index:]
        last = n.index(']')
        lst = []
        new = str(n[:last])
        lst = new.split(',')
        lst = [float(x) for x in lst]
        suma = str(sum(lst))
        s = c.index('s')
        c = c[:s] + str(suma) + n[last + 1:]
        print(c)
        return obrahynki(c)

    elif 'vid' in c:
        suma = 0
        index = c.index('d') + 2
        i = index
        s = c.index('v')
        lst = []
        n = c[index:]
        last = n.index(']')
        new = str(n[:last])
        lst = new.split(',')
        lst1 = [float(x) for x in lst]
        suma = int(sum(lst1) / int(len(lst1)))
        lst2 = []
        display = 0
        for j in lst1:
            j -= suma
            lst2.append(j ** 2)
        for q in lst2:
            display += q
        label = (display / len(lst2)) ** 0.5
        c = c[:s] + str(label) + n[last + 1:]
        print(c)
        return obrahynki(c)

    else:
        return c


constant = {}


def calc(key):
    """дана функція застосовується для всіх кнопок і виконує певні дії при нажатті на них """
    global memory
    global constant
    # при нажатті на кнопку = проводяться всі потрібні обрахунки
    if key == "=":
        # перевірка правильності розстановки дужок
        vyras = calc_entry.get()
        x = vyras.count(')')
        y = vyras.count('(')
        if x != y:
            messagebox.showerror('ERROR', 'НЕВІРНА РОЗСТАНОВКА ДУЖОК')
        else:
            try:
                # зчитування констант з файла
                const = open('const.txt', 'r')

                lst = []
                constant = {}
                # створення словника, в якому ключем є назва константи, а його значенням є число
                for line in const:
                    lst = line.split(',')
                    constant[lst[0]] = str(lst[1]).strip()
                print(constant)

                # розділення по символах і пошук в текстовому полі константи, заміна константи
                symb = '[(+-/*)]'
                vyras_new = re.split(symb, vyras)
                for i in range(len(vyras_new)):
                    for keys in constant:
                        if keys == vyras_new[i]:
                            znachenya = constant[vyras_new[i]]
                            indx = vyras.index(vyras_new[i][0])
                            vyras = vyras[:indx] + str(znachenya) + vyras[indx + len(vyras_new[i]):]
                            print(vyras)

                # збереження історії обчислень
                history = open('history.txt', 'a+')
                line = str(vyras)
                result = str(eval(replace(add_factorial(obrahynki(vyras)))))
                row = str(line + '=' + result + '\n')
                history.write(row)

                # виведення результату обрахунків
                calc_entry.delete(0, END)
                calc_entry.insert(0, str(result))

                history = open('history.txt', 'r')
                add = history.read()
                history = open('history.txt', 'w')
                result = str(eval(replace(add_factorial(obrahynki(vyras)))))
                new = str(line + '=' + result + "\n" + add)
                history.write(new)

            # прописання усіх можливих помилок
            except ZeroDivisionError:
                # ділення на нуль
                messagebox.showerror('ERROR', "devision by zero")
            except ValueError:
                # некоректне введення
                messagebox.showerror('ERROR', "your value is incorrect")
            except SyntaxError:
                messagebox.showerror('ERROR', "attention,please")
            except NameError:
                messagebox.showerror('ERROR', "do not defined, chek again")

    elif key == 'const':
        # при нажатті на кнопку виведення вікна з,доданити користувачем, константами
        const = open('const.txt', 'r')

        constants = Tk()
        constants.title('Constants')
        constants.geometry('230x200+100+200')

        fhandle = open('const.txt', 'r')
        i = 0
        for line in fhandle:
            lable = Label(constants, text=line, font=('Times New Roman', 13)).grid(row=i)
            i += 1

        mainloop()

    elif key == '+const':
        # додавання констант у файл
        messagebox.showinfo('attention', 'click "attention" ')
        const = open('const.txt', 'a+')
        const.write('\n' + calc_entry.get())

    elif key == "attention":
        # виведення вікна з інформацією про правильність запису констант
        messagebox.showinfo('Attention', "if you want to use own constants, you should write their as 'letter,"
                            "digit'. You can not use letter 's, u, m, v, i, d, t, h, a, r'")

    elif key == "save":
        # збереження історії за запитом користувача
        save_new = open('save_new.txt', 'a+')
        history = open('history.txt', 'r')
        hist = history.readline()
        save_new.write(hist)

        save_new == open('save_new.txt', 'r')
        add = save_new.read()
        save_new = open('save_new.txt', 'a+')
        save_new.write(add)

    elif key == "file":
        # зчитування виразу з файла для обрахунків і виведення його на екран
        file = open('file.txt', 'r')
        add = file.read()
        calc_entry.insert(END, add)

    elif key == "C":
        # очищення текстового поля
        calc_entry.delete(0, END)

    elif key == "DEL":
        # видалення останнього елементу
        display = calc_entry.get()
        if len(display):
            new = display[:-1]
            calc_entry.delete(0, END)
            calc_entry.insert(0, new)
        else:
            calc_entry.delete(0, END)
            calc_entry.insert(0, "Error")

    elif key == "Exit":
        # закрити калькулятора
        root.after(1, root.destroy)
        history = open('history.txt', 'w')
        history.write('')
        save_new = open('save_new.txt', 'w')
        save_new.write('')

    elif key == "xⁿ":
        # піднесення до степеня
        calc_entry.insert(END, "^")

    elif key == "%":
        # обрахування відсотків
        calc_entry.insert(END, "%")

    elif key == "√":
        # обчислення кореня
        calc_entry.insert(END, "√" + '(')

    elif key == "(":
        # запис дужки в текстове поле
        calc_entry.insert(END, "(")

    elif key == ")":
        # запис дужки в текстове поле
        calc_entry.insert(END, ")")

    elif key == "lg":
        # запис логарифма
        calc_entry.insert(END, 'lg(')

    elif key == "ln":
        calc_entry.insert(END, 'ln(')

    elif key == "sin":
        calc_entry.insert(END, 'sin' + '(')

    elif key == "cos":
        calc_entry.insert(END, 'cos' + '(')

    elif key == "tan":
        calc_entry.insert(END, 'tan' + '(')

    elif key == "e":
        # запис експоненти
        calc_entry.insert(END, 'e')

    elif key == "π":
        # запис числа пі
        calc_entry.insert(END, 'π')

    else:
        if "=" in calc_entry.get():
            calc_entry.delete(0, END)
        calc_entry.insert(END, key)

    calc = open('memory.txt')
    # відкриття файлу для пам'яті

    if key == "MS":
        # збереження числа в пам'ять
        calc = open('memory.txt', 'w')
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(0, new)
        calc.write(new)

    elif key == 'MR':
        # виведення числа в поле для вводу тексту
        calc = open('memory.txt', 'r')
        line = calc.read()
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(END, str(new) + str(line))

    elif key == 'MC':
        # видалення числа
        calc = open('memory.txt', 'w')
        calc.write('')
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(0, new)

    elif key == 'M+':
        # збільшення значення числа
        calc = open('memory.txt', 'r')
        line = calc.read()
        calc = open('memory.txt', 'w')
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(0, new)
        num = int(line) + int(calc_entry.get())
        calc.write(str(num))

    elif key == 'M-':
        # зменшення значення числа
        calc = open('memory.txt', 'r')
        line = calc.read()
        calc = open('memory.txt', 'w')
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(0, new)
        num = int(line) - int(calc_entry.get())
        calc.write(str(num))

    calc.close()


root.mainloop()
