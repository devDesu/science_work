import cv2
import numpy as np
from Tkinter import *
import tkFileDialog
import os.path

lBoun = np.array([0, 0, 0], dtype=np.uint8)    # b,g,r
uBoun = np.array([62,62,62], dtype=np.uint8)

def getPics(lBound, uBound, toSave, lHeight, uHeight, filename, sBlack, sWhite):
    if(sBlack):
        try:
            os.mkdir("black")
        except:
            pass
    if(sWhite):
        try:
            os.mkdir("white")
        except:
            pass
    saveable=False
    print filename
    #lBound = np.array([0, 0, 0], dtype=np.uint8)
    #uBound = np.array([62,62,62], dtype=np.uint8)
    cap = cv2.VideoCapture(filename.encode("utf-8"))
    i=0
    cnt=0
    try:
		#flName.set(cap.isOpened())
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
                    if(sBlack):
                        cv2.imwrite(os.path.join("black",
                                                 ('file'+str(i)+'.png')),mask)
                    elif(sWhite):
                        cv2.imwrite(os.path.join("white",
                                                 ('file'+str(i)+'.png')),mask)
                    i+=1
                    cnt=0
            saveable=False
    except TypeError:
        print "Finishing..."
        cap.release()

def setBounds(ev):
    case = str(ev.widget)[1:].split(".")
    try:
        if case[1] == 'blueLower':
            uBoun[0] = ev.widget.get()
        elif case[1] == 'greenLower':
            uBoun[1] = ev.widget.get()
        elif case[1] == 'redLower':
            lBoun[2] = ev.widget.get()
        elif case[1] == 'blueUpper':
            uBoun[0] = ev.widget.get()
        elif case[1] == 'greenUpper':
            uBoun[1] = ev.widget.get()
        elif case[1] == 'redUpper':
            uBoun[2] = ev.widget.get()
    except:
        print "error"

def selectFile(ev): 
    fn = tkFileDialog.Open(root, filetypes = [('video files', '.mp4 .mov .avi')]).show()
    if fn == '':
        return
    flName.set(fn)
  
def createScales(seq, frame):
    for nm in seq:
        scale1 = Scale(frame, orient = HORIZONTAL, length = 400,
                       from_ = 0, to = 255, tickinterval = 15, resolution = 1, name = nm[0])
        scale1.set(nm[1])
        label1 = Label(frame, text = nm[0])
        label1.pack()
        scale1.pack()
        scale1.bind("<1>", setBounds)

def tryProcess(ev):
    print var.get()
    getPics(lBoun, uBoun, int(c1.get()), 35, 150,
            os.path.realpath(flName.get()), var.get(), var2.get())

#main interface
root=Tk()
var = IntVar() # save black
var2 = IntVar() # save white
flName = StringVar(value="")
frame = Frame(root, width = 900, height = 400, border = 5)
frame.pack(side = "top", expand = True, fill = X)
c = Label(frame, textvariable = flName)
c.pack()
frame = Frame(root, width = 900, height = 400, border = 8)
frame.pack(side = "top", expand = True, fill = X)
c = Button(frame, text = "Select file", width = 10)
c.bind("<1>", selectFile)
c.pack()
frame = Frame(root, width = 900, height = 400, border = 8)
frame.pack(side = "top", expand = True, fill = X)
c = Button(frame, text = "Go!", width = 10)
c.bind("<1>", tryProcess)
c.pack()
frame = Frame(root, width = 900, height = 100, border = 10)
frame.pack(expand = True)
#advanced settings
c = Label(frame, text = "advanced", font = ("Times", "18"))
c.pack(fill = X)
frame = Frame(root, width = 900, height = 100, border = 10)
frame.pack(expand = True)
c = Checkbutton(frame, text = "save black", onvalue = 1, offvalue = 0, variable = var)
c.select()
c.pack(side = 'right')
c = Checkbutton(frame, text = "save white", onvalue = 1, offvalue = 0, variable = var2)
c.select()
c.pack(side = 'right')
c1 = Entry(frame)
c1.insert(0, "20")
c1.pack()
c = Label(frame, text = "each %number% frame pic will be taken")
c.pack()
frame = Frame(root, width = 450, name="scalesLower")
frame.pack(side="left")
createScales([['blueLower',0],['greenLower',0],['redLower',0]], frame)
frame = Frame(root, width = 450, name = "scalesUpper")
frame.pack(side="right")
createScales([['blueUpper',62],['greenUpper',62],['redUpper',62]], frame)
root.mainloop()
