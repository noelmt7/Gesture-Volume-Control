import customtkinter as ctk
import tkinter as tk
import cv2
import mediapipe as mp
import json
import os
import numpy as np
from pynput import keyboard
from pynput.keyboard import Controller
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import time

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize the keyboard controller
keyboard_controller = Controller()

# File to store gesture-to-key mappings
MAPPINGS_FILE = 'gesture_key_mappings.json'

# Directory to save gesture images
IMAGES_DIR = 'gesture_images'

# Create the directory if it doesn't exist
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Dictionary to store gesture-to-key mappings
gesture_key_map = {}

# Define a recognition threshold
RECOGNITION_THRESHOLD = 0.5

# Time to wait before triggering the same key again (in seconds)
COOLDOWN_TIME = 1.0

captured_landmarks = None
capture_done = False
last_triggered_time = {}

def load_mappings():
    """Load gesture-to-key mappings from a JSON file."""
    global gesture_key_map
    if os.path.exists(MAPPINGS_FILE):
        with open(MAPPINGS_FILE, 'r') as f:
            gesture_key_map = json.load(f)
            # Convert landmarks from lists to tuples
            for key, landmarks in gesture_key_map.items():
                gesture_key_map[key] = [tuple(lm) for lm in landmarks]
            print("Mappings loaded successfully.")
    else:
        print("No mappings file found. Starting fresh.")

def save_mappings():
    """Save gesture-to-key mappings to a JSON file."""
    with open(MAPPINGS_FILE, 'w') as f:
        # Convert landmarks from tuples to lists for JSON serialization
        json.dump({key: [list(lm) for lm in landmarks] for key, landmarks in gesture_key_map.items()}, f)
        print("Mappings saved successfully.")
    update_gesture_listbox()

def record_gesture(hand_landmarks):
    """Records the landmark positions of a hand gesture."""
    landmarks = []
    for landmark in hand_landmarks.landmark:
        landmarks.append((landmark.x, landmark.y, landmark.z))
    return landmarks

def compare_gestures(landmarks1, landmarks2):
    """Compares two sets of landmarks and returns a similarity score."""
    lm1 = np.array(landmarks1).flatten()
    lm2 = np.array(landmarks2).flatten()
    distance = np.linalg.norm(lm1.astype(np.float64) - lm2.astype(np.float64))
    return distance

def detect_gesture(hand_landmarks):
    """Detect and recognize gestures based on hand landmarks."""
    current_landmarks = record_gesture(hand_landmarks)
    
    min_distance = float('inf')
    detected_gesture = None
    
    for gesture, stored_landmarks in gesture_key_map.items():
        for stored_landmark_set in stored_landmarks:
            distance = compare_gestures(current_landmarks, stored_landmark_set)
            if distance < min_distance:
                min_distance = distance
                detected_gesture = gesture
    
    # Return detected gesture only if it is within the recognition threshold
    if min_distance > RECOGNITION_THRESHOLD:
        detected_gesture = None

    return detected_gesture

def on_press(key):
    """Callback function to handle key presses."""
    global captured_landmarks, capture_done
    if key == keyboard.Key.space:
        print("Gesture captured.")
        capture_done = True

def map_gesture_to_key():
    """Capture a gesture and map it to a key."""
    global captured_landmarks, capture_done
    captured_landmarks = None
    capture_done = False

    cap = cv2.VideoCapture(0)
    
    # Set up the key listener
    with keyboard.Listener(on_press=on_press) as listener:
        while not capture_done:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    captured_landmarks = record_gesture(hand_landmarks)

            cv2.imshow("Capture Gesture", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
                print("Gesture mapping cancelled.")
                capture_done = True

    cap.release()
    cv2.destroyAllWindows()

    return captured_landmarks, frame if captured_landmarks else (None, None)

def trigger_key(gesture):
    """Simulate a key press based on the detected gesture."""
    current_time = time.time()
    if gesture:
        if gesture not in last_triggered_time or (current_time - last_triggered_time[gesture] >= COOLDOWN_TIME):
            try:
                keyboard_controller.press(gesture)
                keyboard_controller.release(gesture)
                print(f"Triggered key '{gesture}'")
                last_triggered_time[gesture] = current_time
            except Exception as e:
                print(f"Error triggering key: {e}")

def capture_and_detect():
    """Capture video and detect gestures."""
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                gesture = detect_gesture(hand_landmarks)
                if gesture:  # Only trigger action if a valid gesture is detected
                    trigger_key(gesture)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        cv2.imshow("Gesture Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
            break
    
    cap.release()
    cv2.destroyAllWindows()

def map_new_gesture():
    """Maps a new gesture to a key."""
    captured_landmarks, frame = map_gesture_to_key()
    if captured_landmarks:
        key = key_entry.get().strip().lower()
        if key in gesture_key_map:
            gesture_key_map[key].append(captured_landmarks)
        else:
            gesture_key_map[key] = [captured_landmarks]
        save_mappings()

        # Save the captured frame as an image with the key as the filename
        image_path = os.path.join(IMAGES_DIR, f"{key}.png")
        cv2.imwrite(image_path, frame)

        # Add the image and key to the listbox
        update_gesture_listbox()

        key_entry.pack_forget()  # Hide key entry after mapping
        start_mapping_button.pack_forget()  # Hide the start mapping button after mapping
        print(f"Gesture '{key}' mapped successfully and image saved.")

def update_gesture_listbox():
    """Updates the canvas with the current gestures and their images."""
    canvas.delete("all")  # Clear the canvas
    y_position = 10  # Initial vertical position

    if not gesture_key_map:
        canvas.create_text(150, y_position, text="No mapped gestures", font=("Arial", 16))
    else:
        for key in gesture_key_map.keys():
            # Load the image
            image_path = os.path.join(IMAGES_DIR, f"{key}.png")
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((200, 200))  # Resize image
                img = ImageTk.PhotoImage(img)
                canvas.create_image(10, y_position, anchor=tk.NW, image=img)
                canvas.create_text(220, y_position + 100, text=f" {key}", font=("Arial", 16), anchor=tk.NW)
                # Store reference to avoid garbage collection
                canvas.image = img
                y_position += 220  # Move to the next row

def show_key_entry():
    """Shows the key entry field when mapping a new gesture."""
    key_label.pack(pady=5)
    key_entry.pack(pady=5)
    start_mapping_button.pack(pady=10)

def confirm_gesture():
    """Confirms and starts the mapping process."""
    # Show a confirmation dialog before starting the mapping
    response = messagebox.askyesno("Start Mapping", "Do you want to start mapping this gesture?")
    if response:
        map_new_gesture()

def delete_gesture():
    """Deletes a gesture from the mapping."""
    key = simpledialog.askstring("Delete Gesture", "Enter key of the gesture to delete:")
    if key:
        if key in gesture_key_map:
            del gesture_key_map[key]
            image_path = os.path.join(IMAGES_DIR, f"{key}.png")
            if os.path.exists(image_path):
                os.remove(image_path)
            save_mappings()
            update_gesture_listbox()
            messagebox.showinfo("Success", f"Gesture '{key}' deleted successfully.")
        else:
            messagebox.showerror("Error", f"No gesture found for key '{key}'.")

def start_detecting():
    """Starts the gesture detection process."""
    capture_and_detect()

def combobox_callback(choice):
    """Handles actions based on the combobox selection."""
    if choice == "Map New Gesture":
        show_key_entry()
    elif choice == "Delete Gesture":
        delete_gesture()
    elif choice == "Start Detecting":
        start_detecting()

# Setup the UI
root = ctk.CTk()
root.title("Gesture Mapping Tool")

# Combobox for selecting actions
combobox = ctk.CTkComboBox(root, values=["Map New Gesture", "Delete Gesture", "Start Detecting"], command=combobox_callback)
combobox.pack(pady=10)

# Widgets for mapping a new gesture
key_label = ctk.CTkLabel(root, text="Enter key to map gesture:")
key_entry = ctk.CTkEntry(root)
start_mapping_button = ctk.CTkButton(root, text="Start Mapping", command=confirm_gesture)

# Canvas to display mapped gestures
canvas = tk.Canvas(root, width=400, height=600)
canvas.pack(pady=10)

# Load existing mappings and update the listbox
load_mappings()
update_gesture_listbox()

root.mainloop()


