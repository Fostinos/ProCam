import modules.globals as gb
from modules.globals import cv2
from modules.globals import cfg
from modules.globals import param
from threading import Thread
from datetime import datetime
import os
import time
import numpy as np


def recording():
    cfg.saveRecordingLog(gb.recordID)
    gb.now = int(time.time())
    gb.stop = gb.now + param.duration
    gb.recording = True
    while gb.now < gb.stop :
        gb.recorder.write(cv2.flip(gb.rec_frame, 1))
        time.sleep(0.02)
        gb.now = int(time.time())
    gb.recordID += 1
    gb.telemetry.ID = gb.recordID
    cfg.saveTelemetryConfig('system')
    gb.recording = False
    gb.recorder.release() 
    cv2.destroyAllWindows()


def record():
    # codec AVC ( compatible with browser )
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    # format MP4 
    path = os.path.sep.join([cfg.videoDirectory, 'vid_{}.mp4'.format(gb.recordID)])
    gb.recorder = cv2.VideoWriter(path, fourcc, 20, (640, 480))
    # start new thread for recording the video
    thread = Thread(target = recording, args = [])
    thread.start()


def save_image(frame, filename : str):
    if filename.endswith('original'):
        path = os.path.sep.join([cfg.shotDirectory, 'shot_{}.png'.format(filename)])
        cv2.imwrite(path, frame)
    else:
        now = gb.now
        if (gb.stop - now)%5 == 0:
            path = os.path.sep.join([cfg.shotDirectory, 'shot_{}_{}.png'.format(filename, now)])
            if not os.path.exists(path):
                cv2.imwrite(path, frame)
                cfg.saveImageLog(gb.recordID, now)


def gen_frames():  # generate frame by frame from camera
    success = False
    if gb.enable_camera: # camera online
        if not gb.camera.isOpened():
            gb.camera = cv2.VideoCapture(0)
        success, original = gb.camera.read()  # previous image
        if success:
            original = cv2.rotate(original, cv2.ROTATE_180)
    else: # camera offline
        path = os.path.sep.join([cfg.shotDirectory, 'shot_{}_original.png'.format(gb.recordID-1)])
        if os.path.exists(path):
            original = cv2.imread(path, cv2.IMREAD_UNCHANGED) # last previous image
            success = True
    if success:
        # change previous color image to gray image
        original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)  
        # apply a blur on the previous gray image
        original_gray = cv2.GaussianBlur(original_gray, (param.kernel_blur, param.kernel_blur), 0)  
        kernel_dilate = np.ones((3, 3), np.uint8)
        while True:
            # check camera state
            #########################################################
            success = False
            if not gb.enable_camera :
                if gb.camera.isOpened():
                    gb.camera.release()
                    cv2.destroyAllWindows()
            else:
                if not gb.camera.isOpened():
                    gb.camera = cv2.VideoCapture(0)
                success, frame = gb.camera.read()  # current image
            ##########################################################

            if success: # camera online
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                # change current image's color to gray
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
                # apply a blur on the gray image
                gray = cv2.GaussianBlur(gray, (param.kernel_blur, param.kernel_blur), 0)  
                # create a mask
                mask = cv2.absdiff(original_gray, gray)  
                # increase intensity of the mask
                mask = cv2.threshold(mask, param.mask_threshold, 255, cv2.THRESH_BINARY)[1]  
                # magnify the size of mask objects
                mask = cv2.dilate(mask, kernel_dilate, iterations=3)  
                # get all contours
                contours, nada = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
                original = frame
                original_gray = gray
                # detect intruder
                if gb.enable_intruder:
                    for c in contours:
                        if cv2.contourArea(c) < param.surface_threshold:
                            continue
                        if not gb.recording:
                            param.intruder = True
                            gb.rec_frame = frame.copy()
                            filename = '{}_original'.format(gb.recordID)
                            save_image(original, filename)
                        break
                    if param.intruder:
                        param.intruder = False
                        record()
                        time.sleep(0.1)
                    if gb.recording:
                        gb.rec_frame = frame.copy()
                        filename = '{}_image'.format(gb.recordID)
                        save_image(frame, filename)
                else:
                    gb.recording = False
                # prepare browser image 
                try:
                    if gb.recording: 
                        for c in contours:
                            if cv2.contourArea(c) < param.surface_threshold:
                                continue
                            x, y, w, h=cv2.boundingRect(c)
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    # one if condition will be true or all conditions will be false :
                    ###############################################################
                    if gb.enable_kernel:
                        frame = gray
                    elif gb.enable_surface:
                        for c in contours:
                            if cv2.contourArea(c) < param.surface_threshold:
                                cv2.drawContours(frame, [c], 0, (0, 255, 0), 5)
                                continue
                            cv2.drawContours(frame, [c], 0, (0, 0, 255), 5)
                    elif gb.enable_mask:
                        frame = mask
                    #############################################################
                    if gb.recording:
                        timeString = datetime.now().strftime("%d %B %Y at %H:%M:%S")
                        frame = cv2.putText(cv2.flip(frame, 1), timeString, (100,30),
                                            cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,0,255), 4)
                        frame = cv2.flip(frame, 1)
                    success, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                    if success:
                        buffer = buffer.tobytes()
                        yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n')
                except Exception as e:
                    pass

            else:  # camera offline
                try:
                    offString = "OFF : " + datetime.now().strftime("%d %B %Y at %H:%M:%S")
                    frame = cv2.putText(cv2.flip(original, 1), offString, (50,30),
                                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,0,255), 4)
                    frame = cv2.flip(frame, 1)
                    success, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                    if success:
                        buffer = buffer.tobytes()
                        yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n')
                except Exception as e:
                    pass
    
