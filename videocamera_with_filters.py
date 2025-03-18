import cv2 as cv
import numpy as np

cam_original = cv.VideoCapture(0)  # video input from webcam

fourcc = cv.VideoWriter_fourcc(*'avc1')  # specify codec

#get frame information of the webcam
frame_width = int(cam_original.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam_original.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cam_original.get(cv.CAP_PROP_FPS))

wait_msec = int(1000 / fps) #frame of saved video.

out = cv.VideoWriter('videowithfilters.mp4', fourcc, fps, (frame_width , frame_height))  #output video

recording = False #recording state. toggles between true(recording), and false(waiting).
record_icon = (30, 30) #the center value of record circle.
pt1 = (60, 50) #record message will be put here.

record_appendices = [" with no filter...", " with bright filter", " with mono filter", " with negative image filter"] #messages tell you about current filter 

#indicators for filter/message selection
frame_indicator = 0
append_indicator = 0 

while cam_original.isOpened():
    
    valid, frame = cam_original.read() 
    if not valid: #check validity of the video source.
        break
    
    frame_contrast_bright = cv.convertScaleAbs(frame, alpha=1.0, beta=35)  #bright filter
    frame_mono = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_mono_color = cv.cvtColor(frame_mono, cv.COLOR_GRAY2BGR) #mono filter
    frame_nega = 255 - frame #negative color image filter
    
    filters = [frame, frame_contrast_bright, frame_mono_color, frame_nega] #list of filters
    
    #separating frame being showed from frame being recorded
    frame_show = filters[frame_indicator]
    frame_save = filters[frame_indicator]
    
    cv.imshow('Video', frame_show)  # show frame
    
    if recording == True:
        out.write(frame_save)  # saving process 
        cv.circle(frame_show, record_icon, radius=20, color=(0, 0, 255), thickness= -1)  #record circle
        record_messege = "Recording" + record_appendices[append_indicator] #record message that notices you that recording in process with current filter.
        cv.putText(frame_show, record_messege, pt1, cv.FONT_HERSHEY_COMPLEX, 1, (147, 20, 255), thickness=3) #shows the record message made from above.
        cv.imshow('Video', frame_show) #shows recording frame plus recording circle and recording message.
    
    key = cv.waitKey(wait_msec)
    if key == 27:  # 'ESC' to quit the program
        break
    elif key == 32:  # 'space bar' to toggle record/wait. default state is wait. 
        recording = not recording
    elif key == ord('1'): #no filter
        frame_indicator = 0
        append_indicator = 0
    elif key == ord('2'): #filter 2 : bright 
        frame_indicator = 1
        append_indicator = 1
    elif key == ord('3'): #filter 3 : mono
         frame_indicator = 2
         append_indicator = 2
    elif key == ord('4'):  #filter 4 : negative video
        frame_indicator = 3
        append_indicator = 3

#finishing program :)
cam_original.release()
out.release()
cv.destroyAllWindows()