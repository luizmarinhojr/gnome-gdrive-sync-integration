from pystray import Icon
from PIL import Image
from threading import Thread


class BackgroundIcon:
    def __init__(self, e = ''):
        self.main()
    

    def stopIcon(self):
        print('Stop Icon')
        self.icon.stop()


    def main(self):
        print('Starting Icon Background')
        image = Image.open("./assets/icon.png")  # Substitua "icone.png" pelo caminho para o ícone desejado
        self.icon = Icon("GSyncDrive", image)
        self.running = Thread(target=self.icon.run)
        self.running.start()


if __name__ == "__main__":
    exec = BackgroundIcon()
    