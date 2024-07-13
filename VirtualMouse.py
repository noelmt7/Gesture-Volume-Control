import cv2
import mediapipe as mp
import time
import pyautogui
import numpy as np

# Initialize mediapipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Screen and camera dimensions
wScr, hScr = pyautogui.size()
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            if lm_list:
                x1, y1 = lm_list[8][1], lm_list[8][2]  # Index finger tip
                x2, y2 = lm_list[12][1], lm_list[12][2]  # Middle finger tip

                # Convert Coordinates
                x3 = np.interp(x1, (75, 640-75), (0, wScr))
                y3 = np.interp(y1, (75, 480-75), (0, hScr))

                # Smooth Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # Move Mouse
                pyautogui.moveTo(wScr - clocX, clocY)
                plocX, plocY = clocX, clocY

                # Click Mouse
                length = np.hypot(x2 - x1, y2 - y1)
                if length < 40:
                    pyautogui.click()

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
