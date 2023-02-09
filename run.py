from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
import PyATEMMax
from threading import Thread
from time import sleep
import random
app = Flask(__name__)

# Create a new ATEM object
atem = PyATEMMax.ATEMMaxx()

# Connect to the ATEM
atem.connect('192.168.1.80')
atem.waitForConnection()

cameras = {'1':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False,'8':False}
solo = 0
waittime = 8

def atemloop():
    while True:
        if not solo:
            activecameras = []
            for i in range(1,9):
                if cameras[str(i)]:
                    activecameras.append(i)
            if len(activecameras) == 1:
                camera = random.choice(activecameras)
                atem.setProgramInputVideoSource(0, camera)
            sleep(waittime + (random.random() - 0.5) * waittime)
                
                

@app.route('/')
def hello_world():
    return render_template('index.html', cameras=cameras, solo=solo, waittime=waittime)

@app.route('/dosomething', methods=['POST'])
def dosomething():
    global cameras, solo, waittime
    todo = request.form['todo']
    if todo == 'time':
        waittime = int(request.form['time'])
    elif todo == 'solo':
        solo = int(request.form['solo'])
    elif todo == 'camera':
        camera = request.form['camera']
        if request.form['enable'] == 'true':
            cameras[camera] = True
        else:
            cameras[camera] = False
    return 'ok'
        

if __name__ == '__main__':
    atemthread = Thread(target=atemloop)
    atemthread.start()
    app.run(debug=True, host='', port=5000) 