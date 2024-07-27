
#from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
#create an event handler that listens for when (for our code) a file is created
#hence the check for is not a directory
#we create event handler Observer obj. run our script
#join and close when everything is done
class DownloadHandler(FileSystemEventHandler):
    def __init__(self,target_name):
        self.target_name = target_name
    
    def on_create(self,event):
        if not event.is_directory:
            file_path = event.src_path  # source path of what triggered the event aka our "new download"
            ##wait until our file download is finished##
            try:
                timeout = 0
                download_incomp = True
                while download_incomp and timeout < 60:
                    download_incomp = False
                    for items in os.listdir(file_path):
                        if items.endswith('.crdownload'):
                            download_incomp = True
                            timeout += 1
                            continue
            except Exception as e:
                print(e)
                print("File failed to download.")