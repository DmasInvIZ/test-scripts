import psycopg2
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# настройка параметров подключения к БД, изменить по мере надобности

DATABASE = "postgres"
USER     = "postgres" 
PASSWORD = "interlude"
HOST     = "127.0.0.1" 
PORT     = "5432"

connection = ''

# служебная информация
debug_info = True


def debug(message1: str, message2: str=None, message3: str=None) -> None:
    """Выводит служебное сообщение"""
    if not debug_info:
        return
    print(f'    [DEBUG] {message1}')
    if not message2:
        return
    print(f'    [DEBUG] {message2}')
    if not message3:
        return
    print(f'    [DEBUG] {message3}')



def connect():
    """Подключается к БД"""
    debug('Подключение...')
    #text_field.insert(END, 'Подключение...\n')
 
    global connection
    connection = psycopg2.connect(
      database=DATABASE, 
      user=USER, 
      password=PASSWORD, 
      host=HOST, 
      port=PORT
    )
    debug('Подклшючение успешно')
    #text_field.insert(END, 'Подклшючение успешно\n')
    return connection


def connection_test():
    """Тест подключения к БД
        Пробует подключится и отключается,
        Выводит результат в консоль"""
    debug('Проверяем подключение...')
    #### Проверяем подключение
    try:
        connect()
        connection.close()
        debug('Подключение закрыто.\n')
        #text_field.insert(END, 'Подключение закрыто.\n')

    # ошибка подключения
    except psycopg2.OperationalError:
        print('[ERROR] Подключение не удалоось. Поробуйте изменить настройки подключения.\n')
##        text_field.insert(END, '[ERROR] Подключение не удалоось.\n\
##Поробуйте изменить настройки\n\
##подключения.\n')

    # выводится если не было ошибок
    else:
        print('    [OK] Порядок.\n')
        #text_field.insert(END, '    [OK] Порядок.\n')


def delete_test_data():
    """Удаляет ТОЛЬКО ТЕСТОВЫЕ данные"""
    try:
        connect()
        #### Удаляем тестовые данные из таблиц
        with open('delete_test_data.sql', encoding='utf-8') as del_test_data:
            cur = connection.cursor()
            for sql in del_test_data.readlines():
                debug(f'    Выполняю: {sql.rstrip()}')
                cur.execute(sql)

    # ошибка подключения к БД
    except psycopg2.OperationalError:
        print('    [ERROR] Подключение не удалоось... Поробуйте изменить настройки подключения.\n')

    # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        print('    [ERROR] Ошибка синтаксиса SQL. \n\
    Проверьте правильность синтаксиса SQL запросов в файле "delete_test_data.sql"\n\
    Данные не добавлены.')
        connection.close()
        print('Подключение закрыто.\n')

    # файл не найден
    except FileNotFoundError:
        print('    [ERROR] Файл "delete_test_data.sql" не найден, поврежден или переименован.')
        connection.close()
        debug('Подключение закрыто.\n')
        
    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        print('    [OK] Тестовые данные удалены.\n')
        debug('Изменения сохранены.', 'Подключение закрыто.\n')


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
                debug(f'    Выполняю: {sql.rstrip()}')
                cur.execute(sql)
                
    # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        print('    [ERROR] Ошибка синтаксиса SQL. \n\
    Проверьте правильность синтаксиса SQL запросов в файле "clean_tables.sql"\n\
    Таблицы не очищены.')
        connection.close()
        debug('Подключение закрыто.\n')

    # файл не найден
    except FileNotFoundError:
        print('    [ERROR] Файл "clean_tables.sql" не найден, поврежден или переименован.\n')
        connection.close()
        debug('Подключение закрыто.\n')

    # не удалось подключиться к БД
    except psycopg2.OperationalError:
        print('    [ERROR] Подключение не удалоось... Проверьте настройки подключения.\n')

    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        print('    [OK] Таблицы очищены.\n')
        debug('Изменения сохранены.', 'Подключение закрыто.\n')
        

def add_test_data():
    """Добавялет тестовые данные в бд сайта
    о том как работать с заполнением почитайте в инструкции"""
    try: 
        connect()
    ####Заполняем таблицы данными
        with open('add_test_data.sql', encoding='utf-8') as add_test_data:
            cur = connection.cursor()
            for sql in add_test_data.readlines():
                debug(f'    Выполняю: {sql.rstrip()}')
                cur.execute(sql)      

    # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        print('    [ERROR] Ошибка синтаксиса SQL. \n\
    Проверьте правильность синтаксиса SQL запросов в файле "add_test_data.sql"\n\
    Данные не добавлены.\n')
        connection.close()
        debug('Подключение закрыто.\n')

    # файл не найден
    except FileNotFoundError:
        print('    [ERROR] Файл "add_test_data.sql" не найден, поврежден или переименован.\n')
        connection.close()
        debug('Подключение закрыто.\n')

    # не удалось подключиться к БД
    except psycopg2.OperationalError:
        print('    [ERROR] Подключение не удалоось... Проверьте настройки подключения.\n')

    # значение существует или скрипт выполнялся
    except psycopg2.errors.UniqueViolation as err:
        print(err)
        print('    [ERROR] Возможно скрипт уже выполнялся.\n')
        connection.close()
        debug('Подключение закрыто.\n')
        
    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        print('    [OK] Тестовые данные добавлены.\n')
        debug('Изменения сохранены.', 'Подключение закрыто.\n')



### Интерфейс


def open_settings():
    settings = Tk()
    settings.title('Настройки программы')
    settings.geometry('500x300+150+300')

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



    def checkbutton_changed():
        global debug
        if debug_checkbutton.get() == 1:
            debug = True
        else:
            debug = False

    def save_settings():
        global DATABASE
        DATABASE = entry_database.get()
        global USER
        USER = entry_user.get()
        global PASSWORD
        PASSWORD = entry_password.get()
        global HOST
        HOST = entry_host.get()
        global PORT
        PORT = entry_port.get()
        print('save')

        settings.destroy()

    debug_checkbutton = IntVar()
    enabled_checkbutton = Checkbutton(text="Debug", variable=debug_checkbutton, command=checkbutton_changed)
    enabled_checkbutton.grid(row=5, column=0)

    Button(settings, text='Сохранить', command=save_settings).grid(row=5, column=0)
    Button(settings, text='Отменить', command=settings.destroy).grid(row=5, column=1)
    

def info():
    messagebox.showinfo("Информация", "Dimon Soft.inc\nAll Rights Reserved")

## главное окно программы
root = Tk()
root.title('Add/delete test data in database')
root.geometry('800x600+100+200')


root.option_add("*tearOff", FALSE)
main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="Настройки", command=open_settings)

info_menu = Menu()
info_menu.add_command(label='О программе', command=info)

main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_cascade(label="Информация", menu=info_menu)

root.config(menu=main_menu)

ttk.Button(root, text='Добавлить тестовые данные', command=add_test_data).grid(row=0, column=0)
ttk.Button(root, text='Удалить тестовые данные', command=delete_test_data).grid(row=0, column=1)
ttk.Button(root, text='Удалить все данные', command=delete_data).grid(row=0, column=2)
ttk.Button(root, text='Тест соединения', command=connection_test).grid(row=0, column=3)



text_field = Text(width=50, height=10)# описываем поле ввода
text_field.grid(row=1, column=0, columnspan=4, stick='ew')  # помещаем поле ввода в таблицу


root.mainloop()
