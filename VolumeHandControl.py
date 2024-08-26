import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class HandVolumeControl:
    def __init__(self, wCam=640, hCam=480, detectionCon=0.7):
        self.wCam, self.hCam = wCam, hCam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)
        self.pTime = 0

        self.detector = htm.handDetector(detectionCon=detectionCon)

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)
        self.volRange = self.volume.GetVolumeRange()

        self.minVol = self.volRange[0]
        self.maxVol = self.volRange[1]

    def process_frame(self):
        success, img = self.cap.read()
        if not success:
            return None  # Return None if frame is not captured successfully

        img = cv2.flip(img, 1)
        img = self.detector.findHands(img)
        lmList = self.detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # Thumb
            thumb_tip = lmList[4][1:3]
            thumb_ip = lmList[3][1:3]
            thumb_open = thumb_tip[0] > thumb_ip[0]  # Right hand, for left hand thumb_tip[0] < thumb_ip[0]

            # Index finger
            index_tip = lmList[8][1:3]
            index_mcp = lmList[5][1:3]
            index_open = index_tip[1] < index_mcp[1]

            # Decrease volume if thumb is open
            if thumb_open:
                currentVol = self.volume.GetMasterVolumeLevel()
                newVol = max(currentVol - 1, self.minVol)
                self.volume.SetMasterVolumeLevel(newVol, None)
                cv2.putText(img, 'Volume Down', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Increase volume if index finger is open
            elif index_open:
                currentVol = self.volume.GetMasterVolumeLevel()
                newVol = min(currentVol + 1, self.maxVol)
                self.volume.SetMasterVolumeLevel(newVol, None)
                cv2.putText(img, 'Volume Up', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        return img

if __name__ == "__main__":
    handVolumeControl = HandVolumeControl()
    while True:
        img = handVolumeControl.process_frame()
        if img is not None:
            cv2.imshow("Img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    handVolumeControl.cap.release()
    cv2.destroyAllWindows()
