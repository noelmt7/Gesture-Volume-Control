import cv2
import random
from collections import deque
import statistics as st
from HandTrackingModule import handDetector

def calculate_winner(cpu_choice, player_choice):
    if player_choice == "Invalid":
        return "Invalid!"
    if player_choice == cpu_choice:
        return "Tie!"
    if player_choice == "Rock" and cpu_choice == "Scissors":
        return "You win!"
    if player_choice == "Rock" and cpu_choice == "Paper":
        return "CPU wins!"
    if player_choice == "Scissors" and cpu_choice == "Rock":
        return "CPU wins!"
    if player_choice == "Scissors" and cpu_choice == "Paper":
        return "You win!"
    if player_choice == "Paper" and cpu_choice == "Rock":
        return "You win!"
    if player_choice == "Paper" and cpu_choice == "Scissors":
        return "CPU wins!"

def compute_fingers(hand_landmarks, count):
    if hand_landmarks[8][2] < hand_landmarks[6][2]:  # Index Finger
        count += 1
    if hand_landmarks[12][2] < hand_landmarks[10][2]:  # Middle Finger
        count += 1
    if hand_landmarks[16][2] < hand_landmarks[14][2]:  # Ring Finger
        count += 1
    if hand_landmarks[20][2] < hand_landmarks[18][2]:  # Pinky Finger
        count += 1
    if hand_landmarks[4][1] > hand_landmarks[3][1]:  # Thumb
        count += 1
    return count

webcam = cv2.VideoCapture(0)

cpu_choices = ["Rock", "Paper", "Scissors"]
cpu_choice = "Nothing"
cpu_score, player_score = 0, 0
winner_colour = (0, 255, 0)
player_choice = "Nothing"
hand_valid = False
display_values = ["Rock", "Invalid", "Scissors", "Invalid", "Invalid", "Paper"]
winner = "None"
de = deque(['Nothing'] * 5, maxlen=5)

detector = handDetector()

while webcam.isOpened():
    success, image = webcam.read()
    if not success:
        print("Camera isn't working")
        continue

    image = cv2.flip(image, 1)
    image = detector.findHands(image)
    hand_landmarks_list = detector.findPosition(image)

    handNumber = 0
    isCounting = False
    count = 0

    if hand_landmarks_list:
        isCounting = True
        hand_landmarks = hand_landmarks_list

        if player_choice != "Nothing" and not hand_valid:
            hand_valid = True
            cpu_choice = random.choice(cpu_choices)
            winner = calculate_winner(cpu_choice, player_choice)

            if winner == "You win!":
                player_score += 1
                winner_colour = (255, 0, 0)
            elif winner == "CPU wins!":
                cpu_score += 1
                winner_colour = (0, 0, 255)
            elif winner == "Invalid!" or winner == "Tie!":
                winner_colour = (0, 255, 0)

        count = compute_fingers(hand_landmarks, count)
    else:
        hand_valid = False

    if isCounting and count <= 5:
        player_choice = display_values[count]
    elif isCounting:
        player_choice = "Invalid"
    else:
        player_choice = "Nothing"

    de.appendleft(player_choice)

    try:
        player_choice = st.mode(de)
    except st.StatisticsError:
        continue

    # Adjust text size and positioning
    font_scale = .5
    thickness = 1

    # cv2.putText(image, "You", (20, 40), cv2.FONT_HERSHEY_DUPLEX, font_scale, (255, 0, 0), thickness)
    # cv2.putText(image, "CPU", (380, 40), cv2.FONT_HERSHEY_DUPLEX, font_scale, (0, 0, 255), thickness)
    cv2.putText(image, "Your move: " + player_choice, (20, 80), cv2.FONT_HERSHEY_DUPLEX, font_scale, (255, 0, 0), thickness)
    cv2.putText(image, "CPU move: " + cpu_choice, (380, 80), cv2.FONT_HERSHEY_DUPLEX, font_scale, (0, 0, 255), thickness)
    cv2.putText(image, winner, (240, 200), cv2.FONT_HERSHEY_DUPLEX, font_scale, winner_colour, thickness)
    cv2.putText(image, "You: " + str(player_score), (20, 120), cv2.FONT_HERSHEY_DUPLEX, font_scale, (255, 0, 0), thickness)
    cv2.putText(image, "CPU: " + str(cpu_score), (380, 120), cv2.FONT_HERSHEY_DUPLEX, font_scale, (0, 0, 255), thickness)

    cv2.imshow('Rock, Paper, Scissors', image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

webcam.release()
cv2.destroyAllWindows()
