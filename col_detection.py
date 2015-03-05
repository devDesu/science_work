import cv2
import numpy as np
from Tkinter import *
import tkFileDialog
import os.path
import time
import threading

lBoun = np.array([0, 0, 0], dtype=np.uint8)  # b,g,r
uBoun = np.array([62, 62, 62], dtype=np.uint8)

class Video():
    def __init__(self):
        # print "i'm in class"+str(self)
        self.runs = True

    def stop(self):
        self.runs = False

    # noinspection PyBroadException
    def getPics(self, lbound, ubound, tosave, frmtostrt,
                maximum, lheight, uheight, filename,
                sblack, swhite, soriginal):
        # print "i'm in" + str(self)
        if sblack:
            try:
                os.mkdir("black")
            except:
                pass
        if swhite:
            try:
                os.mkdir("white")
            except:
                pass
        if soriginal:
            try:
                os.mkdir("original")
            except:
                pass
        saveable = False
        cap = cv2.VideoCapture(filename.encode("utf-8"))
        i = 0
        cnt = 0
        total = 0
        waiter = 0
        while not cap.isOpened():
            time.sleep(1)
            cnt += 1
            if cnt > 10:
                return
        try:
            flName.set(cap.isOpened())
            while cap.isOpened():
                if not self.runs:
                    # print 'exiting'
                    cap.release()
                    return
                rd, fram = cap.read()
                while not rd:
                    rd, fram = cap.read()
                    waiter += 1
                    time.sleep(0.1)
                    if waiter > 5:
                        raise TypeError()
                if total > frmtostrt:
                    lowerTemp = lheight if ((fram.shape[0] >= lheight) and (lheight < uheight)) else 0
                    upperTemp = uheight if ((fram.shape[0] >= uheight) and (lheight < uheight)) else fram.shape[0]
                    fram = fram[lowerTemp:upperTemp, :]  # y,x
                    mask = cv2.inRange(fram, lbound, ubound)
                    # res = cv2.bitwise_and(frame, frame, mask=mask)
                    # imgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
                    thresh = cv2.adaptiveThreshold(mask,
                                                   255,
                                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                   cv2.THRESH_BINARY, 11, 2)
                    edged = cv2.Canny(thresh,
                                      80, 200)
                    contours, hierarchy = cv2.findContours(np.copy(edged),
                                                           cv2.RETR_EXTERNAL,
                                                           cv2.CHAIN_APPROX_SIMPLE)
                    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
                    for contour in contours:
                        # temp = np.array(contour)
                        # x, y, w, h = cv2.boundingRect(temp)
                        # pt1 = (bound_rect[0], bound_rect[1])
                        # pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                        # cv2.rectangle(frame, pt1, pt2, cv2.cv.CV_RGB(255,0,0), 1)
                        if cv2.contourArea(contour) > 110:
                            saveable = True
                    cnt += 1
                    if saveable and cnt >= tosave and i < maximum:
                        i += 1
                        if sblack:
                            cv2.imwrite(os.path.join("black",
                                                     ('file' + str(i) + '.png')), mask)
                            flName.set('saving' + str(i))
                        if swhite:
                            mask2 = 255 - mask
                            cv2.imwrite(os.path.join("white",
                                                     ('file' + str(i) + '.png')), mask2)
                        if soriginal:
                            cv2.imwrite(os.path.join("original",
                                                     ('file' + str(i) + '.png')), fram)
                        cnt = 0
                        saveable = False

                else:
                    total += 1
        except TypeError:
            flName.set("Finished")
            cap.release()


def set_bounds(ev):
    case = str(ev.widget)[1:].split(".")
    # noinspection PyBroadException
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
        pass


def set_y_bounds(ev):
    case = str(ev.widget)[1:].split(".")
    try:
        if case[1] == 'lower y border':
            ybounds[0] = int(ev.widget.get())
        elif case[1] == 'upper y border':
            ybounds[1] = int(ev.widget.get())
    except:
        pass

def select_file(event):
    fn = tkFileDialog.Open(root, filetypes=[('video files', '.mp4 .mov .avi')]).show()
    if fn == '':
        return
    flName.set(fn)


def create_scales(seq, fram, pointer):
    for nm in seq:
        scale1 = Scale(fram, orient=HORIZONTAL, length=400,
                       from_=0, to=255, tickinterval=15, resolution=1, name=nm[0])
        scale1.set(nm[1])
        label1 = Label(frame, text=nm[0])
        label1.pack()
        scale1.pack()
        scale1.bind("<ButtonRelease-1>", pointer)


def on_quit():
    vd.stop()
    root.quit()
    root.destroy()

# main interface
vd = Video()
root = Tk()
root.protocol("WM_DELETE_WINDOW", on_quit)
var = IntVar()  # save black
var2 = IntVar()  # save white
var3 = IntVar()  # save original image
ybounds = [0, 200]
flName = StringVar(value="")
frame = Frame(root, width=900, height=400, border=5)
frame.pack(side="top", expand=True, fill=X)
c = Label(frame, textvariable=flName)
c.pack()
frame = Frame(root, width=900, height=400, border=8)
frame.pack(side="top", expand=True, fill=X)
c = Button(frame, text="Select file", width=10)
c.bind("<1>", select_file)
c.pack()
frame = Frame(root, width=900, height=400, border=8)
frame.pack(side="top", expand=True, fill=X)
c = Button(frame, text="Go!", width=10)
c.bind("<1>", lambda(event): threading.Thread(target=vd.getPics,
                                              name='pics', args=(lBoun,
                                                                 uBoun, int(c1.get()), int(c2.get()), int(c3.get()),
                                                                 ybounds[0], ybounds[1], os.path.realpath(flName.get()),
                                                                 var.get(), var2.get(), var3.get())).start())
c.pack()
frame = Frame(root, width=900, height=100, border=10)
frame.pack(expand=True)
#  advanced settings
c = Label(frame, text="advanced", font=("Times", "18"))
c.pack(fill=X)

frame = Frame(root, name="borders")
frame.pack(side="top")
create_scales((('upper y border', 200), ('lower y border', 0)), frame, set_y_bounds)

frame = Frame(root, width=900, height=100, border=10)
frame.pack(expand=True)
c = Checkbutton(frame, text="save black", onvalue=1, offvalue=0,
                variable=var)
c.select()
c.pack(side='right')
c = Checkbutton(frame, text="save white", onvalue=1, offvalue=0,
                variable=var2)
c.select()
c.pack(side='right')
c = Checkbutton(frame, text="save original", onvalue=1, offvalue=0,
                variable=var3)
c.select()
c.pack(side='right')
c1 = Entry(frame)
c1.insert(0, "20")
c1.pack()
c = Label(frame, text="each %number% frame pic will be taken")
c.pack()
c2 = Entry(frame)
c2.insert(0, "0")
c2.pack()
c = Label(frame, text="frame to start. 1 second ~ 24 frames")
c.pack()
c3 = Entry(frame)
c3.insert(0, "100")
c3.pack()
c = Label(frame, text="max amount of pics")
c.pack()
frame = Frame(root, width=450, name="scalesLower")
frame.pack(side="left")
create_scales((('blueLower', 0), ('greenLower', 0), ('redLower', 0)), frame, set_bounds)
frame = Frame(root, width=450, name="scalesUpper")
frame.pack(side="right")
create_scales((('blueUpper', 62), ('greenUpper', 62), ('redUpper', 62)), frame, set_bounds)
root.mainloop()
