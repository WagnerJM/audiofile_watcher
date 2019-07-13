import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pydub import AudioSegment

import logging

# Create a custom logger
name = __name__
logger = logging.getLogger(name)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(f"/media/festplatte/public/logs/{name}.log")
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

class Watcher:
    DIRECTORY_TO_WATCH = "/media/festplatte/public/recordings/input"
    OUTPUT_DIR = "/media/festplatte/public/recordings/output"

    def __init__(self):
        #logger.info("Creating observer")
        print("Creating observer")
        self.observer = Observer()

    def run(self):
        logger.info("Creating Event Handler")
        print("Creating Event Handler")
        event_handler = Handler()
        self.observer.schedule(
            event_handler,
           self.DIRECTORY_TO_WATCH,
            recursive=False
        )
        print("Starting observer")
        logger.info("Starting observer")

        self.observer.start()
        try:
            while True:
                time.sleep(60)
        except:
            self.observer.stop()
            logger.error("An Error occured, stopping watcher")
        
        self.observer.join()


class Handler(FileSystemEventHandler):

    DIRECTORY_TO_WATCH = "/media/festplatte/public/recordings/input"
    OUTPUT_DIR = "/media/festplatte/public/recordings/output"
    
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == "created":
            logger.debug("File found")
            # Check if file is wav file
            file_list = os.listdir(Handler.DIRECTORY_TO_WATCH)
            logger.debug(f"File list: {file_list}")
            for track in file_list:
                if track == "GOOD":
                    return None
                else:

                    if track.endswith(".wav"):
                        trackname, ext = track.split(".")
                        from_path = "{}/{}".format(
                            Handler.DIRECTORY_TO_WATCH, track)
                        export_path = "{}/{}.mp3".format(
                            Handler.OUTPUT_DIR, trackname)
                        # create mp3 file from wave file
                        logger.info("Creating mp3 file")
                        
                        try:
                            AudioSegment.from_wav(from_path).export(export_path, format="mp3")
                            logger.info("mp3-file was created")
                        except Exception as e:
                            logger.error("Could not create mp3-file")  
                            logger.error(e)

                        try:

                            # move wav file to GOOD location
                            logger.info(f"Moving {trackname} to GOOD/")
                            shutil.move(from_path, Handler.DIRECTORY_TO_WATCH + "/GOOD/" + track)
                        except Exception as e:
                            logger.error("Could not move file")
                            logger.error(e)
