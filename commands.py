import os
import shutil


def createDirectory(path):
    drivePath = fetchUser()
    new_path = drivePath + path.replace('/home/machine', '')
    try:
        os.mkdir(new_path)
    except:
        print('Fail to create the directory: ', new_path)
    finally:
        print('Directory created successfully on: ', new_path)


def createFile(path):
    drivePath = fetchUser()
    new_path = str(drivePath) + path.replace('/home/machine', '')
    print('New Path: ', new_path)
    try:
        shutil.copy(src=path, dst=new_path)
    except:
        print('Fail to copy the file ', path, ' to ', new_path)
    finally:
        print('File copied successfully on ', new_path)


def verificationUser():
    ls = os.listdir()
    if 'usermail.txt' not in ls:
        while True:
            try:
                with open('usermail.txt', 'w') as usermail:
                    usermail.write(str(input('Type your gmail username: ')).removesuffix('@gmail.com'))
                    usermail.close()
                    return fetchUser()
            except:
                print('A error on file')
            finally:
                print('File .txt created sussesfully!')
    else:
        fetchUser()


def fetchUser():
    try:
        with open('usermail.txt', 'r') as usermail:
            mail = usermail.read().splitlines()
            for i in mail:
                drivePath = (f'/run/user/1000/gvfs/google-drive:host=gmail.com,user={i}/Meu Drive')
            usermail.close()
            return str(drivePath)
    except:
        print('An error to read the file usermail.txt')
    finally:
        print('File readed sussesfully!')
