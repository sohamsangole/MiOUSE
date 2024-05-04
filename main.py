import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import autopy
import numpy as np

wCam, hCam = 640,480
frameR = 100
wScr, hScr = autopy.screen.size()
print(wScr,hScr)
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = HandDetector(maxHands=2,detectionCon=0.8)
x1,x2,x3,x4 = -1,-1,-1,-1
y1,y2,y3,y4 = -1,-1,-1,-1
fingersL = [-1, -1, -1, -1, -1]
fingersR = [-1, -1, -1, -1, -1]
while True:
    success, img = cap.read()
    hands,img = detector.findHands(img,flipType=False)
    if hands:
        if(len(hands) == 1):
            if hands[0]['type'] == 'Left':  
                x1, y1 = hands[0]['lmList'][8][:2]  
                x2, y2 = hands[0]['lmList'][12][:2]
                fingersL = detector.fingersUp(hands[0])
                fingersR = [-1, -1, -1, -1, -1]

            if hands[0]['type'] == 'Right':  
                x3, y3 = hands[0]['lmList'][8][:2]  
                x4, y4 = hands[0]['lmList'][12][:2]
                fingersL = [-1, -1, -1, -1, -1]
                fingersR = detector.fingersUp(hands[0])
        if(len(hands) == 2):
            x1, y1 = hands[0]['lmList'][8][:2]  
            x2, y2 = hands[0]['lmList'][12][:2]
            x3, y3 = hands[1]['lmList'][8][:2]  
            x4, y4 = hands[1]['lmList'][12][:2]  
            fingersL = detector.fingersUp(hands[0])
            fingersR = detector.fingersUp(hands[1])
        # print(f'x1 : {x1} y1 : {y1} x2 : {x2} y2 : {y2} x3 : {x3} y3 : {y3} x4 : {x4} y4 : {y4}')
        
        # print(fingersL,fingersR)
        # print(fingersL,fingersR)
        if fingersR == [0,1,1,1,1] or fingersR == [0,1,1,1,0] : 
            # Calculate the position of the rectangle based on the right hand
            # Calculate the position of the rectangle based on the right hand
            rect_x1 = 0
            rect_y1 = int(y3) - frameR
            rect_x2 = int(x4) - frameR
            rect_y2 = int(y4) + frameR
            cv2.rectangle(img,(rect_x1,rect_y1),(rect_x2,rect_y2),(255,0,255),2)
            if fingersL == [1,1,0,0,0] :
                rel_x = np.interp(x1, (rect_x1, rect_x2), (0, 1))
                rel_y = np.interp(y1, (rect_y1, rect_y2), (0, 1))

                # Map the relative position to the screen size
                mouseX = np.interp(x1, (rect_x1, rect_x2), (wScr,0))
                mouseY = np.interp(y1, (rect_y1, rect_y2), (0,hScr))
                
                # Move the mouse accordingly
                if rect_x1 < x1 < rect_x2 and rect_y1 < y1 < rect_y2:
                    # Move the mouse accordingly
                    autopy.mouse.move(mouseX, mouseY)

                # print("Mouse Moving")
    # Frame Rate
    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
