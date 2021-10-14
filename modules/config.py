import jsonpickle
import os
from modules.classes.telemetry import Telemetry
from modules.classes.log import Log, Path
import logging
from logging.handlers import RotatingFileHandler

projectDirectory = '/home/pi/ProCam/'
configDirectory = projectDirectory + 'config'
shotDirectory = projectDirectory + 'screenshots'
videoDirectory = projectDirectory + 'videos'

log_critic = os.path.sep.join([configDirectory, 'system_critic.log'])
log_error = os.path.sep.join([configDirectory, 'system_error.log'])
log_warning = os.path.sep.join([configDirectory, 'system_warning.log'])
log_info = os.path.sep.join([configDirectory, 'system_info.log'])

format ='%(asctime)s -- %(module)s -- %(funcName)s -- %(msecs)d -- %(name)s -- %(processName)s -- %(levelname)s -- %(message)s'
formatter = logging.Formatter(format)

handler_critic = RotatingFileHandler(log_critic, mode="a", maxBytes=10000, backupCount=5, encoding="utf-8")
handler_error = RotatingFileHandler(log_error, mode="a", maxBytes=10000, backupCount=5, encoding="utf-8")
handler_warning = RotatingFileHandler(log_warning, mode="a", maxBytes=10000, backupCount=5, encoding="utf-8")
handler_info = RotatingFileHandler(log_info, mode="a", maxBytes=10000, backupCount=5, encoding="utf-8")

handler_critic.setFormatter(formatter)
handler_error.setFormatter(formatter)
handler_warning.setFormatter(formatter)
handler_info.setFormatter(formatter)

handler_critic.setLevel(logging.CRITICAL)
handler_error.setLevel(logging.ERROR)
handler_warning.setLevel(logging.WARNING)
handler_info.setLevel(logging.INFO)

root_logger = logging.getLogger()
logger = logging.getLogger('PI')
logger.setLevel(logging.INFO)

root_logger.addHandler(handler_critic)
root_logger.addHandler(handler_error)
root_logger.addHandler(handler_warning)
logger.addHandler(handler_info) 

def getConfigFromTelemetry():
    return jsonpickle.encode(Telemetry.getInstance(), indent=4)

def getTelemetryFromConfig(config):
    return jsonpickle.decode(config)

def updateTelemetryFromConfig(config):
    system : Telemetry = getTelemetryFromConfig(config)
    Telemetry.getInstance().cam = system.cam
    Telemetry.getInstance().ID = system.ID

def setConfigOnTelemetry(filename):
    path = os.path.sep.join([configDirectory, filename + '.json'])
    with open(path, 'rt') as f:
        config = f.read()
    updateTelemetryFromConfig(config)

def saveTelemetryConfig(filename):
    path = os.path.sep.join([configDirectory, filename + '.json'])
    config = getConfigFromTelemetry()
    with open(path, 'w') as file:
        file.write(config)

def saveRecordingLog(id : int):
    path = os.path.sep.join([configDirectory, 'log_{}.json'.format(id)])
    if not os.path.exists(path):
        config = Log(id).getJson()
        with open(path, 'w') as file:
            file.write(config)

def saveImageLog(id : int, now : int):
    path = os.path.sep.join([configDirectory, 'log_{}.json'.format(id)])
    log = Log(id)
    Path.add_image(log.path.images, id, now)
    config = log.getJson()
    with open(path, 'w') as file:
        file.write(config)

def setLog(id : int, now : int):
    path = os.path.sep.join([configDirectory, 'log_{}.json'.format(id)])
    log = Log(id)
    Path.add_image(log.path.images, id, now)
    config = log.getJson()
    with open(path, 'w') as file:
        file.write(config)