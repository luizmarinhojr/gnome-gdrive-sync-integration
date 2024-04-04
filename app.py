import flet as ft
import time
from data import Data


class App(Data):
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Gdrive Sync'
        self.page.window_width = 500
        self.page.window_height = 500
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.on_resize = self.resizePage
        self.value = ''
        self.paths = [] if len(super().fetchData()) < 0 else super().fetchData()
        self.main()


    def main(self):        
        self.field_path = ft.TextField(
            hint_text='Type the path...',
            expand=True,
            on_change=self.fetchText
        )

        container_field = ft.Row(
            [self.field_path, ft.FloatingActionButton(
                        icon = ft.icons.ADD,
                        bgcolor=ft.colors.BLUE,
                        on_click=self.fetchPath
                    )
            ],
            spacing=15
        )

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
            disabled=True if len(self.paths) < 1 else False,
            on_click=super().createData
        )
        self.containerConfirm = ft.Row([self.buttonConfirm], height=70)
        return self.containerConfirm


    def createContainerView(self):
        if len(self.paths) > 0:
            self.container_view = ft.Column(
                [ft.Text(value=item) for item in self.paths],
                height=70,
                scroll=ft.ScrollMode.AUTO,
                visible=True if len(self.paths) > 0 else False,
                width = self.page.window_width
            )
            return self.container_view
        else:
            self.container_view = ft.Column(
                height=70,
                scroll=ft.ScrollMode.AUTO,
                visible=False,
                width = self.page.window_width
            )
            return self.container_view


    def fetchText(self, e):
        self.value = e.control.value
        return str(self.value)


    def cleanField(self):
        self.field_path.value = ''
        self.page.update()


    def fetchPath(self, e=''):
        if len(self.value) > 0:
            self.paths.append(self.value)
            print(list(self.paths))
            self.container_view.controls.append(ft.Text(value=self.value))
            self.container_view.visible = True
            self.container_view.width = self.page.window_width
            self.buttonConfirm.disabled = False
            self.cleanField()
        else:
            print('Type your path first')


if __name__ == '__main__':
    ft.app(target=App)