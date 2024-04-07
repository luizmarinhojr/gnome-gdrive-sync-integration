import os, shutil, time, threading


class Commands:
    def __init__(self):
        self.drivePath = self.verifyUser()
        self.background_thread_busy = False


    def changeDirectory(self):
        time.sleep(1)
        root = self.drivePath.removesuffix('/Meu Drive')
        try:
            os.chdir(root)
        except:
            print("Fail: it didn't connect")
        finally:
            print('Success: connection established')


    def createDirectory(self, path):
        new_path = self.drivePath + path.removeprefix('/home/machine')
        try:
            self.changeDirectory()
            os.mkdir(new_path)
        except:
            print('Fail to create the directory: ', new_path)
        finally:
            print('Success: directory created on: ', new_path)


    def createFile(self, path):
        new_path = self.drivePath + path.removeprefix('/home/machine')
        try:
            self.changeDirectory()
            shutil.copyfile(src=path, dst=new_path)
        except:
            print('Fail to copy the file ', path, ' to ', new_path)
        finally:
            print('Success: file copied to ', new_path)
            time.sleep(4)


    def backgroundOperations(self, path, new_path):
        self.background_thread_busy = True
        try:
            self.changeDirectory()
            shutil.copyfile(src=path, dst=new_path)
        except OSError as error:
            print(error)
        finally:
            print('Success: file copied to ', new_path)
            time.sleep(2)
            self.background_thread_busy = False

    
    def modifiedFile(self, path):
        new_path = self.drivePath + path.removeprefix('/home/machine')
        time_modified_file = os.path.getmtime(path)
        LOCAL_TIME = time.time()
        difference_time = LOCAL_TIME - time_modified_file
        if difference_time <= 2:
            if not self.background_thread_busy:
                background_thread = threading.Thread(target=self.backgroundOperations, args=(path, new_path))
                background_thread.start()
            else:
                print('A thread already busy. Please wait for it to finish.')
        

    def verifyUser(self):
        ls = os.listdir()
        if 'usermail.txt' not in ls:
            while True:
                try:
                    with open('usermail.txt', 'w') as usermail:
                        usermail.write(str(input('Type your gmail username: ')).removesuffix('@gmail.com'))
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
                mail = usermail.read().splitlines()
                for line in mail:
                    drivePath = f'/run/user/1000/gvfs/google-drive:host=gmail.com,user={line}/Meu Drive'
        except:
            print('Error: file usermail.txt was not available to read')
        finally:
            print('Success: usermail.txt read!')
            return drivePath
