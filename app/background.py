from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread


class BackgroundIcon:
    def __init__(self, e = ''):
        self.main()
    

    def stopIcon(self):
        print('Stop')
        self.icon.stop()
        
    # Função a ser executada quando o ícone do System Tray for clicado
    def showApp(self, icon, item):
        print(f'Clicked {item}')


    def stopSync(Self, icon, item):
        print(f'Clicked ')


    def main(self):
        print('Starting Icon Background')
        image = Image.open("./assets/icon.png")  # Substitua "icone.png" pelo caminho para o ícone desejado
        self.icon = Icon("GSyncDrive", image)
        self.running = Thread(target=self.icon.run)
        self.running.start()


if __name__ == "__main__":
    exec = BackgroundIcon()
    