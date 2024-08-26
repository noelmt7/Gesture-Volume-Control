import cv2
import mediapipe as mp
import random
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Get frame dimensions
ret, frame = cap.read()
if ret:
    height, width, _ = frame.shape

# Full-screen window
cv2.namedWindow('Gesture Control Game', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Gesture Control Game', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Variables to hold player names and scores
player_1_name = ""
player_2_name = ""
player_1_score = 0
player_2_score = 0
current_player = 1

def reset_game():
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y, bar_x, bar_width, game_over, start_time
    ball_x = random.randint(50, width - 50)
    ball_y = 50
    ball_radius = 20
    ball_velocity_x = 5  # Slower initial speed
    ball_velocity_y = 5
    bar_width = 100
    bar_x = (width - bar_width) // 2
    game_over = False
    start_time = time.time()

reset_game()

def input_player_name(prompt):
    name = ""
    while True:
        frame_copy = frame.copy()
        cv2.putText(frame_copy, prompt, (width // 2 - 150, height // 2 - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame_copy, name + "|", (width // 2 - 150, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Gesture Control Game', frame_copy)
        key = cv2.waitKey(0)
        if key == 13:  # Enter key
            return name
        elif key == 8:  # Backspace key
            name = name[:-1]
        elif key != -1:
            name += chr(key)

# Ask for player names
player_1_name = input_player_name("Enter Player 1 Name:")
player_2_name = input_player_name("Enter Player 2 Name:")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    # Convert the BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the index fingertip coordinates (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            index_x, index_y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)

            # Move the bar based on the index finger position
            bar_x = max(0, min(index_x - bar_width // 2, width - bar_width))

            # Draw the square box on the hand
            box_size = 50
            cv2.rectangle(frame, (index_x - box_size // 2, index_y - box_size // 2),
                          (index_x + box_size // 2, index_y + box_size // 2), (0, 255, 255), 2)

            # Draw a line connecting the square to the bar
            cv2.line(frame, (index_x, index_y), (bar_x + bar_width // 2, height - 20), (0, 255, 255), 2)

    # Move the ball
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Check for collisions with the screen boundaries
    if ball_x - 20 <= 0 or ball_x + 20 >= width:
        ball_velocity_x = -ball_velocity_x

    if ball_y - 20 <= 0:
        ball_velocity_y = -ball_velocity_y

    # Check for collision with the bar
    if ball_y + 20 >= height - 30 and (ball_x >= bar_x and ball_x <= bar_x + bar_width):
        ball_velocity_y = -ball_velocity_y
        # Gradually increase ball speed slowly
        ball_velocity_y += int(ball_velocity_y * 0.30)
        ball_velocity_x += int(ball_velocity_x * 0.30)

    elif ball_y + 20 >= height:
        game_over = True

    # Draw the ball
    if not game_over:
        cv2.circle(frame, (ball_x, ball_y), 20, (0, 0, 255), -1)
        # Draw the bar
        cv2.rectangle(frame, (bar_x, height - 30), (bar_x + bar_width, height - 10), (0, 255, 0), -1)
        # Display scores
        cv2.putText(frame, f"{player_1_name}: {player_1_score}", (width - 250, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"{player_2_name}: {player_2_score}", (width - 250, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        # Calculate score based on how long the player lasted
        elapsed_time = int(time.time() - start_time)
        if current_player == 1:
            player_1_score = elapsed_time
            current_player = 2
            reset_game()
            cv2.putText(frame, f"{player_2_name}'s Turn", (width // 2 - 150, height // 2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.imshow('Gesture Control Game', frame)
            cv2.waitKey(2000)  # Wait for 2 seconds before Player 2's turn
        else:
            player_2_score = elapsed_time
            winner = player_1_name if player_1_score > player_2_score else player_2_name
            cv2.putText(frame, f"Winner: {winner}", (width // 2 - 150, height // 2 - 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.putText(frame, "Press 'R' to Restart", (width // 2 - 150, height // 2 + 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Gesture Control Game', frame)
            key = cv2.waitKey(0)
            if key == ord('r'):  # Press 'R' to restart
                player_1_score = 0
                player_2_score = 0
                current_player = 1
                reset_game()

    cv2.imshow('Gesture Control Game', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()







