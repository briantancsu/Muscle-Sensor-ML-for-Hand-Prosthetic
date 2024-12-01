import tkinter as tk
from typing import Collection
import pyfirmata
import time
import pandas as pd

board = pyfirmata.Arduino('/dev/cu.usbmodem101')
it = pyfirmata.util.Iterator(board)
it.start()

analog_pin = board.get_pin('a:0:i')

root = tk.Tk()
root.title("Calibration")
root.configure(bg="black") 

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

center_window(root, 500, 400)
global do_col, label, labels, reads
do_col = False
label = 1
labels = []
reads = []
def start_collection():
    global do_col, label, labels, reads
    if do_col == True:
        analog_value = analog_pin.read()/1.203*5
        print(analog_value, label)
        labels.append(label)
        reads.append(analog_value)
        root.after(10, start_collection)

def stop_col():
    global do_col
    do_col = False

def change_label(l):
    global label
    label = l

def save_data():
    df = pd.DataFrame({"Value": reads, "Label": labels})
    df.to_csv('data.csv', index=False)
    print("done")

def start_cal():
    global do_col, labels, reads
    print("start")
    start_button.destroy()
    inst_text.pack(expand=True)
    do_col = True
    root.after(10, start_collection())
    root.after(2000, lambda : inst_text.configure(text="Release", fg="green"))
    root.after(2000, lambda : change_label(0))
    root.after(4000, lambda : inst_text.configure(text="Flex", fg="red"))
    root.after(4000, lambda : change_label(1))
    root.after(6000, lambda : inst_text.configure(text="Release", fg="green"))
    root.after(6000, lambda : change_label(0))
    root.after(8000, lambda : inst_text.configure(text="Flex", fg="red"))
    root.after(8000, lambda : change_label(1))
    root.after(10000, lambda : inst_text.configure(text="Release", fg="green"))
    root.after(10000, lambda : change_label(0))
    root.after(11000, stop_col)
    root.after(11000, lambda : inst_text.configure(text="Done" ,fg="white"))
    root.after(11000, save_data)
    root.after(12500, lambda : root.destroy())
    
    


start_button = tk.Button(root, text="Start", command=start_cal)
start_button.pack(expand=True)  

inst_text = tk.Label(root, text="Flex", font=("Arial", 48), bg="black", fg="red")

root.mainloop()
