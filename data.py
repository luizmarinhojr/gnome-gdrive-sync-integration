class Data:
    def fetchData(self):
        self.file_data = []
        try:
            with open('datapaths.txt', 'r') as data:
                self.file_data = data.read().splitlines()
            print('Data Found: ', self.file_data)
        except OSError:
            print('Failed to create the file')
        finally:
            print('data.txt created or modified sussesfully!\n')
        return self.file_data


    def savePaths(self, e=''):
        try:
            with open('datapaths.txt', 'w') as data:
                [data.write(item + '\n') for item in self.paths]
        except OSError:
            print('Failed to create the file')
        finally:
            print('data.txt created or modified sussesfully!\n')
