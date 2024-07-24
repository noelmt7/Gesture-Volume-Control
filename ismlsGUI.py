import tkinter as tk
import subprocess
import os

# Paths to your existing Python scripts
video_control_script = 'videocontrol.py'
audio_control_script = 'path/to/your/audio_control_script.py'
mouse_tracking_script = 'D:\Christ\Sem 4\SP\Gesture-Volume-Control\mouse.py'

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

# Create the main window
root = tk.Tk()
root.title("Gesture Control GUI")

# Create variables to store the state of each feature
var_video = tk.IntVar()
var_audio = tk.IntVar()
var_mouse_tracking = tk.IntVar()

# Create checkboxes for each feature
chk_video = tk.Checkbutton(root, text="Control Video", variable=var_video)
chk_video.grid(row=0, column=0, sticky='w')

chk_audio = tk.Checkbutton(root, text="Control Audio", variable=var_audio)
chk_audio.grid(row=1, column=0, sticky='w')

chk_mouse_tracking = tk.Checkbutton(root, text="Mouse Tracking", variable=var_mouse_tracking)
chk_mouse_tracking.grid(row=2, column=0, sticky='w')

# Create a button to toggle the selected features
btn_toggle = tk.Button(root, text="Toggle Features", command=toggle_features)
btn_toggle.grid(row=3, column=0, pady=10)

# Create a button to enable all features at once
btn_enable_all = tk.Button(root, text="Enable All Features", command=enable_all_features)
btn_enable_all.grid(row=4, column=0, pady=10)

# Start the main event loop
root.mainloop()

