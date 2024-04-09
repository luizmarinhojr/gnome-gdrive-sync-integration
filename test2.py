dicionario = {
        'path': '',
        'usermail': '',
        'folder': ''
    }

try:
    with open('./data/configs.txt', 'r') as file:
        for item in dicionario.keys():
            dicionario[item] = file.readline().strip()
    print(dicionario)
except:
    print('error')


