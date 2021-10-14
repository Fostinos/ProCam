from modules.classes.log import Log
from modules.classes.picam import PiCam
from flask import Flask, render_template, request, Response, jsonify, abort
import json
import io
from base64 import encodebytes
from PIL import Image
import modules.globals as gb
from modules.globals import cfg
import modules.processing as process
from modules.classes.monitor import Monitor


#########################################################################


def set_telemetry_duration(duration : str):
   if duration != None:
      try:
         gb.param.duration = int(duration)
         data = '"duration":{}'.format(duration)
      except:
         data = '"duration":{}'.format('null')
   else :
      data = '"duration":{}'.format('null')
   data = '{' + data + '}'
   return json.loads( data )

def get_camera():
   data = ""
   if gb.enable_camera:
      data = data + '"state":{}'.format('true')
   else:
      data = data + '"state":{}'.format('false')
   if gb.enable_intruder:
      data = data + ', "intruder":{}'.format('true')
   else :
      data = data + ', "intruder":{}'.format('false')
   data = '{' + data + '}'
   return json.loads( data )

def set_camera_state(state : str):
   if state != None:
      if state == 'false' or state == '0':
         gb.enable_camera = False
         data = '"state":{}'.format('false')
      else:
         gb.enable_camera = True
         data = '"state":{}'.format('true')
   else :
      data = '"state":{}'.format('null')
   data = '{' + data + '}'
   return json.loads( data )

def set_camera_intruder(intruder : str):
   if intruder != None:
      if intruder == 'false' or intruder == '0':
         gb.enable_intruder = False
         data = '"intruder":{}'.format('false')
      else:
         gb.enable_intruder = True
         data = '"intruder":{}'.format('true')
   else :
      data = '"intruder":{}'.format('null')
   data = '{' + data + '}'
   return json.loads( data )

def get_response_image(image_path):
   pil_img = Image.open(image_path, mode='r') # reads the PIL image
   byte_arr = io.BytesIO()
   pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
   encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
   return encoded_img

#########################################################################

app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')

@app.route('/video_feed')
def video_feed():
   return Response(process.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/explorer")
def file():
   return render_template('explorer.html')

@app.route("/about")
def about():
   return render_template('about.html')

@app.route("/api/monitoring")
def monitor():
   data = json.loads(Monitor.getJson())
   return jsonify(data)

@app.route('/api/telemetry', methods = ['GET'])
def telemetry():
   data = json.loads(cfg.getConfigFromTelemetry().replace('\"_','\"'))
   return jsonify(data)

@app.route('/api/telemetry/default', methods = ['POST'])
def telemetry_default():
   gb.telemetry.cam = PiCam()
   data = json.loads(cfg.getConfigFromTelemetry().replace('\"_','\"'))
   cfg.saveTelemetryConfig("system")
   cfg.logger.info(request.remote_addr + ' : RESET')
   return jsonify(data)

@app.route('/api/telemetry/kernel_blur', methods = ['POST'])
def telemetry_kernel_blur():
   operation = request.form.get('operation', type=int)
   if operation == 1:
      gb.param.increase_kernel_blur()
   elif operation == -1:
      gb.param.decrease_kernel_blur()
   gb.enable_camera = True
   gb.enable_intruder = False
   gb.enable_kernel = True
   gb.enable_surface = False
   gb.enable_mask = False
   data = '"kernel_blur":{}'.format(gb.param.kernel_blur)
   data = json.loads( '{' + data + '}' )
   cfg.saveTelemetryConfig("system")
   cfg.logger.info(request.remote_addr + ' : ' + str(data))
   return jsonify(data)

@app.route('/api/telemetry/surface_step', methods = ['POST'])
def telemetry_surface_step():
   operation = request.form.get('operation', type=int)
   if operation == 1:
      gb.param.increase_surface_step()
   elif operation == -1:
      gb.param.decrease_surface_step()
   gb.enable_camera = True
   gb.enable_intruder = False
   gb.enable_kernel = False
   gb.enable_surface = True
   gb.enable_mask = False
   data = '"surface_step":{}'.format(gb.param.surface_step)
   data = json.loads( '{' + data + '}' )
   cfg.saveTelemetryConfig("system")
   cfg.logger.info(request.remote_addr + ' : ' + str(data))
   return jsonify(data)

@app.route('/api/telemetry/surface_threshold', methods = ['POST'])
def telemetry_surface_threshold():
   operation = request.form.get('operation', type=int)
   if operation == 1:
      gb.param.increase_surface_threshold()
   elif operation == -1:
      gb.param.decrease_surface_threshold()
   gb.enable_camera = True
   gb.enable_intruder = False
   gb.enable_kernel = False
   gb.enable_surface = True
   gb.enable_mask = False
   data = '"surface_threshold":{}'.format(gb.param.surface_threshold)
   data = json.loads( '{' + data + '}' )
   cfg.saveTelemetryConfig("system")
   cfg.logger.info(request.remote_addr + ' : ' + str(data))
   return jsonify(data)

@app.route('/api/telemetry/mask_threshold', methods = ['POST'])
def telemetry_mask_threshold():
   operation = request.form.get('operation', type=int)
   if operation == 1:
      gb.param.increase_mask_threshold()
   elif operation == -1:
      gb.param.decrease_mask_threshold()
   gb.enable_camera = True
   gb.enable_intruder = False
   gb.enable_kernel = False
   gb.enable_surface = False
   gb.enable_mask = True
   data = '"mask_threshold":{}'.format(gb.param.mask_threshold)
   data = json.loads( '{' + data + '}' )
   cfg.saveTelemetryConfig("system")
   cfg.logger.info(request.remote_addr + ' : ' + str(data))
   return jsonify(data)

@app.route('/api/telemetry/duration', methods = ['POST'])
def telemetry_duration():
   duration = request.form.get('duration')
   data = set_telemetry_duration(duration)
   cfg.saveTelemetryConfig("system")
   cfg.logger.info(request.remote_addr + ' : ' + str(data))
   return jsonify(data)

@app.route('/api/camera', methods = ['GET', 'POST'])
def camera():
   if request.method == 'GET':
      data = get_camera()
      return jsonify(data) 
   if request.method == 'POST':
      gb.enable_kernel = False
      gb.enable_surface = False
      gb.enable_mask = False
      data = get_camera()
      cfg.logger.info(request.remote_addr + ' : ' + str(data))
      return jsonify(data) 

@app.route('/api/camera/state', methods = ['POST'])
def camera_state():
   state = request.form.get('state')
   data = set_camera_state(state)
   cfg.logger.info(request.remote_addr + ' : ' + str(data))
   return jsonify(data)   

@app.route('/api/camera/intruder', methods = ['POST'])
def camera_intruder():
   intruder = request.form.get('intruder')
   data = set_camera_intruder(intruder)
   cfg.logger.info(request.remote_addr + ' : ' + str(data))
   return jsonify(data) 


###################### EXPLORER #########################

@app.route('/api/images',methods=['POST'])
def images():
   ID = request.form.get('ID', type=int)
   path = gb.cfg.os.path.sep.join([gb.cfg.configDirectory, 'log_{}.json'.format(ID)])
   if gb.cfg.os.path.exists(path):
      log = Log(ID)
      encoded_images = []
      for image_path in log.path.images:
         encoded_images.append(get_response_image(image_path))
      return jsonify({'images': encoded_images, 'date': log.date, 'max': gb.recordID-1})
   else: 
      abort(404)

#########################################################


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5050, debug=False)