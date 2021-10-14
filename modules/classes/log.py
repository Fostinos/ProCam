from datetime import datetime
import jsonpickle
import os

class Path:
    # constants 
    projectDirectory = '/home/pi/ProCam/'
    configDirectory = projectDirectory + 'config'
    shotDirectory = projectDirectory + 'screenshots'
    videoDirectory = projectDirectory + 'videos'

    # constructor

    def __init__(self, id : int):
        self.original = os.path.sep.join([Path.shotDirectory, 'shot_{}_original.png'.format(id)])
        self.video = os.path.sep.join([Path.videoDirectory, 'vid_{}.mp4'.format(id)])
        self.images = []
    
    # add image 
    @staticmethod
    def add_image(images : list, id : int, now : int):
        image = os.path.sep.join([Path.shotDirectory, 'shot_{}_image_{}.png'.format(id, now)])
        images.append(image)
        pass


class Log:
    
    # constructor

    def __init__(self, id : int):
        path = os.path.sep.join([Path.configDirectory, 'log_{}.json'.format(id)])
        if not os.path.exists(path):
            self.ID = id
            self.date = datetime.now().strftime("%d %B %Y at %H:%M:%S")
            self.path = Path(id)
        else:
            with open(path, 'rt') as file :
                config = file.read()
            log : Log = jsonpickle.decode(config)
            self.ID = log.ID
            self.date = log.date
            self.path = log.path
    
    # getter json method

    def getJson(self):
        return jsonpickle.encode(self, indent=4)

