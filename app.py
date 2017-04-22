#!/usr/bin/env python
import os
import sys
import signal
import threading
import time
import json
from flask import Flask, request, Response
from gevent.wsgi import WSGIServer

import config as cfg

import camera_pi as cam
#import camera_cv as cam

app = Flask(__name__, static_url_path='/static')

# Handler for a clean shutdown when pressing Ctrl-C
def signal_handler(signal, frame):
    http_server.close()
    sys.exit(0)

# Base URL / - loads web interface
@app.route('/')
def index():
    cfg.video_fps = 0
    video = request.args.get('video')
    if video == 'n':
        cfg.video_status = False
    else:
        if video == None:
            cfg.video_status = cfg.camera_detected
        elif float(video) > 0:
            cfg.video_fps = float(video)
            cfg.video_status = cfg.camera_detected
    return app.send_static_file('index.html')

def gen(camera):
    """Video streaming generator function."""
    if cfg.video_status:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# URL for heartbeat requests (resets watchdog timer)
# Returns JSON object with status data
@app.route('/heartbeat')
def heartbeat():
    cfg.watchdog = 0
    output = {}
    output['f'] = cfg.video_fps
    output['v'] = cfg.video_status
    return json.dumps(output)


# URL for video stream feed
@app.route('/video_feed')
def video_feed():
    if cfg.camera_detected:
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(gen(cam.Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return 'no video'

# URL for single frame feed
@app.route('/single_frame.jpg')
def single_frame():
    if cfg.camera_detected:
        jpeg =  cam.single_frame()
        return Response(jpeg, mimetype='image/jpeg; boundary=frame')
    else:
        return 'no video'

if __name__ == '__main__':
    cfg.camera_detected, cfg.camera = cam.init_camera()

    # register signal handler for a clean exit
    signal.signal(signal.SIGINT, signal_handler)

    #app.run(host='0.0.0.0', debug=False, threaded=True)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
