from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from math import *
import sys
import re

root = Tk()
root.title("Calculator")
root.geometry("646x848+200+200")

btns = [
    "C", "DEL", "Exit", "!", "%", "=",
    "MC", "MS", "MR", "M+", "M-", "ln",
    "1", "2", "3", "/", "sin", "lg",
    "4", "5", "6", "+", "cos", "e",
    "7", "8", "9", "-", "tan", "π",
    "(", "0", ")", "*", "файл", "save",
    ".", ",", "√", "xⁿ", "[", "]",
    "sum", "arith", "vid", "+const", "const"
]

x = 10
y = 110
for bt in btns:
    com = lambda x=bt: calc(x)
    Button(text=bt, bg="SkyBlue1",
           font=("Times New Roman", 30),
           command=com).place(x=x, y=y,
                              width=98,
                              height=60)

    x += 100
    if x > 600:
        x = 15
        y += 71

calc_entry = Entry(root, width=43, font=("Times New Roman", 28, "bold"), bg="snow")
calc_entry.grid(row=2, column=3, columnspan=4)


def replace(a):
    return a.replace('^', '**').replace('%', '*0.1').replace('ln', 'log').replace('lg', 'log10').replace('√',
                                                                                                         'sqrt').replace(
        'π', 'pi')


def add_factorial(a):
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
    global memory
    global constant

    if key == "=":
        # try:
        const = open('const.txt', 'r')

        lst = []
        constant = {}

        for line in const:
            lst = line.split(',')
            constant[lst[0]] = str(lst[1]).strip()
        print(constant)

        vyras = calc_entry.get()

        symb = '[(+-/*)]'
        vyras_new = re.split(symb, vyras)
        for i in range(len(vyras_new)):
            for keys in constant:
                if keys == vyras_new[i]:
                    znachenya = constant[vyras_new[i]]
                    indx = vyras.index(vyras_new[i][0])
                    vyras = vyras[:indx] + str(znachenya) + vyras[indx + len(vyras_new[i]):]
                    print(vyras)

        history = open('history.txt', 'a+')
        line = str(vyras)
        result = str(eval(replace(add_factorial(obrahynki(vyras)))))
        row = str(line + '=' + result + "\n")
        history.write(row)

        calc_entry.delete(0, END)
        calc_entry.insert(0, str(result))

        history = open('history.txt', 'r')
        add = history.read()
        history = open('history.txt', 'w')
        result = str(eval(replace(add_factorial(vyras))))
        new = str(line + '=' + result + "\n" + add)
        history.write(new)

        # except:
        # messagebox.showerror('ERROR',"ПОМИЛКА")

    elif key == 'const':
        const = open('const.txt', 'r')

        constants = Tk()
        constants.title('Constants')

        fhandle = open('const.txt', 'r')
        i = 0
        for line in fhandle:
            lable = Label(constants, text=line, font=('Times New Roman', 13)).grid(row=i)
            i += 1

        mainloop()


    elif key == "+const":
        const = open('const.txt', 'a+')
        const.write('\n' + calc_entry.get())


    elif key == "save":
        save = open('save.txt', 'a+')
        history = open('history.txt', 'r')
        hist = history.readline()
        save.write(hist)

        save == open('save.txt', 'r')
        add = save.read()
        save = open('save.txt', 'a+')
        save.write(add)



    elif key == "файл":
        file = open('file.txt', 'r')
        add = file.read()
        calc_entry.insert(END, add)



    elif key == "C":
        calc_entry.delete(0, END)

    elif key == "DEL":
        display = calc_entry.get()
        if len(display):
            new = display[:-1]
            calc_entry.delete(0, END)
            calc_entry.insert(0, new)
        else:
            calc_entry.delete(0, END)
            calc_entry.insert(0, "Error")

    elif key == "Exit":
        root.after(1, root.destroy)
        sys.exit
        history = open('history.txt', 'w')
        history.write('')
        save = open('save.txt', 'w')
        save.write('')


    elif key == "xⁿ":
        calc_entry.insert(END, "^")


    elif key == "%":
        calc_entry.insert(END, "%")


    elif key == "√":
        try:
            calc_entry.insert(END, "√" + '(')
        except:
            messagebox.showerror('ERROR', "Корінь з від'ємного числа")



    elif key == "(":
        calc_entry.insert(END, "(")

    elif key == ")":
        calc_entry.insert(END, ")")



    elif key == "lg":
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
        calc_entry.insert(END, 'e')


    elif key == "π":
        calc_entry.insert(END, 'π')



    else:
        if "=" in calc_entry.get():
            calc_entry.delete(0, END)
        calc_entry.insert(END, key)

    calc = open('memory.txt')

    if key == "MS":
        calc = open('memory.txt', 'w')
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(0, new)
        calc.write(new)

    elif key == 'MR':
        calc = open('memory.txt', 'r')
        line = calc.read()
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(END, str(new) + str(line))

    elif key == 'MC':
        calc = open('memory.txt', 'w')
        calc.write('')
        f = calc_entry.get()
        new = f[0:-2]
        calc_entry.delete(0, END)
        calc_entry.insert(0, new)

    elif key == 'M+':
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
