import cv2
import numpy as np
import HandTrackingModule as htm
import pyautogui
import time

# Screen width and height
screenWidth, screenHeight = pyautogui.size()

# Camera settings
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionCon=0.7)

# Smoothening factor
smoothening = 7
prevX, prevY = 0, 0
currX, currY = 0, 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip

        fingers = []
        if lmList[4][1] > lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(8, 21, 4):
            if lmList[id][2] < lmList[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (75, wCam - 75), (0, screenWidth))
            y3 = np.interp(y1, (75, hCam - 75), (0, screenHeight))

            currX = prevX + (x3 - prevX) / smoothening
            currY = prevY + (y3 - prevY) / smoothening

            pyautogui.moveTo(screenWidth - currX, currY)
            prevX, prevY = currX, currY

        if fingers[1] == 1 and fingers[2] == 1:
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            if length < 40:
                pyautogui.click()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
