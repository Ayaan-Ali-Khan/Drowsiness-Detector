# Import Libraries
import tkinter as tk
import customtkinter as ctk
import torch
import numpy as np
import cv2
from PIL import Image, ImageTk
import vlc
import random

# Build the app
app = tk.Tk()
app.geometry("600x600")
app.title("Drowsiness Detector App")
ctk.set_appearance_mode("dark")

# Video frame setup
vidFrame = tk.Frame(height=480, width=600)
vidFrame.pack()
vid = ctk.CTkLabel(vidFrame)
vid.pack()

counter = 0
counterLabel = ctk.CTkLabel(vidFrame, text=counter, height=40, width=120, font=("Arial", 20), text_color='white', fg_color='teal')
counterLabel.pack(pady=10)

# Button
def reset_counter():
    global counter
    counter = 0
reset_Button = ctk.CTkButton(vidFrame, text="Reset Counter", command=reset_counter, height=40, width=120, font=("Arial", 20), text_color='white', fg_color='teal')
reset_Button.pack()

# Get the model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp9/weights/last.pt', force_reload=True)
capture = cv2.VideoCapture(0)

def detect():
    global counter
    ret, frame = capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results =  model(frame)
    img = np.squeeze(results.render())

    if len(results.xywh[0]) > 0:
        dconf = results.xywh[0][0][4]
        dclass = results.xywh[0][0][5]
        if dconf.item() > 0.55 and dclass.item() == 1.0:
            filechoice = random.choice([1,2,3])
            p = vlc.MediaPlayer(f'file:///{filechoice}.wav')
            p.play()
            counter += 1

    imgarr = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(imgarr)
    vid.imgtk = imgtk
    vid.configure(image=imgtk)
    vid.after(10, detect)
    counterLabel.configure(text=counter)

detect()
app.mainloop()