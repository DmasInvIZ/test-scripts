import psycopg2, configparser


# импортируем настройки из .ini файла
ini_parse = configparser.ConfigParser()  # объект парсера
#ini_parse.read('config.ini')  # читаем файл
if not ini_parse.read('config.ini'):
    with open('config.ini', "w") as configfile:
        configfile.write('\
# Файл отсутствовал и был создан заново.\n\
[CONNECTION]\n\
DATABASE = \n\
USER     = \n\
PASSWORD = \n\
HOST     = \n\
PORT     = \n\
\n\
[DEV]\n\
debug_information = False\
                         ')
        
ini_parse.read('config.ini')  # читаем файл
main = ini_parse['CONNECTION']  # первый раздел настроек
dev = ini_parse['DEV']  # второй раздел

# записываем настройки из файла
DATABASE = main['DATABASE']
USER     = main['USER']
PASSWORD = main['PASSWORD']
HOST     = main['HOST']
PORT     = main['PORT']

debug_info = dev['debug_information']


def curr_settings():
    print('Текущая конфигурация настроек:')
    print(f"\
|  DATABASE = {DATABASE}\n\
|  USER     = {USER}\n\
|  PASSWORD = {PASSWORD}\n\
|  HOST     = {HOST}\n\
|  PORT     = {PORT}\n\
|\n\
|  debug    = {debug_info}\n\
          ")


def config_save():
    pass


def debug(message1: str, message2: str=None, message3: str=None) -> None:
    """Выводит служебное сообщение"""
    if debug_info != 'True':
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
    global connection
    connection = psycopg2.connect(
      database=DATABASE, 
      user=USER, 
      password=PASSWORD, 
      host=HOST, 
      port=PORT
    )
    debug('Подклшючение успешно.')


def greeting():
    """Экран приветствия"""
    print(f'\n\
 ####  ### #   #  ###  #   #    ####  ###   ##### #####\n\
 #   #  #  ## ## #   # ##  #   #     #   #  #       #\n\
 #   #  #  # # # #   # # # #    ###  #   #  ###     #\n\
 #   #  #  #   # #   # #  ##       # #   #  #       #\n\
 ####  ### #   #  ###  #   #   ####   ###   #       #\n\
\n\
Этот скрипт выполняет некоторые манипуляции с базой данных v2.3\n')

    curr_settings()


def reconf():
    """При вызове изменяет настройки подключения к БД"""
    
    global DATABASE
    DATABASE = input(f'Введите имя БД. Сейчас введено "{DATABASE}": ')
    global USER
    USER     = input(f'Введите имя пользователя. Сейчас введено "{USER}": ')
    global PASSWORD
    PASSWORD = input(f'Введите пароль. Сейчас введено "{PASSWORD}": ')
    global HOST
    HOST     = input(f'Введите адрес сервера (хост). Сейчас введено "{HOST}": ')
    global PORT
    PORT     = input(f'Введите порт от БД. Сейчас введено "{PORT}": ')
    print('    [OK] Конфигурация сохранена\n')

    config_save()
    make_choice()


def run_txt_file():
    """Выполняет список SQL команд из файла"""
    try: 
        connect()
    ####Заполняем таблицы данными
        with open('SQLs.txt', encoding='utf-8') as run_file:
            cur = connection.cursor()
            for sql in run_file.readlines():
                print(f'    Выполняю: {sql.rstrip()}')
                cur.execute(sql)      

    # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        print('    [ERROR] Ошибка синтаксиса SQL. \n\
    Проверьте правильность синтаксиса SQL запросов в файле "add_test_data.sql"\n\
    Данные не добавлены.\n')

    # файл не найден
    except FileNotFoundError:
        print('    [ERROR] Файл "SQLs.txt" не найден, поврежден или переименован.\n')
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

    except psycopg2.errors.UndefinedTable as err:
        print('    [ERROR]', err)
        connection.close()
        debug('Подключение закрыто.\n')
        
    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        print('    [OK] Команды из файла выполнены.\n')
        debug('Изменения сохранены.', 'Подключение закрыто.\n')

    make_choice()


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
            

    # ошибка подключения
    except psycopg2.OperationalError:
        print('    [ERROR] Подключение не удалоось... Поробуйте изменить настройки.\n')

    # выводится если не было ошибок
    else:
        print('    [OK] Порядок.\n')
    make_choice()


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
        debug('Подключение закрыто.\n')

    # файл не найден
    except FileNotFoundError:
        print('    [ERROR] Файл "delete_test_data.sql" не найден, поврежден или переименован.\n')
        connection.close()
        debug('Подключение закрыто.\n')
        
    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        print('    [OK] Тестовые данные удалены.\n')
        debug('Подключение закрыто.\n')

    make_choice()


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

    # файл не найден
    except FileNotFoundError:
        print('    [ERROR] Файл "add_test_data.sql" не найден, поврежден или переименован.\n')

    # не удалось подключиться к БД
    except psycopg2.OperationalError:
        print('    [ERROR] Подключение не удалоось... Проверьте настройки подключения.\n')

    # значение существует или скрипт выполнялся
    except psycopg2.errors.UniqueViolation as err:
        print(err)
        print('    [ERROR] Возможно скрипт уже выполнялся.\n')
        
    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.commit()
        connection.close()
        print('    [OK] Тестовые данные добавлены.\n')
        debug('Изменения сохранены.', 'Подключение закрыто.\n')

    make_choice()
        

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
        
    make_choice()


def reconf():
    """При вызове изменяет настройки подключения к БД"""
    
    global DATABASE
    DATABASE = input(f'Введите имя БД. Сейчас введено "{DATABASE}": ')
    global USER
    USER     = input(f'Введите имя пользователя. Сейчас введено "{USER}": ')
    global PASSWORD
    PASSWORD = input(f'Введите пароль. Сейчас введено "{PASSWORD}": ')
    global HOST
    HOST     = input(f'Введите адрес сервера (хост). Сейчас введено "{HOST}": ')
    global PORT
    PORT     = input(f'Введите порт от БД. Сейчас введено "{PORT}": ')
    print('    [OK] Конфигурация сохранена\n')
    
    make_choice()


def make_sql():
    """Отпарвляет SQL запрос в БД"""
    try: 
        connect()
        #### делаем запрос
        cur = connection.cursor()
        sql = ''
        while sql != 'exit':
            if sql == 'commit':
                print('[OK] Изменения сохранены')
                connection.commit()
            try:
                sql = input('Введите SQL запрос. Чтобы сохранить "commit", для выхода "exit": ')
                cur.execute(sql)
                result = cur.fetchall()
                print(result)
            except psycopg2.ProgrammingError as err:
                print(err)
        

        # ошибка синтаксиса SQL в файле
    except psycopg2.errors.SyntaxError:
        print('    [ERROR] Ошибка синтаксиса SQL. \n\
    Проверьте правильность синтаксиса SQL запросов в файле "clean_tables.sql"\n\
    Таблицы не очищены.\n')
        connection.close()
        debug('Подключение закрыто.\n')

    # не удалось подключиться к БД
    except psycopg2.OperationalError:
        print('    [ERROR] Подключение не удалоось... Проверьте настройки подключения.\n')

    #### сохраняем и закрываем подключение (сработает если исключения не было)
    else:
        connection.close()
        print('[OK] Подключение закрыто, выходим...\n')

    make_choice()


#### информация о действиях
info1 = 'Этот скрипт добавляет тестовые данные: \n\
\n\
До этого должно быть сделано:\n\
    сделаны миграции, то есть созданы таблицы \n\
    лучше если таблицы будут пустыми\n\
    создан админ (первым) и тестовый юзер (его id должен быть 2, id админа будет 1 смотреть в таблице auth_user)\n\
\n\
Что создается в бд: \n\
    2 новости для главной страницы \n\
    2 области - Минская и Витебская \n\
    3 города в Витебской области \n\
    2 города в Минской области \n\
    публикации пользователей для трех городов, сразу опубликованные \n\
    2 поста в раздел "о проекте" \n\
    2 поста в раздел "отзывы о путешествиях" от админа и тестового юзера (id 1, 2) \n'

info2 = 'Этот скрипт удаляет ТОЛЬКО ТЕСТОВЫЕ данные, \n\
то есть данные которые были занесены в БД первым скриптом,\n\
остальные данные не трогает.\n'

info3 = 'Этот скрипт удаляет ВСЕ данные из используемых таблиц.\n\
На всякий случай напомню:\n\
    blog_post\n\
    guide_news\n\
    guide_about\n\
    guide_usertowns\n\
    guide_towns\n\
    guide_districts\n'

info4 = 'Здесь можно изменить настройки подключения к БД\n\
если лень лезть в файл и менять там, но лучше так и сделать,\n\
настройки не сохраняются при перезапуске скрипта.\n'

info5 = 'Этот скрипт тестирует подключение к БД.\n\
Пробует подключится используя записанные настройки и отключается.\n\
Результат проверки будет здесь.\n'

info6 = 'Здесь можно сделать SQL запрос вручную.\n\
Помните про синтаксис.\n'

info8 = 'Этот скрипт выполняет SQL запросы из файла "SQLs.txt".\n\
Убедитесь что синтаксис языка SQL соблюден.'

####

greeting()  # Выводим экран приветствия и текущие настройки подключения

def make_choice():
    """Основнова функция, определяем выбор пользователя"""
    
    print('Выберите одно из следующий действий:\n\
1 - Запись тестовых данных\n\
2 - Удаление тестовых данных\n\
3 - Удаление всех данных из таблиц изменяемых пользователем\n\
4 - Изменить настройки подключения к БД\n\
5 - Тест подключения к БД\n\
6 - [TEST] Сделать SQL-запрос в БД (Работает кривовато, есть ошибка транзакций)\n\
8 - [TEST] Выполнить SQL-команды из файла SQLs.txt\n\
9 - Показать настройки подключения к БД\n\
0 - Выход из программы')
    
    choice = input('Введите число: ')
    print(f'Вы ввели {choice}\n')
    
    if choice == '1':
        print(info1)  # печатаем информацию о действии
        if input('Продолжаем? "Enter" - Да, любой другой символ - нет: ') == '':
            add_test_data()  # Добавление тестовых данных
        else:
            print('Отменено\n')
            make_choice()
        
    elif choice == '2':
        print(info2)  # печатаем информацию о действии
        if input('Продолжаем? "Enter" - Да, любой другой символ - нет: ') == '':
            delete_test_data()  # Удаление тестовых данных
        else:
            print('Отменено\n')
            make_choice()
        
    elif choice == '3':
        print(info3)  # печатаем информацию о действии
        if input('Продолжаем? "Enter" - Да, любой другой символ - нет: ') == '':
            delete_data()  # Очистка таблиц
        else:
            print('Отменено\n')
            make_choice()
        
    elif choice == '4':
        print(info4)  # печатаем информацию о действии
        if input('Продолжаем? "Enter" - Да, любой другой символ - нет: ') == '':
            reconf()  # Изменение настроек подключения к БД
        else:
            print('Отменено\n')
            make_choice()
        
    elif choice == '5':
        print(info5)  # печатаем информацию о действии
        if input('Продолжаем? "Enter" - Да, любой другой символ - нет: ') == '':
            connection_test()  # Проверка подключения к БД
        else:
            print('Отменено\n')
            make_choice()

    elif choice == '6':
        print(info6)
        if input('Продолжаем? "Enter" - Да, любой другой символ - нет: ') == '':
            make_sql()

    elif choice == '8':
        print(info8)
        if input('Продолжаем? "Enter" - Да, любой другой символ - нет: ') == '':
            run_txt_file()#  Выполняем команды из файла SQLs.txt
        
    elif choice == '9':
        curr_settings()  # Выводим текущие настройки подключения
        make_choice()
        
    elif choice == '0':
        if input('Выйти из программы? "Enter" - Да, любой другой символ - нет: ') == '':
            print('Выходим...')
            exit()  # Выход из программы
        else: make_choice()
        
    elif choice in '0123456789' and len(choice) > 1:
        print('Таких вариантов не предусмотрено...\n')
        make_choice()
        
    else:
        print('Какое из слов "Введите число" вам не понятно? Давайте еще раз.\n')
        make_choice()
        

if __name__ == '__main__':
    make_choice()
