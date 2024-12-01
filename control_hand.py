from pyfirmata import Arduino, util
import time
import numpy as np
import pickle

board = Arduino('/dev/cu.usbmodem101')

it = util.Iterator(board)
it.start()

def close_hand():
    for i in range(5):
        if i == 2:
            servo_pins[i].write(180)
        else:
            servo_pins[i].write(0)

def open_hand():
    for i in range(5):
        if i == 2:
            servo_pins[i].write(0)
        else:
            servo_pins[i].write(180)

servo_pins = []
for i in [4, 10, 6, 7, 8]:
    name = 'd:' + str(i) + ":s"
    servo_pins.append(board.get_pin(name))

analog_pin = board.get_pin('a:0:i')

with open('svm_model.pkl', 'rb') as model_file:
   loaded_svm = pickle.load(model_file)
while True:
    
    analog_value = analog_pin.read()/1.203*5
    if loaded_svm.predict(np.array(analog_value).reshape(-1, 1))[0] == 1    :
        close_hand()
    else:
        open_hand()
    time.sleep(0.1)