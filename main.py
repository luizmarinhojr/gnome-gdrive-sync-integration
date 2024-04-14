import flet as ft
from data import Data


class App():
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.window_width = 450
        self.page.window_height = 550
        self.page.title = 'Gdrive Sync'
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.Data = Data()
        self.data = self.Data.fetchData()
        self.running_program = False
        self.selected_first_directory = False
        self.selected_path = False
        self.selected_mail = False
        self.main()


    def main(self):
        empty = False
        for item in self.data:
            if len(self.data[item]) < 1: # Verify if all items on dict are empty
                empty = True
        
        if not empty:
            self.selected_first_directory = True
            self.selected_path = True
            self.selected_mail = True


        # JUST ELEMENTS
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result
        )

        self.field_path = ft.TextField(
            value = self.data['path'],
            hint_text = 'Select the path to monitor',
            expand = True,
            disabled = True
        )

        self.field_mail = ft.TextField(
            value = self.data['usermail'],
            hint_text = 'Type your mail',
            expand = True,
            disabled = False,
            on_change = self.captureTextMail,
            suffix = ft.Text('@gmail.com')
        )

        self.field_first_folder = ft.TextField(
            value = self.data['folder'],
            hint_text = 'Type the first directory name on Google Drive',
            expand = True,
            disabled = False,
            on_change = self.captureTextFirstFolder,
        )

        self.button_save_all = ft.ElevatedButton(
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
            icon = ft.icons.SYNC,
            bgcolor = ft.colors.BLUE,
            disabled = True if empty == True else False,
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
                        size=14,
                        color = ft.colors.WHITE70,
                )]
            ),
                ft.Row([
                    self.field_path,
                    ft.FloatingActionButton(
                        icon = ft.icons.DRIVE_FOLDER_UPLOAD,
                        bgcolor = ft.colors.BLUE,
                        on_click = lambda _: self.pick_files_dialog.get_directory_path()
                    )
                ])
            ]),
            ft.Column([
                ft.Row([
                    ft.Text(
                        'Type your mail',
                        size = 14,
                        color = ft.colors.WHITE70
                    )]
                ),
                ft.Row([
                    self.field_mail
                ])
            ]),
            ft.Column([
                ft.Row([
                    ft.Text(
                        'Type the drive directory',
                        size = 14,
                        color = ft.colors.WHITE70,
                    )]
                ),
                ft.Row([
                    self.field_first_folder
                ])
            ])
            ], spacing=25)

        self.container_monitoring = ft.Column([
            ft.Row(
                [ft.Icon(ft.icons.INFO, size = 17), ft.Text(value = 'Save all and later Active the Sync')]
            )
        ])

        self.container_confirm = ft.Container(
            ft.Column([
                ft.Row([self.button_save_all]),
                ft.Row([self.button_active_sync]),
                ft.Row([self.button_stop_sync])
            ]),
            padding = ft.padding.symmetric(vertical=20)
        )

        self.page.overlay.append(self.pick_files_dialog)

        self.page.add(container_field, self.container_monitoring, self.container_confirm)


    def pick_files_result(self, e):
        self.data['path'] = '' if e.path == None else e.path
        if len(self.data['path']) > 0:
            self.selected_path = True
        self.verifyInputs()
        self.field_path.value = e.path
        self.field_path.update()


    def captureTextMail(self, e):
        self.data['usermail'] = e.control.value
        self.selected_mail = True if len(self.data['usermail']) > 3 else False
        self.verifyInputs()


    def captureTextFirstFolder(self, e):
        self.data['folder'] = e.control.value
        self.selected_first_directory = True if len(self.data['folder']) > 0 else False
        self.verifyInputs()

    
    def verifyInputs(self):
        if self.selected_path and self.selected_mail and self.selected_first_directory:
            self.button_save_all.disabled = False
            self.button_save_all.update()
        else:
            self.button_save_all.disabled = True
            self.button_save_all.update()


    def saveAll(self, e):
        self.Data.saveAll(data = self.data)
        self.button_save_all.disabled = True
        self.button_active_sync.disabled = False
        self.button_save_all.update()
        self.button_active_sync.update()


    def executeProgram(self, e):
        self.running_program = self.Data.executeProgram()
        self.container_monitoring.controls.pop()
        self.container_monitoring.controls.append(ft.Row([ft.Icon(ft.icons.CHECK, size = 17), ft.Text(value = f'Monitoring now {self.data["path"]}')]))
        self.button_active_sync.visible = False
        self.button_stop_sync.visible = True
        self.container_confirm.update()
        self.container_monitoring.update()

    
    def stopProgram(self, e):
        self.running_program = self.Data.killProgram()
        self.container_monitoring.controls.pop()
        self.container_monitoring.controls.append(ft.Row([ft.Icon(ft.icons.INFO, size = 17), ft.Text(value = 'Save all and later Active the Sync')]))
        self.button_active_sync.visible = True
        self.button_stop_sync.visible = False
        self.container_monitoring.update()
        self.container_confirm.update()


if __name__ == '__main__':
    ft.app(target=App)
