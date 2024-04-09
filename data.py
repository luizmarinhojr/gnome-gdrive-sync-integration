import os, threading, main
from watchdog.observers import Observer


class Data:
    def __init__(self):
        self.dicionario = {'path': '', 'usermail': '', 'folder': ''}
    
    
    @staticmethod
    def fetchData():
        file_data = []
        if os.path.exists('./data/datapaths.txt'):
            try:
                with open('./data/datapaths.txt', 'r') as data:
                    file_data = data.read().splitlines()
                print('Data Found: ', file_data[0])
                return file_data
            except OSError:
                print('Failed to create the file')
        
        return []

    @staticmethod
    def fetchUser():
        try:
            with open('./data/usermail.txt', 'r') as usermail:
                mail = usermail.read().splitlines()
            print('Success: usermail.txt read!')
            return mail
        except OSError as error:
            print('Error: file usermail.txt was not available to read - ', error)


    def savePaths(self, e = '', mail = ''):
        try:
            with open('./data/datapaths.txt', 'w') as data:
                [data.write(item + '\n') for item in self.paths]
            print('data.txt created or modified sussesfully!\n')
            self.createUser(mail)
        except OSError:
            print('Fail to create the file')


    def createUser(self, mail):
        try:
            with open('./data/usermail.txt', 'w') as usermail:
                usermail.write(mail)
            print('Success: usermail.txt was created!')
            self.createFileExecute()
        except OSError as error:
            print('Error: File usermail.txt was not created - ', error)
    

    def createFirstDirectory(self):
        try:
            with open('./data/usermail.txt', 'w') as usermail:
                usermail.write(mail)
            print('Success: usermail.txt was created!')
            self.createFileExecute()
        except OSError as error:
            print('Error: File usermail.txt was not created - ', error)


    def createFileExecute(self, e = ''):
        self.current_path = os.getcwd()
        if not os.path.exists(self.current_path+'main.py'):
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
        exec = self.current_path+'/shell/gdrivesync.sh'
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
