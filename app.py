import flet as ft
import time
from data import Data


class App(Data):
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Gdrive Sync'
        self.page.window_width = 500
        self.page.window_height = 600
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.on_resize = self.resizePage
        self.data = super().fetchData()
        self.paths = [] if len(self.data) < 0 else self.data
        self.main()


    def main(self):
        # JUST ELEMENTS
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result
        )

        self.field_path = ft.TextField(
            value=self.paths[0],
            hint_text='Select the path you want to monitor',
            expand=True,
            disabled=True
        )

        self.buttonConfirm = ft.ElevatedButton(
            text = 'Confirm paths and active Sync',
            expand = True,
            height = 40,
            color = ft.colors.WHITE,
            icon = ft.icons.CHECK,
            bgcolor = ft.colors.BLUE,
            disabled = False if len(self.paths) > 0 else True,
            on_click = super().savePaths
        )

        container_field = ft.Row(
            [self.field_path, ft.FloatingActionButton(
                        icon = ft.icons.FOLDER,
                        bgcolor = ft.colors.BLUE,
                        on_click = lambda _: self.pick_files_dialog.get_directory_path()
                    )
            ],
            spacing = 15
        )

        self.container_monitoring = ft.Column([ft.Row(
            [ft.Icon(ft.icons.CHECK), ft.Text(value=f'Monitoring: {self.paths[0]}')]
        )]
        )

        self.container_confirm = ft.Row(
            [self.buttonConfirm],
            height = 70
        )

        self.page.overlay.append(self.pick_files_dialog)

        self.page.add(container_field, self.container_monitoring, self.container_confirm)


    def resizePage(self, e):
        time.sleep(1)
        print('Page resized')
        self.page.update() # When page resized, the page will update


    def pick_files_result(self, e):
        self.paths.append(e.path)
        self.field_path.value = e.path
        self.container_monitoring.controls.append(ft.Row([ft.Icon(ft.icons.WARNING, color=ft.colors.YELLOW), ft.Text(value=f'Do you wanna change to {self.paths[-1]} ?')]))
        self.field_path.update()
        self.container_monitoring.update()
        print(self.paths)


if __name__ == '__main__':
    ft.app(target=App)