import os, main, threading, main, time
from watchdog.observers import Observer


class Data:
    def fetchData(self):
        self.file_data = []
        if os.path.exists('./data/datapaths.txt'):
            try:
                with open('./data/datapaths.txt', 'r') as data:
                    self.file_data = data.read().splitlines()
                print('Data Found: ', self.file_data)
            except OSError:
                print('Failed to create the file')
            finally:
                print('data.txt created or modified sussesfully!\n')
            return self.file_data
        
        return []


    def savePaths(self, e = ''):
        try:
            with open('./data/datapaths.txt', 'w') as data:
                [data.write(item + '\n') for item in self.paths]
            print('data.txt created or modified sussesfully!\n')
            self.createFileExecute()
        except OSError:
            print('Fail to create the file')


    def createFileExecute(self, e = ''):
        current_path = os.getcwd()
        if not os.path.exists(current_path+'main.py'):
            try:
                with open('./shell/gdrivesync.sh', 'w') as gdrive_file:
                    command_sh = f'python {current_path}/main.py'
                    gdrive_file.write(command_sh)
                print('File gdrivesync.sh create succesfully')
            except OSError as error:
                print('A error occurred ', error)


    def executeProgram(self, e = ''):
        # os.popen('sh ./shell/gdrivesync.sh')
        self.event_handler = main.MyHandler()
        self.background_running = threading.Thread(target=self.startProgram, args=())
        self.background_running.start()
        print('Program running succesfully')
        return True
    

    def startProgram(self):
        path = "/home/machine/Documents"  # Diretório a ser monitorado
        observer = Observer()
        print('Chegou aqui starProgram')
        observer.schedule(self.event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
                if not self.event_handler.running:
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            observer.stop()
            print('Sincronização interrompida')
        observer.join()
    

    def killProgram(self, e = ''):
        self.event_handler.running = False
        print('Button pressed')
        return False
    