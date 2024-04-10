import os, threading, main
from watchdog.observers import Observer


class Data:
    def __init__(self):
        self.dicionario = {'path': '', 'usermail': '', 'folder': ''}
    

    @staticmethod
    def fetchData():
        data = {'path': '', 'usermail': '', 'folder': ''}
        if os.path.exists('./data/config.txt'):
            try:
                with open('./data/config.txt', 'r') as file:
                    for item in data:
                        data[item] = file.readline().strip()
            except:
                print('error')
        
        return data


    def saveAll(self, data, e=''):
        try:
            with open('./data/config.txt', 'w') as file:
                [file.write(data[item]+'\n') for item in data]
            self.createFileExecute()
        except:
            print('Error')


    def createFileExecute(self, e = ''):
        self.current_path = os.getcwd()
        if not os.path.exists(self.current_path+'/shell/gdrivesync.sh'):
            try:
                with open('./shell/gdrivesync.sh', 'w') as gdrive_file:
                    command_sh = f'python {self.current_path}/app.py'
                    gdrive_file.write(command_sh)
                print('File gdrivesync.sh create succesfully')
                self.createFileDesktop()
            except OSError as error:
                print('A error occurred ', error)

    
    def createFileDesktop(self):
        icon = self.current_path+'/content/google-drive-logo.png'
        exec = 'sh '+self.current_path+'/shell/gdrivesync.sh'
        user = os.getlogin()
        path = f'/home/{user}/.local/share/applications/gdrive-sync.desktop'
        if not os.path.exists(path):
            with open(path, 'w') as gdrive:
                gdrive.write(f'''[Desktop Entry]
Version=1.0
Name=gDrive Sync
Comment=Command Shell to execute automatic sync on Gnome
Type=Application
Icon={icon}
Exec={exec}
Terminal=false
Categories=Utility;''')


    def executeProgram(self, e = ''):
        # os.popen('sh ./shell/gdrivesync.sh')
        self.event_handler = main.MyHandler()
        self.background_running = threading.Thread(target = self.event_handler.startProgram, args = ())
        self.background_running.start()
        print('Program running succesfully')
        return True
    

    def killProgram(self, e = ''):
        self.event_handler.running = False
        print('Button pressed')
        return False
