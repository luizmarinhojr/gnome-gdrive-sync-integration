import os, shutil, time, threading


class Commands:
    def __init__(self):
        self.drivePath = self.verifyUser()
        self.background_thread_busy = False
        self.mountDriver() # Mounting the Google Drive account on program boot


    def mountDriver(self):
        if 'mount-google-drive.sh' in os.listdir(path='./'):
            UID = os.getuid()
            URI = f'/run/user/{UID}/gvfs'
            if not f'google-drive:host=gmail.com,user={self.mail[0]}' in os.listdir(URI):
                try:
                    os.popen('sh ./mount-google-drive.sh')
                except OSError as error:
                    print(error)
                finally:
                    print('Google Drive mounted with sucess in ', self.drivePath)
            else:
                print('The driver already is mounted')
        else:
            self.createMountFile()
    

    def createMountFile(self):
        try:
            with open('mount-google-drive.sh', 'w') as mount_file:
                command_gio = f'gio mount --device="google-drive://{self.mail[0]}@gmail.com/"'
                mount_file.write(command_gio)
        except OSError as error:
            print('A error occurred ', error)
        finally:
            self.mountDriver()


    def changeDirectory(self):
        time.sleep(1)
        root = self.drivePath.removesuffix('/Meu Drive')
        try:
            os.chdir(root)
            print('Success: connection established')
        except OSError as error:
            print("Fail: it didn't connect: ", error)


    def createDirectory(self, path):
        new_path = self.drivePath + path.removeprefix('/home/machine')
        self.changeDirectory()
        try:
            os.mkdir(new_path)
            print('Success: directory created on: ', new_path)
        except:
            print('Fail to create the directory: ', new_path)


    def createFile(self, path):
        new_path = self.drivePath + path.removeprefix('/home/machine')
        background_thread = threading.Thread(target=self.backgroundCopying, args=(path, new_path))
        background_thread.start()


    def backgroundCopying(self, path, new_path):
        self.background_thread_busy = True
        self.changeDirectory()
        try:
            shutil.copyfile(src=path, dst=new_path)
            print('Success: file copied to ', new_path)
            self.background_thread_busy = False
        except:
            print('Error: The file was not copied')

    
    def modifiedFile(self, path):
        new_path = self.drivePath + path.removeprefix('/home/machine')
        file_exist = os.path.exists(new_path)
        LOCAL_TIME = time.time()
        if file_exist:
            time_modified_file = os.path.getmtime(new_path)
            difference_time = LOCAL_TIME - time_modified_file # Calculates file modification time
            if difference_time > 5:
                background_thread = threading.Thread(target=self.backgroundCopying, args=(path, new_path))
                background_thread.start()
            else:
                print('The file already was modified a less 5 seconds')


    def verifyUser(self):
        ls = os.listdir()
        if 'usermail.txt' not in ls:
            while True:
                try:
                    with open('usermail.txt', 'w') as usermail:
                        mail = str(input('Type your gmail username: ')).removesuffix('@gmail.com')
                        usermail.write(mail)
                except:
                    print('Error: File usermail.txt was not created')
                finally:
                    print('Success: usermail.txt was created!')
                    return self.fetchUser()
        else:
            return self.fetchUser()


    def fetchUser(self):
        try:
            with open('usermail.txt', 'r') as usermail:
                self.mail = usermail.read().splitlines()
                drivePath = f'/run/user/1000/gvfs/google-drive:host=gmail.com,user={self.mail[0]}/Meu Drive'
        except:
            print('Error: file usermail.txt was not available to read')
        finally:
            print('Success: usermail.txt read!')
            return drivePath
