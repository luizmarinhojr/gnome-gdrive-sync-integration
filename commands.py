import os, shutil, time, threading
from random import uniform


class Commands:
    def __init__(self):
        self.drivePath = self.fetchUser()
        self.background_thread_busy = False
        self.TIME_EVENT = time.time()
        self.default_path = self.formattingDefaultPath()
        self.mountDriver() # Mounting the Google Drive account on program boot


    def mountDriver(self):
        if os.path.exists('./shell/mount-google-drive.sh'):
            UID = os.getuid()
            URI = f'/run/user/{UID}/gvfs/google-drive:host=gmail.com,user={self.mail[0]}'
            if not os.path.exists(URI):
                try:
                    os.popen('sh ./shell/mount-google-drive.sh')
                    print('Google Drive mounted with sucess in ', self.drivePath)
                    self.TIME_EVENT = time.time()
                except OSError as error:
                    print(error)
            else:
                print('The driver is ready')
        else:
            self.createMountFile()
    

    def createMountFile(self):
        try:
            with open('./shell/mount-google-drive.sh', 'w') as mount_file:
                command_gio = f'gio mount --device="google-drive://{self.mail[0]}@gmail.com/"'
                mount_file.write(command_gio)
            self.mountDriver()
        except OSError as error:
            print('A error occurred ', error)
    

    def verifyMount(self):
        TIME_NOW = time.time()
        if not (TIME_NOW - self.TIME_EVENT) < 60:
            self.mountDriver()


    def formattingDefaultPath(self):
        bring_path = Commands.fetchPath().split('/')
        default_path = '/'.join(bring_path[0:-1])
        return default_path


    def createDirectory(self, path):
        print(self.default_path)
        new_path = self.drivePath + path.removeprefix(self.default_path)
        self.verifyMount()
        try:
            os.mkdir(new_path)
            self.TIME_EVENT = time.time()
            print('Success: directory created on: ', new_path)
        except:
            print('Fail to create the directory: ', new_path)


    def createFile(self, path):
        time.sleep(uniform(0, 2))
        new_path = self.drivePath + path.removeprefix(self.default_path)
        background_thread = threading.Thread(target=self.backgroundCopying, args=(path, new_path))
        background_thread.start()


    def backgroundCopying(self, path, new_path):
        self.background_thread_busy = True
        self.verifyMount()
        try:
            shutil.copyfile(src=path, dst=new_path)
            print('Success: file copied to ', new_path)
            self.TIME_EVENT = time.time()
            self.background_thread_busy = False
        except:
            print('Error: The file was not copied')

    
    def modifiedFile(self, path):
        time.sleep(uniform(0, 2))
        new_path = self.drivePath + path.removeprefix(self.default_path)
        file_exist = os.path.exists(new_path)
        TIME_NOW = time.time()
        if file_exist:
            time_modified_file = os.path.getmtime(new_path)
            difference_time = TIME_NOW - time_modified_file # Calculates file modification time
            if difference_time > 5:
                if not self.background_thread_busy:
                    background_thread = threading.Thread(target=self.backgroundCopying, args=(path, new_path))
                    background_thread.start()
            else:
                print('The file already was modified a less 5 seconds')


    def fetchUser(self):
        try:
            with open('./data/usermail.txt', 'r') as usermail:
                self.mail = usermail.read().splitlines()
                drivePath = f'/run/user/1000/gvfs/google-drive:host=gmail.com,user={self.mail[0]}/Meu Drive'
            print('Success: usermail.txt read!')
            return drivePath
        except OSError as error:
            print('Error: file usermail.txt was not available to read - ', error)


    @staticmethod
    def fetchPath():
        if os.path.exists('./data/datapaths.txt'):
            try:
                with open('./data/datapaths.txt', 'r') as data:
                    file_data = data.read().splitlines()
                print('Data Found: ', file_data)
                return file_data[0]
            except OSError:
                print('Failed to create the file')