import time
import commands as comm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    running = True
    def __init__(self):
        self.commands = comm.Commands()
    
    def on_any_event(self, event):
        if event.is_directory:
            if event.event_type == 'created':
                print(f'Directory created: {event.src_path}')
                self.commands.createDirectory(event.src_path)

            elif event.event_type == 'modified':
                print(f'Directory modified: {event.src_path}')

            elif event.event_type == 'deleted':
                print(f'Directory deleted: {event.src_path}')
                
        else:
            if event.event_type == 'created':
                print(f'File created: {event.src_path}')
                self.commands.createFile(event.src_path)

            elif event.event_type == 'modified':
                print(f'File modified: {event.src_path}')
                self.commands.modifiedFile(event.src_path)

            elif event.event_type == 'deleted':
                print(f'File deleted: {event.src_path}')


# def startProgram():
#     path = "/home/machine/Documents"  # Directory to monitor
#     event_handler = MyHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#             if MyHandler.running == False:
#                 raise KeyboardInterrupt
#     except KeyboardInterrupt:
#         observer.stop()
#         print('Sync Stopped')
#     observer.join()
