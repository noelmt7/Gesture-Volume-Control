import cv2
import time
import numpy as np
import HandTrackingModule as htm
import pyautogui

# Camera settings
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# Hand detector
detector = htm.handDetector(detectionCon=0.7)

# Function to check which fingers are up
def fingersUp(lmList):
    fingers = []
    # Thumb
    if lmList[4][1] > lmList[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    # 4 Fingers
    for id in range(8, 21, 4):
        if lmList[id][2] < lmList[id - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

# Media control state
mediaControl = {"playing": False, "paused": False}

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # Media control logic
        fingers = fingersUp(lmList)
        if fingers.count(1) == 5:
            if not mediaControl["playing"]:
                pyautogui.press("playpause")
                mediaControl["playing"] = True
                mediaControl["paused"] = False
        elif fingers.count(1) == 0:
            if not mediaControl["paused"]:
                pyautogui.press("playpause")
                mediaControl["paused"] = True
                mediaControl["playing"] = False

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
