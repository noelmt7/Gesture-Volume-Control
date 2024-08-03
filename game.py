import cv2
import time
import pyautogui
import HandTrackingModule as htm  # Assuming this is your handDetector class

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

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = fingersUp(lmList)

        # Mapping gestures to keys
        if fingers == [1, 1, 1, 1, 1]:
            pyautogui.press('up')  # Open hand -> Up arrow key
            cv2.putText(img, 'UP', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
        elif fingers == [0, 0, 0, 0, 0]:
            pyautogui.press('down')  # Closed hand -> Down arrow key
            cv2.putText(img, 'DOWN', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    
    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()