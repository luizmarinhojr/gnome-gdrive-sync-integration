import flet as ft
import time
from data import Data


class App(Data):
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Gdrive Sync'
        self.page.window_width = 600
        self.page.window_height = 600
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.data = ''
        self.paths = super().fetchData()
        self.user = super().fetchUser()
        print(self.user)
        self.running_program = False
        self.selected_path = False
        self.selected_mail = False
        self.main()


    def main(self):
        # JUST ELEMENTS
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result
        )

        self.field_path = ft.TextField(
            text_align = ft.TextAlign.CENTER,
            value = self.paths[0] if len(self.paths) > 0 else '',
            hint_text = 'Select the path to monitor',
            expand = True,
            disabled = False
        )

        self.field_mail = ft.TextField(
            text_align=ft.TextAlign.CENTER,
            value = self.user[0] if len(self.user) > 0 else '',
            hint_text = 'Type your mail',
            expand = True,
            disabled = False,
            on_change = self.captureTextMail,
            suffix = ft.Text('@gmail.com')
        )

        self.field_first_directory = ft.TextField(
            text_align=ft.TextAlign.CENTER,
            value = self.user[0] if len(self.user) > 0 else '',
            hint_text = 'Type the first directory name on Google Drive',
            expand = True,
            disabled = False,
            on_change = self.captureTextFirstDirectory,
        )

        self.button_save_paths = ft.ElevatedButton(
            text = 'Save all',
            expand = True,
            height = 45,
            color = ft.colors.WHITE,
            icon = ft.icons.SAVE,
            bgcolor = ft.colors.BLUE,
            disabled = True,
            on_click = self.saveAll
        )

        self.button_active_sync = ft.ElevatedButton(
            text = 'Active Sync',
            expand = True,
            height = 45,
            color = ft.colors.WHITE,
            icon = ft.icons.CHECK,
            bgcolor = ft.colors.BLUE,
            disabled = False if len(self.paths) > 0 else True,
            visible = True,
            on_click = self.executeProgram
        )

        self.button_stop_sync = ft.ElevatedButton(
            text = 'Stop Sync',
            expand = True,
            height = 45,
            color = ft.colors.WHITE,
            icon = ft.icons.CLOSE,
            bgcolor = ft.colors.RED,
            disabled = False,
            visible = False,
            on_click = self.stopProgram
        )

        #JUST CONTAINERS
        container_field = ft.Column([
            ft.Column([
                ft.Row([
                    ft.Text(
                        'Choose the path to monitor',
                        size=16,
                        color = ft.colors.WHITE70,
                )],
                alignment=ft.MainAxisAlignment.CENTER
            ),
                ft.Row([
                    self.field_path,
                    ft.FloatingActionButton(
                        icon = ft.icons.FOLDER,
                        bgcolor = ft.colors.BLUE,
                        on_click = lambda _: self.pick_files_dialog.get_directory_path()
                    )]
                )
            ]),
            ft.Column([
                ft.Row([
                    ft.Text(
                        'Type you mail',
                        size = 16,
                        color = ft.colors.WHITE70
                    )],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row([
                    self.field_mail
                ])
            ]),
            ft.Column([
                ft.Row([
                    ft.Text(
                        'Type the drive directory',
                        size = 16,
                        color = ft.colors.WHITE70,
                    )],
                    alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    self.field_first_directory
                ])
            ])
        ], spacing=25)

        self.container_monitoring = ft.Column([
            ft.Row(
                [ft.Icon(ft.icons.INFO, size = 17), ft.Text(value = f'Monitoring: {self.paths[0]}' if len(self.paths) > 0 else 'Save all and later Active the Sync')]
            )
        ])

        self.container_confirm = ft.Container(
            ft.Column([
                ft.Row([self.button_save_paths]),
                ft.Row([self.button_active_sync]),
                ft.Row([self.button_stop_sync])
            ]),
            padding = ft.padding.symmetric(vertical=20)
        )

        self.page.overlay.append(self.pick_files_dialog)

        self.page.add(container_field, self.container_monitoring, self.container_confirm)


    def pick_files_result(self, e):
        if len(self.paths) > 0:
            self.paths.pop()
        self.paths.append('' if e.path == None else e.path)
        self.field_path.value = e.path
        if len(self.paths[0]) > 0:
            self.selected_path = True
        self.verifyInputs()
        self.field_path.update()
        print(self.paths)


    def captureTextMail(self, e):
        self.mail = e.control.value
        self.selected_mail = True if len(self.mail) > 3 else False

    
    def captureTextFirstDirectory(self, e):
        self.first_directory = e.control.value
        self.selected_first_directory = True if len(self.first_directory) > 0 else False
        self.verifyInputs()

    
    def verifyInputs(self):
        if self.selected_path and self.selected_mail and self.selected_first_directory:
            self.button_save_paths.disabled = False
            self.button_save_paths.update()
        else:
            self.button_save_paths.disabled = True
            self.button_save_paths.update()


    def saveAll(self, e):
        super().savePaths(mail=self.mail)
        self.button_save_paths.disabled = True
        self.button_active_sync.disabled = False
        self.button_save_paths.update()
        self.button_active_sync.update()


    def executeProgram(self, e):
        self.running_program = super().executeProgram()
        self.container_monitoring.controls.pop()
        self.container_monitoring.controls.append(ft.Row([ft.Icon(ft.icons.CHECK, size = 17), ft.Text(value = f'Monitoring now {self.paths[0]}')]))
        self.button_active_sync.visible = False
        self.button_stop_sync.visible = True
        self.container_confirm.update()
        self.container_monitoring.update()

    
    def stopProgram(self, e):
        self.running_program = super().killProgram()
        self.button_active_sync.visible = True
        self.button_stop_sync.visible = False
        self.container_confirm.update()


if __name__ == '__main__':
    ft.app(target=App)