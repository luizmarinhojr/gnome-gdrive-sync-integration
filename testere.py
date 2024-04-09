import os


class Animal:
    def __init__(self):
        print('Acionou no init')
    
    @staticmethod
    def imprimir():
        return '/home/machine/Documents/python-projects/gnome'
    
    
    def testScript():
        print('Qualquer coisa')
        exemplo = Animal.imprimir().split('/')
        test = '/'.join(exemplo[0: -1])
        print(test)


exem = Animal
exem.testScript()
# user = os.getlogin()

# icon = '/home/machine/Documents'
# exec = '/home/machine/Documents/python-projects/gnome-fedora'.split('/')

# print(user)
# print(exec[1:3])