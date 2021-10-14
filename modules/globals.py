import modules.config as cfg
import cv2

cfg.setConfigOnTelemetry("system")

# Global variables
global telemetry, camera, param, rec_frame, recorder, recording, recordID, analyzer, now, stop
global enable_intruder, enable_camera, enable_kernel, enable_surface, enable_mask

telemetry = cfg.Telemetry.getInstance()
param = telemetry.cam
camera = cv2.VideoCapture(0)
camera.release()
cv2.destroyAllWindows()
rec_frame = 0
recorder = 0
recording = False
recordID = telemetry.ID
analyzer = 0
now = 0
stop = 0
enable_intruder = False
enable_camera = False
enable_kernel = False
enable_surface = False
enable_mask = False