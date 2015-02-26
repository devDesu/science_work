import cv2
import numpy as np
import random

def lower(i):
    lower_blue[0]=i

def upper(i):
    upper_blue[0]=i

def lower1(i):
    lower_blue[1]=i

def upper1(i):
    upper_blue[1]=i

def lower2(i):
    lower_blue[2]=i

def upper2(i):
    upper_blue[2]=i

#cap = cv2.VideoCapture("file.mov")#0)
#cap.set(3, 450)
#cap.set(4, 450)
#cap.set(5, 10)
saveable=False
lastx=0
lasty=0
posx=0
posy=0
cv2.namedWindow('frame')
cv2.createTrackbar('blue_low','frame',0,255,lower)
cv2.createTrackbar('blue_upper','frame',54,255,upper)
cv2.createTrackbar('green_low','frame',0,255,lower1)
cv2.createTrackbar('green_upper','frame',54,255,upper1)
cv2.createTrackbar('red_low','frame',0,255,lower2)
cv2.createTrackbar('red_upper','frame',54,255,upper2)
lower_blue = np.array([0, 0, 0], dtype=np.uint8)
upper_blue = np.array([62,62,62], dtype=np.uint8)

# frame = cv2.imread("detect.png",-1)
# frame1 = cv2.GaussianBlur(frame, (9,9), 10)
# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
cap = cv2.VideoCapture("file.mp4")
i=0
cnt=0
while(1):
        #frame=np.copy(frame1)
    _, frame = cap.read()
    frame = frame[65:135,:] #y,x
    #frame=cv2.GaussianBlur(frame, (5,5), 11)
    mask = cv2.inRange(frame, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    imgray = cv2.cvtColor(res,
                          cv2.COLOR_BGR2GRAY)
    thresh=cv2.adaptiveThreshold(mask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                 cv2.THRESH_BINARY,11,2)
    edged = cv2.Canny(thresh,#imgray,
                      80, 200)
    contours, hierarchy = cv2.findContours(np.copy(edged),#thresh,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
    #print len(contours)
    #print contours
    for contour in  contours:
        temp = np.array(contour)
        bound_rect = cv2.boundingRect(temp)
        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        cv2.rectangle(frame, pt1, pt2, cv2.cv.CV_RGB(255,0,0), 1)
        if(cv2.contourArea(contour)>110):
            saveable=True
        break
##        lastx=posx
##        lasty=posy
##        posx=cv2.cv.Round((pt1[0]+pt2[0])/2)
##        posy=cv2.cv.Round((pt1[1]+pt2[1])/2)
##        if lastx!=0 and lasty!=0:
##            cv2.line(res,(posx,posy),(lastx,lasty),(0,255,255))
##            cv2.circle(res,(posx,posy),5,(0,255,255),-1)
    #thresh = cv2.GaussianBlur(thresh, (3,3), 10)
    #thresh = cv2.medianBlur(thresh,3)
    cv2.imshow('frame',frame)
    cnt+=1
    #mask = cv2.GaussianBlur(mask, (3,3), 10)
    #mask = cv2.medianBlur(mask,3)
    #mask=255-mask
    if(saveable and cnt>=20):
            cv2.imwrite('file'+str(i)+'.png',mask)
            i+=1
            cnt=0
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('thresh',thresh)
    saveable=False
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    elif k==ord('q'):
        print hierarchy
cap.release()
cv2.destroyAllWindows()
