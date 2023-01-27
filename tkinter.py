import tkinter as tk

def say_hello():
    print('hello')

def add_label():
    label = tk.Label(win, text='new')
    label.pack()

def counter():
    global count
    count+=1
    btn4['text'] = f'Счетчик: {count}'

def btn_disable():
    btn1['state'] = tk.DISABLED

count = 0

win = tk.Tk()
win.title('Приложение')  # заголовок окна
win.geometry('400x500+100+200')  # размеры окна и положение при появлении
#win.resizable(True, True)  # изменение размеров окна
#win.minsize(300, 300)  # мин размер окна, maxsize - максимальный размер

btn1 = tk.Button(win, text='Hello',
                 command=say_hello)
btn2 = tk.Button(win, text='New label',
                 command=add_label)
btn3 = tk.Button(win, text='New label lambda',
                 command=lambda: tk.Label(win, text='new lambda').pack()
                 )
btn4 = tk.Button(win, text=f'Счетчик: {count}',
                 command=counter,
                 activebackground='blue',
                 bg='yellow',
                 )
btn5 = tk.Button(win, text='Отключает кнопки',
                 command=btn_disable,
                 activebackground='blue',
                 bg='red',
                 )

btn1.pack()
btn2.pack()
btn3.pack()
btn4.pack()
btn5.pack()

win.mainloop()
