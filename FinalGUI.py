import customtkinter as ctk
import subprocess
import os
from PIL import Image

# Paths to your existing Python scripts
video_control_script = 'videocontrol.py'
audio_control_script = 'VolumeHandControl.py'
mouse_tracking_script = 'mouse.py'

# Placeholder functions for subprocesses
video_process = None
audio_process = None
mouse_process = None

def start_video_control():
    global video_process
    if video_process is None:
        video_process = subprocess.Popen(['python', video_control_script])
        print("Video control started")

def stop_video_control():
    global video_process
    if video_process is not None:
        video_process.terminate()
        video_process = None
        print("Video control stopped")

def start_audio_control():
    global audio_process
    if audio_process is None:
        audio_process = subprocess.Popen(['python', audio_control_script])
        print("Audio control started")

def stop_audio_control():
    global audio_process
    if audio_process is not None:
        audio_process.terminate()
        audio_process = None
        print("Audio control stopped")

def start_mouse_tracking():
    global mouse_process
    if mouse_process is None:
        mouse_process = subprocess.Popen(['python', mouse_tracking_script])
        print("Mouse tracking started")

def stop_mouse_tracking():
    global mouse_process
    if mouse_process is not None:
        mouse_process.terminate()
        mouse_process = None
        print("Mouse tracking stopped")

def toggle_features():
    if var_video.get():
        start_video_control()
    else:
        stop_video_control()
    
    if var_audio.get():
        start_audio_control()
    else:
        stop_audio_control()
    
    if var_mouse_tracking.get():
        start_mouse_tracking()
    else:
        stop_mouse_tracking()

def enable_all_features():
    var_video.set(1)
    var_audio.set(1)
    var_mouse_tracking.set(1)
    toggle_features()

def end_program():
    stop_video_control()
    stop_audio_control()
    stop_mouse_tracking()
    root.destroy()

# Initialize customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# Create the main window
root = ctk.CTk()
root.title("Gesture Control GUI")
root.geometry("400x600")  # Adjusted window size to accommodate the image and buttons

# Configure grid to center align the widgets
root.grid_columnconfigure(0, weight=1)
for i in range(8):
    root.grid_rowconfigure(i, weight=1)


image_path = "Gesture Volume Control/1.png"

main_image = ctk.CTkImage(Image.open(image_path), size=(200, 200))  # Adjust size as needed

image_label = ctk.CTkLabel(root, image=main_image, text="")
image_label.grid(row=1, column=0, pady=10, padx=20, sticky='nsew')

# Create variables to store the state of each feature
var_video = ctk.IntVar()
var_audio = ctk.IntVar()
var_mouse_tracking = ctk.IntVar()

# Font configuration
font_config = ('  Sans', 14)

# Create checkboxes for each feature
chk_video = ctk.CTkCheckBox(root, text="Control Video", variable=var_video, font=font_config)
chk_video.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)

chk_audio = ctk.CTkCheckBox(root, text="Control Audio", variable=var_audio, font=font_config)
chk_audio.grid(row=3, column=0, sticky='nsew', padx=20, pady=10)

chk_mouse_tracking = ctk.CTkCheckBox(root, text="Mouse Tracking", variable=var_mouse_tracking, font=font_config)
chk_mouse_tracking.grid(row=4, column=0, sticky='nsew', padx=20, pady=10)

# Create a button to toggle the selected features
btn_toggle = ctk.CTkButton(root, text="Start", command=toggle_features, font=font_config)
btn_toggle.grid(row=5, column=0, pady=10, padx=20, sticky='nsew')

# Create a button to enable all features at on
btn_enable_all = ctk.CTkButton(root, text="Enable All Features", command=enable_all_features, font=font_config)
btn_enable_all.grid(row=6, column=0, pady=10, padx=20, sticky='nsew')

# Create a button to end the program
btn_end = ctk.CTkButton(root, text="End", command=end_program, font=font_config)
btn_end.grid(row=7, column=0, pady=10, padx=20, sticky='nsew')

root.mainloop()
