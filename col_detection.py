import cv2
import numpy as np
from Tkinter import *
import tkFileDialog

lBound = np.array([0, 0, 0], dtype=np.uint8)    #b,g,r
uBound = np.array([62,62,62], dtype=np.uint8)

def setBounds(ev):
    case = str(ev.widget)[1:].split(".")
    try:
        if case[1] == 'blueLower':
            uBound[0] = ev.widget.get()
        elif case[1] == 'greenLower':
            uBound[1] = ev.widget.get()
        elif case[1] == 'redLower':
            lBound[2] = ev.widget.get()
        elif case[1] == 'blueUpper':
            uBound[0] = ev.widget.get()
        elif case[1] == 'greenUpper':
            uBound[1] = ev.widget.get()
        elif case[1] == 'redUpper':
            uBound[2] = ev.widget.get()
    except:
        print "error"

def selectFile(ev): 
    fn = tkFileDialog.Open(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    flName.set(fn)
  
def createScales(seq, frame):
    for nm in seq:
        scale1 = Scale(frame,orient = HORIZONTAL,length = 400,
                       from_ = 0, to = 255, tickinterval = 15, resolution = 1, name = nm[0])
        scale1.set(nm[1])
        label1 = Label(frame, text = nm[0])
        label1.pack()
        scale1.pack()
        scale1.bind("<1>", setBounds)

root=Tk()
flName = StringVar(value="")
label1 = Label(root, textvariable = flName)
label1.pack()


frame = Frame(root, width = 900, height = 200, name = "main")
frame.pack(side = "top")
bt = Button(frame, text = "Select file")
bt.bind("<1>", selectFile)
bt.pack()
frame = Frame(root, width = 450, name="scalesLower")
frame.pack(side="left")
createScales([['blueLower',0],['greenLower',0],['redLower',0]], frame)
frame = Frame(root, width = 450, name = "scalesUpper")
frame.pack(side="right")
createScales([['blueUpper',0],['greenUpper',0],['redUpper',0]], frame)
root.mainloop()


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
