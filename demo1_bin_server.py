from threading import Thread
import move
from matplotlib import pyplot as plt
from web_client import WebClient
from camera import Camera
from flask import Flask

client = WebClient('http://localhost:5000')
camera_top = Camera('1.1.3') # when installing make sure the usb port ids match
camera_side = Camera('1.2')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def run():
    template = open('demo1.html').read()
    image_top = camera_top.capture()
    image_side = camera_side.capture()
    plt.imsave('top.png', image_top)
    plt.imsave('side.png', image_side)
    pred_label = client.classify(image_top=image_top, image_side=image_side)
    if pred_label == 'recyclable':
        move_thread = Thread(target=move.bin0)
    else:
        move_thread = Thread(target=move.bin1)
    # start moving in a separate thread so the webpage is returned immediately
    move_thread.start()
    return template.replace('{pred_label}', pred_label)

@app.route('/file/<filename>', methods=['GET'])
def file(filename):
    return open(filename, 'rb').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
