import cv2
import time
import numpy as np
import HandTrackingModule as htm
import pyautogui

class HandControl:
    def __init__(self, wCam=640, hCam=480, detectionCon=0.7):
        self.wCam, self.hCam = wCam, hCam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)
        self.pTime = 0

        self.detector = htm.handDetector(detectionCon=detectionCon)

        # Media control state
        self.mediaControl = {"playing": False, "paused": False}
        self.lastActionTime = 0
        self.message = ""
        self.messageTime = 0

    def fingersUp(self, lmList):
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

    def process_frame(self):
        success, img = self.cap.read()
        if not success:
            return None  # Return None if frame is not captured successfully

        img = cv2.flip(img, 1)
        img = self.detector.findHands(img)
        lmList = self.detector.findPosition(img, draw=False)

        currentTime = time.time()

        if len(lmList) != 0:
            fingers = self.fingersUp(lmList)
            if fingers.count(1) == 5 and not self.mediaControl["playing"]:
                if currentTime - self.lastActionTime > 1:  # Prevents repeated commands
                    pyautogui.press("playpause")
                    self.mediaControl["playing"] = True
                    self.mediaControl["paused"] = False
                    self.message = "Paused"
                    self.messageTime = currentTime
                    self.lastActionTime = currentTime

            elif fingers.count(1) == 0 and not self.mediaControl["paused"]:
                if currentTime - self.lastActionTime > 1:  # Prevents repeated commands
                    pyautogui.press("playpause")
                    self.mediaControl["paused"] = True
                    self.mediaControl["playing"] = False
                    self.message = "Resumed"
                    self.messageTime = currentTime
                    self.lastActionTime = currentTime

            # Check if only the thumb or index finger is up
            if fingers[1:] == [1, 0, 0, 0] and not fingers[0]:  # Index finger up
                cv2.putText(img, 'Volume Up', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                # Code to increase volume

            elif fingers[0] and not any(fingers[1:]):  # Thumb up
                cv2.putText(img, 'Volume Down', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                # Code to decrease volume

        # Display pause/resume message for at least 7 seconds
        if self.message and currentTime - self.messageTime <= 7:
            cv2.putText(img, self.message, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        return img

if __name__ == "__main__":
    handControl = HandControl()
    while True:
        img = handControl.process_frame()
        if img is not None:
            cv2.imshow("Img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    handControl.cap.release()
    cv2.destroyAllWindows()
