import flet as ft
import time


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Gdrive Sync'
        self.page.window_width = 500
        self.page.window_height = 500
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.on_resize = self.resizePage
        self.value = ''
        self.data = Data()
        self.paths = [] if self.fetchData() == [] else self.fetchData()
        self.main()


    def main(self):        
        self.field_path = ft.TextField(
            hint_text='Type the path...',
            expand=True,
            on_change=self.fetchText
        )

        # self.buttonConfirm = ft.ElevatedButton(
        #     text='Confirm paths and active Sync',
        #     expand=True,
        #     height=40,
        #     color=ft.colors.WHITE,
        #     icon=ft.icons.CHECK,
        #     bgcolor=ft.colors.BLUE,
        #     disabled=True if len(self.paths) < 0 else False,
        #     on_click=self.createData
        # )
        
        container_field = ft.Row(
            [self.field_path, ft.FloatingActionButton(
                        icon = ft.icons.ADD,
                        bgcolor=ft.colors.BLUE,
                        on_click=self.fetchPath
                    )
            ],
            spacing=15
        )

        # self.container_view = ft.Column(
        #     height=70,
        #     scroll=ft.ScrollMode.AUTO,
        #     visible=False,
        #     width = self.page.window_width
        # )

        # self.container_confirm = ft.Row([self.buttonConfirm], height=70)

        if len(self.value) > 0:
            self.fetchPath()

        self.page.add(container_field, self.createContainerView(), self.createContainerConfirm())


    def resizePage(self, e):
        time.sleep(1)
        print('Page resized')
        self.page.update() # When page resized, the page will update


    def createContainerConfirm(self):
        self.buttonConfirm = ft.ElevatedButton(
            text='Confirm paths and active Sync',
            expand=True,
            height=40,
            color=ft.colors.WHITE,
            icon=ft.icons.CHECK,
            bgcolor=ft.colors.BLUE,
            disabled=True if len(self.paths) < 0 else False,
            on_click=self.createData
        )
        return ft.Row([self.buttonConfirm], height=70)


    def createContainerView(self):
        if len(self.paths) > 0:
            return ft.Column(
                [ft.Text(value=item) for item in self.paths],
                height=70,
                scroll=ft.ScrollMode.AUTO,
                visible=True,
                width = self.page.window_width
            )
        else:
            return ft.Column(
                height=70,
                scroll=ft.ScrollMode.AUTO,
                visible=False,
                width = self.page.window_width
            )


    def fetchText(self, e):
        self.value = e.control.value
        return str(self.value)


    def cleanField(self):
        self.field_path.value = ''
        self.page.update()


    def fetchPath(self, e=''):
        if len(self.value) > 0:
            self.paths.append(self.value)
            self.container_view.visible = True
            self.container_view.controls.append(ft.Text(value=self.value))
            self.buttonConfirm.disabled = False
            self.container_view.width = self.page.window_width
            self.cleanField()
        else:
            print('Type your path first')
    

    def createData(self, e):
        try:
            with open('data.txt', 'w') as data:
                [data.write(item + '\n') for item in self.paths]
        except OSError:
            print('Failed to create the file')
        finally:
            print('data.txt created or modified sussesfully!\n')
    

    def fetchData(self):
        file_data = []
        try:
            with open('data.txt', 'r') as data:
                file_data.append(linha.strip for linha in data)
            print('Data Found: ' ,list(file_data))
        except OSError:
            print('Failed to create the file')
        finally:
            print('data.txt created or modified sussesfully!\n')
        return file_data


class Data:
    def __init__(self):
        self.data = self.fetchData()



    def fetchData(self):
        file_data = []
        try:
            with open('data.txt', 'r') as data:
                file_data.append(linha.strip for linha in data)
            print('Data Found: ' ,list(file_data))
        except OSError:
            print('Failed to create the file')
        finally:
            print('data.txt created or modified sussesfully!\n')
        return file_data


if __name__ == '__main__':
    ft.app(target=App)