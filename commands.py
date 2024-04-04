import os
import shutil


drivePath = '/run/user/1000/gvfs/google-drive:host=gmail.com,user=lc.juninhonota10000/Meu Drive'

def createDirectory(path):
    new_path = drivePath + path.replace('/home/machine', '')
    try:
        os.mkdir(new_path)
    except:
        print('Fail to create the directory: ', new_path)
    finally:
        print('Directory created successfully on: ', new_path)

def createFile(path):
    new_path = drivePath + path.replace('/home/machine', '')
    try:
        shutil.copy(src=path, dst=new_path)
    except:
        print('Fail to copy the file ', path, ' to ', new_path)
    finally:
        print('File copied successfully on ', new_path)