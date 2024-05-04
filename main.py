import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import autopy
import numpy as np

wCam, hCam = 720,405
frameR = 100
wScr, hScr = autopy.screen.size()
print(wScr,hScr)
mouse_buffer = [(wScr // 2, hScr // 2)] * 5
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = HandDetector(maxHands=2,detectionCon=0.8)
x1,x2,x3,x4 = -1,-1,-1,-1
y1,y2,y3,y4 = -1,-1,-1,-1
fingersL = [-1, -1, -1, -1, -1]
fingersR = [-1, -1, -1, -1, -1]
prev_click_state = False  # Track the previous state of click gesture
click_threshold = 30
lCentre_X = -1
lCentre_Y = -1
prev_x, prev_y = -1, -1


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
                lCentre_X = hands[0]['center'][0]
                lCentre_Y = hands[0]['center'][1]

            if hands[0]['type'] == 'Right':  
                x3, y3 = hands[0]['lmList'][8][:2]  
                x4, y4 = hands[0]['lmList'][12][:2]
                fingersL = [-1, -1, -1, -1, -1]
                fingersR = detector.fingersUp(hands[0])
                lCentre_X = -1
                lCentre_Y = -1
        if(len(hands) == 2):
            x1, y1 = hands[0]['lmList'][8][:2]  
            x2, y2 = hands[0]['lmList'][12][:2]
            x3, y3 = hands[1]['lmList'][8][:2]  
            x4, y4 = hands[1]['lmList'][12][:2]  
            fingersL = detector.fingersUp(hands[0])
            fingersR = detector.fingersUp(hands[1])
            lCentre_X = hands[0]['center'][0]
            lCentre_Y = hands[0]['center'][1]
        # print(f'x1 : {x1} y1 : {y1} x2 : {x2} y2 : {y2} x3 : {x3} y3 : {y3} x4 : {x4} y4 : {y4}')
        # Mouse Movement & Clicking
        if fingersR == [0,1,1,1,1] or fingersR == [0,1,1,1,0] : 
            rect_x1 = 0 + int(frameR / 3)
            rect_y1 = int(y3) - frameR
            rect_x2 = int(x4) - frameR
            rect_y2 = int(y4) + frameR
            cv2.rectangle(img,(rect_x1,rect_y1),(rect_x2,rect_y2),(255,0,255),2)
            if fingersL == [0,1,1,1,1] :
                centroid = np.mean(np.array(hands[0]["lmList"][1:]), axis=0, dtype=np.int)
                # m1 = x1
                # m2 = y1
                m1 = centroid[0]
                m2 = centroid[1]
                print(lCentre_X,lCentre_Y)
                # Map the relative position to the screen size
                mouseX = np.interp(m1, (rect_x1, rect_x2), (wScr,0))
                mouseY = np.interp(m2, (rect_y1, rect_y2), (0,hScr))
                
                mouse_buffer.pop(0)  # Remove oldest position
                mouse_buffer.append((mouseX, mouseY))  # Add current position to buffer
                smoothMouseX, smoothMouseY = np.mean(mouse_buffer, axis=0)  
                
                # Move the mouse accordingly
                if rect_x1 < m1 < rect_x2 and rect_y1 < m2 < rect_y2:
                    # Move the mouse accordingly
                    autopy.mouse.move(smoothMouseX, smoothMouseY)
                # print("Mouse Moving")

                lmList1 = hands[1]["lmList"]
                length, info, img = detector.findDistance(lmList1[4][0:2], lmList1[8][0:2], img, color=(0, 255, 0),scale=5)
                # Calculate the distance between thumb and index finger for click gesture
                # print(length)
                if length < click_threshold:  # If distance is less than threshold, it's a click gesture
                    if not prev_click_state:  # If previous state was not clicking, simulate a click
                        autopy.mouse.click()  # Perform left-click action
                        prev_click_state = True 
                    # Select text if hand is moved after clicking
                    if prev_x != -1 and prev_y != -1:
                        if prev_click_state or (prev_x != m1 or prev_y != m2):
                            autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=True)
                        else :
                            autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=False)
                    # Update previous hand position
                    prev_x, prev_y = m1, m2
                else:
                    prev_click_state = False  
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=False)# Update previous click state if not clicking
                    prev_x = -1
                    prev_y = -1

    # Frame Rate
    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
