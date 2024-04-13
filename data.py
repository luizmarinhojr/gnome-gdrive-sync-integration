import os, threading, events


class Data:
    def __init__(self):
        self.default_path_home = os.path.join(os.path.expanduser('~'), '.local', 'share', 'GDriveSync')


    def fetchData(self):
        self.data = {'path': '', 'usermail': '', 'folder': ''}
        if os.path.exists(os.path.join(self.default_path_home, 'data', 'config.txt')):
            try:
                with open(os.path.join(self.default_path_home, 'data', 'config.txt'), 'r') as file:
                    for item in self.data:
                        self.data[item] = file.readline().strip()
            except:
                print('Error to read the data')
        
        return self.data


    def saveAll(self, data, e=''):
        self.createDirectory()
        os.system(f'chmod +w {os.path.join(self.default_path_home, "data")}')
        try:
            with open(os.path.join(self.default_path_home, 'data', 'config.txt'), 'w') as file:
                [file.write(data[item]+'\n') for item in data]
        except OSError as error:
            print('Error', error)
    

    def createDirectory(self):
        try:
            if not os.path.exists(self.default_path_home):
                os.mkdir(self.default_path_home)
            if not os.path.exists(os.path.join(self.default_path_home, 'data')):
                os.mkdir(os.path.join(self.default_path_home, 'data'))
        except OSError as error:
            print('A error to create directory: ', error)


    def executeProgram(self, e = ''):
        self.event_handler = events.MyHandler()
        self.background_running = threading.Thread(target = self.event_handler.startProgram, args = ())
        self.background_running.start()
        print('Program running succesfully')
        return True
    

    def killProgram(self, e = ''):
        self.event_handler.running = False
        print('Button pressed')
        return False