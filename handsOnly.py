import os
from cvzone.HandTrackingModule import HandDetector
import cv2 

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/Background.png");

folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []

for imgMode in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgMode)))

print(listImgModes)

modeType = 0 # fro changing the mode

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    #overlaying the webcam feed on the background image
    imgBackground[139:139+480, 50:50+640] = img
    imgBackground[0:720, 847:1280] = listImgModes[modeType]

    if hands:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)   
        print(fingers1)

    #Display the images
    cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)