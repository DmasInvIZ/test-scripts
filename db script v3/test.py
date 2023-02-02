import psycopg2
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import configparser


# импортируем настройки из .ini файла
ini_parse = configparser.ConfigParser()                         # создаем объект парсера
if not ini_parse.read('config.ini'):                            # если файл не найден, записываем пустые настройки
    with open('config.ini', "w") as configfile:
        configfile.write('\
[CONNECTION]\n\
DATABASE = \n\
USER     = \n\
PASSWORD = \n\
HOST     = \n\
PORT     = \n\
                         ')
        
ini_parse.read('config.ini')                                    # читаем файл
main = ini_parse['CONNECTION']                                  # первый раздел настроек

# записываем настройки из файла
global DATABASE
DATABASE = main['DATABASE']
global USER
USER     = main['USER']
global PASSWORD
PASSWORD = main['PASSWORD']
global HOST
HOST     = main['HOST']
global PORT
PORT     = main['PORT']


def connect():
    """Подключается к БД"""
    
    global connection
    connection = psycopg2.connect(
      database=DATABASE, 
      user=USER, 
      password=PASSWORD, 
      host=HOST, 
      port=PORT
    )


def connection_test():
    """Тест подключения к БД
    Пробует подключится и отключается"""
    
    try:
        connect()
        connection.close()

    # ошибка подключения
    except psycopg2.OperationalError:
        messagebox.showerror('ERROR', 'Подключение не удалоось. Поробуйте изменить настройки подключения.')

    # выводится если не было ошибок
    else:
        messagebox.showinfo('OK', 'Порядок.')


def delete_test_data():
    """Удаляет ТОЛЬКО ТЕСТОВЫЕ данные"""
    
    try:
        connect()
        #### Удаляем тестовые данные из таблиц
        with open('delete_test_data.sql', encoding='utf-8') as del_test_data:
            cur = connection.cursor()
            for sql in del_test_data.readlines():
                cur.execute(sql)

    # ошибка подключения к БД
    except psycopg2.OperationalError:
        messagebox.showerror('ERROR', 'Подключение не удалоось... Поробуйте изменить настройки подключения.')

    # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        connection.close()
        messagebox.showerror('ERROR','Ошибка синтаксиса SQL.\n\
Проверьте правильность синтаксиса SQL запросов в файле "delete_test_data.sql"\n\
    Данные не добавлены.')
        

    # файл не найден
    except FileNotFoundError:
        connection.close()
        messagebox.showerror('ERROR', 'Файл "delete_test_data.sql" не найден, поврежден или переименован.')
        
    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        messagebox.showinfo('OK', 'Тестовые данные удалены.')


def delete_data():
    """Удаляет все данные из таблиц
    которые были созданы в моделях.
    Не трогает пользователей.
    Отредактировать скрипт при изменении количества таблиц"""
    
    try: 
        connect()
    #### очищаем таблицы
        with open('clean_tables.sql') as clear:
            cur = connection.cursor()
            for sql in clear.readlines():
                cur.execute(sql)
                
    # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        connection.close()
        messagebox.showerror('ERROR', 'Ошибка синтаксиса SQL. \n\
Проверьте правильность синтаксиса SQL запросов в файле "clean_tables.sql"\n\
    Таблицы не очищены.')

    # файл не найден
    except FileNotFoundError:
        connection.close()
        messagebox.showerror('ERROR', 'Файл "clean_tables.sql" не найден, поврежден или переименован.')

    # не удалось подключиться к БД
    except psycopg2.OperationalError:
        messagebox.showerror('ERROR', 'Подключение не удалоось... Проверьте настройки подключения.')

    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        messagebox.showinfo('OK', 'Таблицы очищены.')
        

def add_test_data():
    """Добавялет тестовые данные в бд сайта
    о том как работать с заполнением почитайте в инструкции"""

    try: 
        connect()
    ####Заполняем таблицы данными
        with open('add_test_data.sql', encoding='utf-8') as add_test_data:
            cur = connection.cursor()
            for sql in add_test_data.readlines():
                cur.execute(sql)      

    # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        connection.close()
        messagebox.showerror('ERROR', 'Ошибка синтаксиса SQL. \n\
Проверьте правильность синтаксиса SQL запросов в файле "add_test_data.sql"\n\
    Данные не добавлены.')

    # файл не найден
    except FileNotFoundError:
        connection.close()
        messagebox.showerror('ERROR', 'Файл "add_test_data.sql" не найден, поврежден или переименован.')

    # не удалось подключиться к БД
    except psycopg2.OperationalError:
        messagebox.showerror('ERROR', 'Подключение не удалоось... Проверьте настройки подключения.')

    # значение существует или скрипт выполнялся
    except psycopg2.errors.UniqueViolation as err:
        connection.close()
        messagebox.showwarning('Warning', f'{err}\nВозможно скрипт уже выполнялся.')
        
    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        messagebox.showinfo('OK', 'Тестовые данные добавлены.')


### Интерфейс

## окно настроек
def open_settings():
    settings = Tk()
    settings.title('Настройки программы')
    settings.geometry('300x130+250+250')
    settings.resizable(False, False)

    label_database = ttk.Label(settings, text='Название БД')
    entry_database = Entry(settings)

    label_user = Label(settings, text='Имя пользователя')
    entry_user = Entry(settings)

    label_password = Label(settings, text='Пароль')
    entry_password = Entry(settings)

    label_host = Label(settings, text='Хост')
    entry_host = Entry(settings)

    label_port = Label(settings, text='Порт')
    entry_port = Entry(settings)

    label_database.grid(row=0, column=0)
    entry_database.grid(row=0, column=1)
    label_user.grid(row=1, column=0)
    entry_user.grid(row=1, column=1)
    label_password.grid(row=2, column=0)
    entry_password.grid(row=2, column=1)
    label_host.grid(row=3, column=0)
    entry_host.grid(row=3, column=1)
    label_port.grid(row=4, column=0)
    entry_port.grid(row=4, column=1)

    entry_database.insert(0, DATABASE)
    entry_user.insert(0, USER)
    entry_password.insert(0, PASSWORD)
    entry_host.insert(0, HOST)
    entry_port.insert(0, PORT)


    def save_settings():  
        global DATABASE
        DATABASE = entry_database.get()
        main['DATABASE'] = DATABASE
        
        global USER
        USER = entry_user.get()
        main['USER'] = USER
        
        global PASSWORD
        PASSWORD = entry_password.get()
        main['PASSWORD'] = PASSWORD
        
        global HOST
        HOST = entry_host.get()
        main['HOST'] = HOST
        
        global PORT
        PORT = entry_port.get()
        main['PORT'] = PORT

        with open('config.ini', 'w') as configfile:
            ini_parse.write(configfile)

        settings.destroy()

    Button(settings, text='Сохранить', command=save_settings).grid(row=5, column=0)
    Button(settings, text='Отменить', command=settings.destroy).grid(row=5, column=1)
    

def info():
    messagebox.showinfo("Информация", "Dimon Soft inc\nAll Rights Reserved")

## главное окно программы
root = Tk()
root.title('DB operator')
root.geometry('300x100+200+200')
root.resizable(False, False)

root.option_add("*tearOff", FALSE)                                      # убираем разделитель в выпадающем меню
main_menu = Menu()

file_menu = Menu()                                                      # подменю "Файл"
file_menu.add_command(label="Настройки", command=open_settings)

info_menu = Menu()                                                      # подменю "Инфо"
info_menu.add_command(label='О программе', command=info)

main_menu.add_cascade(label="Файл", menu=file_menu)                     # меню "Файл"
main_menu.add_cascade(label="Информация", menu=info_menu)               # меню "Информация"

root.config(menu=main_menu)

ttk.Button(root, text='Добавлить тестовые данные', command=add_test_data).grid(row=0, column=0, stick='ew')
ttk.Button(root, text='Удалить тестовые данные', command=delete_test_data).grid(row=1, column=0, stick='ew')
ttk.Button(root, text='Удалить все данные', command=delete_data).grid(row=2, column=0, stick='ew')
ttk.Button(root, text='Тест соединения', command=connection_test).grid(row=3, column=0, stick='ew')

root.mainloop()
