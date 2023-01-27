import configparser

config = configparser.ConfigParser()
config.read('set.ini')

hello = config['заголовок']
for i in hello:
    print(i)
print(hello)

c = config['заголовок2']['c']
print(c)
