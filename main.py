import cv2
import numpy as np
from time import sleep

width_min = 80 # Minimum rectangle width
height_min = 80 # Minimum rectangle height

offset = 6 # Margin of error between pixels

line_position = 450 # Line position (vertically)

delay = 60 # Video FPS

detect = []
cars = 0

	
def center_point(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

video_src = cv2.VideoCapture('video.mp4')
subtract = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret , frame1 = video_src.read()
    time = float(1/delay)
    sleep(time) 
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    img_sub = subtract.apply(blur)
    dilation = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatation = cv2.morphologyEx (dilation, cv2. MORPH_CLOSE , kernel)
    dilatation = cv2.morphologyEx (dilatation, cv2. MORPH_CLOSE , kernel)
    contour,h = cv2.findContours(dilatation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1, (25, line_position), (1200, line_position), (255,127,0), 3) 
    for(i,c) in enumerate(contour):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_outline = (w >= width_min) and (h >= height_min)
        if not validate_outline:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)        
        center = center_point(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0,255), -1)

        for (x,y) in detect:
            if y<(line_position+offset) and y>(line_position-offset):
                cars+=1
                cv2.line(frame1, (25, line_position), (1200, line_position), (0,127,255), 3)  
                detect.remove((x,y))
                print("car is detected : "+str(cars))        
       
    cv2.putText(frame1, "Vehile counted : "+str(cars), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("Video Original" , frame1)
    cv2.imshow("dilatation",dilatation)

    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
video_src.release()
