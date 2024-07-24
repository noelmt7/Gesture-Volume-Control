import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from VolumeHandControl import HandVolumeControl  # Adjust the import as per your file structure

class HandVolumeControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Volume Control")
        self.root.geometry("800x600")

        self.hand_volume_control = HandVolumeControl()

        self.canvas = tk.Canvas(self.root, width=self.hand_volume_control.wCam, height=self.hand_volume_control.hCam)
        self.canvas.pack()

        self.update()

    def update(self):
        img = self.hand_volume_control.process_frame()
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        self.root.after(10, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = HandVolumeControlApp(root)
    root.mainloop()
