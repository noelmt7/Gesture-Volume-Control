import customtkinter as ctk
import subprocess
import os
from PIL import Image

# Paths to your existing Python scripts
video_control_script = 'videocontrol.py'
audio_control_script = 'VolumeHandControl.py'
mouse_tracking_script = 'mouse.py'
rock_paper_scissors_script = 'rock_paper_scissors.py'
gesture_mapping_script = 'gesture_mapping.py'
media_control_script = 'mediacontrol.py'
bouncing_ball_script = 'pythongame.py'

# Placeholder functions for subprocesses
video_process = None
audio_process = None
media_process = None
mouse_process = None
bouncing_ball_process = None
rps_process = None
gesture_mapping_process = None

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

def start_media_control():
    global media_process
    if media_process is None:
        media_process = subprocess.Popen(['python', media_control_script])
        print("Media control started")

def stop_media_control():
    global media_process
    if media_process is not None:
        media_process.terminate()
        media_process = None
        print("Media control stopped")

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

def start_bouncing_ball():
    global bouncing_ball_process
    if bouncing_ball_process is None:
        bouncing_ball_process = subprocess.Popen(['python', bouncing_ball_script])
        print("Bouncing ball started")

def stop_bouncing_ball():
    global bouncing_ball_process
    if bouncing_ball_process is not None:
        bouncing_ball_process.terminate()
        bouncing_ball_process = None
        print("Bouncing ball stopped")

def start_rock_paper_scissors():
    global rps_process
    if rps_process is None:
        rps_process = subprocess.Popen(['python', rock_paper_scissors_script])
        print("Rock Paper Scissors started")

def stop_rock_paper_scissors():
    global rps_process
    if rps_process is not None:
        rps_process.terminate()
        rps_process = None  
        print("Rock Paper Scissors stopped")

def start_gesture_mapping():
    global gesture_mapping_process
    if gesture_mapping_process is None:
        gesture_mapping_process = subprocess.Popen(['python', gesture_mapping_script])
        print("Gesture Mapping application started")

def stop_gesture_mapping():
    global gesture_mapping_process
    if gesture_mapping_process is not None:
        gesture_mapping_process.terminate()
        gesture_mapping_process = None
        print("Gesture Mapping application stopped")

def toggle_features():
    if var_video.get():
        start_video_control()
    else:
        stop_video_control()
    
    if var_audio.get():
        start_audio_control()
    else:
        stop_audio_control()

    if var_media.get():
        start_media_control()
    else:
        stop_media_control()

    if var_mouse_tracking.get():
        start_mouse_tracking()
    else:
        stop_mouse_tracking()

    if var_bouncing_ball.get():
        start_bouncing_ball()
    else:
        stop_bouncing_ball()
    
    if var_rps.get():
        start_rock_paper_scissors()
    else:
        stop_rock_paper_scissors()

def enable_all_features():
    var_video.set(1)
    var_audio.set(1)
    var_media.set(1)
    var_mouse_tracking.set(1)
    var_bouncing_ball.set(1)
    var_rps.set(1)
    toggle_features()

def end_program():
    stop_video_control()
    stop_audio_control()
    stop_media_control()
    stop_mouse_tracking()
    stop_bouncing_ball()
    stop_rock_paper_scissors()
    stop_gesture_mapping()  # Ensure gesture mapping is stopped
    root.destroy()

# Initialize customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# Create the main window
root = ctk.CTk()
root.title("Gesture Control GUI")
root.state('zoomed')  # Open in full screen
root.geometry("400x600")  # Adjusted window size to accommodate the image and buttons

# Configure grid to center align the widgets
root.grid_columnconfigure(0, weight=1)
for i in range(10):
    root.grid_rowconfigure(i, weight=1)

image_path = "1.png"

main_image = ctk.CTkImage(Image.open(image_path), size=(200, 200))  # Adjust size as needed

image_label = ctk.CTkLabel(root, image=main_image, text="")
image_label.grid(row=1, column=0, pady=10, padx=20, sticky='nsew')

# Create variables to store the state of each feature
var_video = ctk.IntVar()
var_audio = ctk.IntVar()
var_media = ctk.IntVar()
var_mouse_tracking = ctk.IntVar()
var_bouncing_ball = ctk.IntVar()
var_rps = ctk.IntVar()

# Font configuration
font_config = ('Sans', 14)

# Create checkboxes for each feature
chk_video = ctk.CTkCheckBox(root, text="Control Video", variable=var_video, font=font_config)
chk_video.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)

chk_audio = ctk.CTkCheckBox(root, text="Control Audio", variable=var_audio, font=font_config)
chk_audio.grid(row=3, column=0, sticky='nsew', padx=20, pady=10)

chk_media = ctk.CTkCheckBox(root, text="Control Media", variable=var_media, font=font_config)
chk_media.grid(row=4, column=0, sticky='nsew', padx=20, pady=10)

chk_mouse_tracking = ctk.CTkCheckBox(root, text="Mouse Tracking", variable=var_mouse_tracking, font=font_config)
chk_mouse_tracking.grid(row=5, column=0, sticky='nsew', padx=20, pady=10)

chk_bouncing_ball = ctk.CTkCheckBox(root, text="Bouncing Ball", variable=var_bouncing_ball, font=font_config)
chk_bouncing_ball.grid(row=6, column=0, sticky='nsew', padx=20, pady=10)

chk_rps = ctk.CTkCheckBox(root, text="Rock Paper Scissors", variable=var_rps, font=font_config)
chk_rps.grid(row=7, column=0, sticky='nsew', padx=20, pady=10)

# Create a button to toggle the selected features
btn_toggle = ctk.CTkButton(root, text="Start", command=toggle_features, font=font_config)
btn_toggle.grid(row=8, column=0, pady=10, padx=20, sticky='nsew')




# Create a button to start the Gesture Mapping application
btn_gesture_mapping = ctk.CTkButton(root, text="Open Gesture Mapping", command=start_gesture_mapping, font=font_config)
btn_gesture_mapping.grid(row=10, column=0, pady=10, padx=20, sticky='nsew')

# Create a button to end the program
btn_end = ctk.CTkButton(root, text="End", command=end_program, font=font_config)
btn_end.grid(row=11, column=0, pady=10, padx=20, sticky='nsew')

root.mainloop()
