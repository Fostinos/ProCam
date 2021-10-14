from modules.classes.picam import PiCam
from modules.classes.color import Color as color
import platform, psutil

class Telemetry:

    # singleton instance
    __instance = None

    # constructor

    def __init__(self):
        if Telemetry.__instance != None:
            print(color.RED + 'ERROR Singleton : this class is a singleton!' + color.END)
            raise Exception("This class is a singleton!")
        else:
            Telemetry.__instance = self
            self._ID = 0
            self._cam = PiCam()
            self._about = self.__get_about()
            

    # static method : getter singleton instance

    @staticmethod
    def getInstance():
        if Telemetry.__instance == None:
            Telemetry()
        return Telemetry.__instance
    
    # private method : getter about pi

    def __get_about(self) :
        infos={}
        infos['platform'] = platform.system()
        infos['platform-release']=platform.release()
        infos['platform-version']=platform.version()
        infos['architecture']=platform.machine()
        infos['processor']=platform.processor()
        infos['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return infos

    # getters

    @property
    def ID(self):
        return self._ID

    @property
    def cam(self):
        return self._cam

    @property
    def about(self):
        return self._about
    

    # setters

    @ID.setter
    def ID(self, new_ID):
        if isinstance(new_ID, int):
            self._ID = new_ID
        else :
            print(color.RED + 'ERROR ID : the value must be between <class \'int\'>' + color.END)
            print(color.RED + 'ATTENTION ID : the default value is setting...' + color.END)
            self._ID = 0

    @cam.setter
    def cam(self, new_cam):
        if isinstance(new_cam, PiCam):
            self._cam.kernel_blur = new_cam.kernel_blur
            self._cam.surface_step = new_cam.surface_step
            self._cam.surface_threshold = new_cam.surface_threshold
            self._cam.mask_threshold = new_cam.mask_threshold
            self._cam.duration = new_cam.duration
            self._cam.intruder = False # to avoid recording of intruder during the setting
        else :
            print(color.RED + 'ERROR cam : the value must be between <class \'PiCam\'>' + color.END)
            print(color.RED + 'ATTENTION cam : the default value is setting...' + color.END)
            self._cam = PiCam()