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
        self.running_program = False
        self.main()


    def main(self):
        # JUST ELEMENTS
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result
        )

        self.field_path = ft.TextField(
            hint_text = 'Select the path you want to monitor',
            expand = True,
            disabled = False
        )

        self.button_save_paths = ft.ElevatedButton(
            text = 'Save paths',
            expand = True,
            height = 45,
            color = ft.colors.WHITE,
            icon = ft.icons.SAVE,
            bgcolor = ft.colors.BLUE,
            disabled = True,
            on_click = self.savePaths
        )

        self.button_active_sync = ft.ElevatedButton(
            text = 'Active Sync',
            expand = True,
            height = 45,
            color = ft.colors.WHITE,
            icon = ft.icons.CHECK,
            bgcolor = ft.colors.BLUE,
            disabled = False if len(self.paths) > 0 else True,
            on_click = self.executeProgram
        )

        self.button_stop_sync = ft.ElevatedButton(
            text = 'Stop Sync',
            expand = True,
            height = 45,
            color = ft.colors.WHITE,
            icon = ft.icons.CHECK,
            bgcolor = ft.colors.BLUE,
            disabled = False,
            on_click = self.stopProgram
        )

        #JUST CONTAINERS
        container_field = ft.Row(
            [self.field_path, ft.FloatingActionButton(
                        icon = ft.icons.FOLDER,
                        bgcolor = ft.colors.BLUE,
                        on_click = lambda _: self.pick_files_dialog.get_directory_path()
                    )
            ],
            spacing = 15
        )

        self.container_monitoring = ft.Column([
            ft.Row(
                [ft.Icon(ft.icons.INFO, size = 17), ft.Text(value = f'Monitoring: {self.paths[0]}' if len(self.paths) > 0 else 'The path will appear here')]
            )
        ])

        self.container_confirm = ft.Container(
            ft.Column([
                ft.Row([self.button_save_paths]),
                ft.Row([self.button_active_sync])
            ]),
            padding = ft.padding.symmetric(vertical=20)
        )

        self.page.overlay.append(self.pick_files_dialog)

        self.page.add(container_field, self.container_monitoring, self.container_confirm)


    def resizePage(self, e):
        time.sleep(1)
        print('Page resized')
        self.page.update() # When page resized, the page will update


    def pick_files_result(self, e):
        self.paths.pop()
        self.paths.append(e.path)
        self.field_path.value = self.field_path.hint_text
        self.container_monitoring.controls.pop()
        self.container_monitoring.controls.append(ft.Row([ft.Icon(ft.icons.WARNING, size = 17), ft.Text(value = f'Confirm to monitor this path? {self.paths[0]}')]))
        self.button_save_paths.disabled = False
        self.field_path.update()
        self.container_monitoring.update()   
        self.button_save_paths.update()
        print(self.paths)
    

    def savePaths(self, e):
        super().savePaths()
        self.button_save_paths.disabled = True
        self.button_active_sync.disabled = False
        self.button_save_paths.update()
        self.button_active_sync.update()


    def executeProgram(self, e):
        self.running_program = super().executeProgram()
        self.container_monitoring.controls.pop()
        self.container_monitoring.controls.append(ft.Row([ft.Icon(ft.icons.CHECK, size = 17), ft.Text(value = f'Monitoring now {self.paths[0]}')]))
        self.container_confirm.content.controls.pop()
        self.container_confirm.content.controls.append(ft.Row([self.button_stop_sync]))
        self.container_confirm.update()
        self.container_monitoring.update()

    
    def stopProgram(self, e):
        self.running_program = super().killProgram()
        self.container_confirm.content.controls.pop()
        self.container_confirm.content.controls.append(ft.Row([self.button_active_sync]))
        self.container_confirm.update()


if __name__ == '__main__':
    ft.app(target=App)