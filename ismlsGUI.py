import customtkinter as ctk
import subprocess
import threading

# Paths to your existing Python scripts
video_control_script = 'videocontrol.py'
audio_control_script = 'VolumeHandControl.py'
mouse_tracking_script = 'mouse.py'
media_control_script = 'mediacontrol.py'

# Placeholder functions for subprocesses
video_thread = None
audio_thread = None
mouse_thread = None
media_thread = None

# Function to run a script in a new thread
def run_script(script_path, global_var):
    global_var["process"] = subprocess.Popen(['python', script_path])
    global_var["running"] = True
    global_var["process"].wait()
    global_var["running"] = False

# Function to start a new thread for a script
def start_script(global_var, script_path):
    if not global_var["running"]:
        global_var["thread"] = threading.Thread(target=run_script, args=(script_path, global_var))
        global_var["thread"].start()
        print(f"{script_path} started")

# Function to stop a running script
def stop_script(global_var):
    if global_var["running"]:
        global_var["process"].terminate()
        global_var["thread"].join()
        global_var["running"] = False
        print(f"{global_var['process'].args[1]} stopped")

# Define control state for each feature
video_control = {"thread": None, "process": None, "running": False}
audio_control = {"thread": None, "process": None, "running": False}
mouse_tracking = {"thread": None, "process": None, "running": False}
media_control = {"thread": None, "process": None, "running": False}

def toggle_features():
    # Stop individual scripts if both video and audio are on
    if var_video.get() and var_audio.get():
        stop_script(video_control)
        stop_script(audio_control)
        start_script(media_control, media_control_script)
    else:
        stop_script(media_control)
        if var_video.get():
            start_script(video_control, video_control_script)
        else:
            stop_script(video_control)

        if var_audio.get():
            start_script(audio_control, audio_control_script)
        else:
            stop_script(audio_control)
    
    if var_mouse_tracking.get():
        start_script(mouse_tracking, mouse_tracking_script)
    else:
        stop_script(mouse_tracking)

def enable_all_features():
    var_video.set(1)
    var_audio.set(1)
    var_mouse_tracking.set(1)
    toggle_features()

def end_program():
    stop_script(video_control)
    stop_script(audio_control)
    stop_script(mouse_tracking)
    stop_script(media_control)
    root.destroy()

# Initialize customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
root = ctk.CTk()
root.title("Gesture Control GUI")
root.geometry("400x300")  # Set window size

# Configure grid to center align the widgets
root.grid_columnconfigure(0, weight=1)
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

# Create variables to store the state of each feature
var_video = ctk.IntVar()
var_audio = ctk.IntVar()
var_mouse_tracking = ctk.IntVar()

# Font configuration
font_config = ('Comic Sans', 14)

# Create checkboxes for each feature
chk_video = ctk.CTkCheckBox(root, text="Control Video", variable=var_video, font=font_config)
chk_video.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)

chk_audio = ctk.CTkCheckBox(root, text="Control Audio", variable=var_audio, font=font_config)
chk_audio.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

chk_mouse_tracking = ctk.CTkCheckBox(root, text="Mouse Tracking", variable=var_mouse_tracking, font=font_config)
chk_mouse_tracking.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)

# Create a button to toggle the selected features
btn_toggle = ctk.CTkButton(root, text="Start", command=toggle_features, font=font_config)
btn_toggle.grid(row=3, column=0, pady=10, padx=20, sticky='nsew')

# Create a button to enable all features at once
btn_enable_all = ctk.CTkButton(root, text="Enable All Features", command=enable_all_features, font=font_config)
btn_enable_all.grid(row=4, column=0, pady=10, padx=20, sticky='nsew')

# Create a button to end the program
btn_end = ctk.CTkButton(root, text="End", command=end_program, font=font_config)
btn_end.grid(row=5, column=0, pady=10, padx=20, sticky='nsew')

root.mainloop()
