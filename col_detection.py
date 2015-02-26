import cv2
import numpy as np
from Tkinter import *

root=Tk()
root.mainloop()

def lower(i):
    lBound[0]=i

def upper(i):
    uBound[0]=i

def lower1(i):
    lBound[1]=i

def upper1(i):
    uBound[1]=i

def lower2(i):
    lBound[2]=i

def upper2(i):
    uBound[2]=i

def get_pics(lBound, uBound, toSave, lHeight, uHeight, filename):
    saveable=False
    #lBound = np.array([0, 0, 0], dtype=np.uint8)
    #uBound = np.array([62,62,62], dtype=np.uint8)
    cap = cv2.VideoCapture(filename)
    i=0
    cnt=0
    try:
        while(cap.isOpened()):
            _, frame = cap.read()
            frame = frame[lHeight:uHeight, :] #y,x
            mask = cv2.inRange(frame, lBound, uBound)
            res = cv2.bitwise_and(frame, frame, mask = mask)
            imgray = cv2.cvtColor(res,
                                  cv2.COLOR_BGR2GRAY)
            thresh=cv2.adaptiveThreshold(mask,
                                         255,
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                         cv2.THRESH_BINARY,11,2)
            edged = cv2.Canny(thresh,
                              80, 200)
            contours, hierarchy = cv2.findContours(np.copy(edged),
                                                   cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
            for contour in  contours:
                #temp = np.array(contour)
                #bound_rect = cv2.boundingRect(temp)
                #pt1 = (bound_rect[0], bound_rect[1])
                #pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                #cv2.rectangle(frame, pt1, pt2, cv2.cv.CV_RGB(255,0,0), 1)
                if(cv2.contourArea(contour)>110):
                    saveable=True
            cnt+=1
            if(saveable and cnt>=toSave):
                    cv2.imwrite('file'+str(i)+'.png',mask)
                    i+=1
                    cnt=0
            saveable=False
    except TypeError:
        print "Finishing..."
        cap.release()
