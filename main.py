import os
from cvzone.HandTrackingModule import HandDetector
import cv2 

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/Background.png");

#import all the mode images to a list
folderPathModes = "Resources/Modes"
listImgModesPath = sorted(os.listdir(folderPathModes))
listImgModes = []

for imgMode in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgMode)))

#import all the icons to a list
folderPathIcons = "Resources/Icons"
listImgIconsPath = sorted(os.listdir(folderPathIcons))
listImgIcons = []

for imgIcon in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIcon)))



modeType = 0 # for changing the mode
selection = -1 # for changing selection
counter = 0
selectionSpeed = 7
modePosition = [(1136,196),(1000,384),(1136,581)]
counterPause = 0
selectionList = [-1,-1,-1]

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    #overlaying the webcam feed on the background image
    imgBackground[139:139+480, 50:50+640] = img
    resized_image = cv2.resize(listImgModes[modeType], (433, 720))
    imgBackground[0:720, 847:1280] = resized_image

    if hands and counterPause == 0 and modeType < 3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)   
        # print(fingers1)
        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2        
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3        
        else:
            selection = -1
            counter = 0

        if counter >0:
            counter +=1
            # print(counter)

            cv2.ellipse(imgBackground, modePosition[selection-1], (103,103), 0, 0, counter*selectionSpeed, (255,51,204),20)
            if counter*selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType +=1
                counter=0
                selection=-1
                counterPause = 1

    # Pause after each selection is made
    if counterPause > 0:
        counterPause += 1
        if counterPause > 10:
            counterPause = 0
    
    # Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[636:636+66, 133:133+66] = listImgIcons[selectionList[0]-1]
    if selectionList[1] != -1:
        imgBackground[636:636+66, 340:340+66] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636+66, 542:542+66] = listImgIcons[5 + selectionList[2]]

    #Display the images
    cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)