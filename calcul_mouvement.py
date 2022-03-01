#// Don't forget to hit SUBSCRIBE, LIKE, COMMENT, and LEARN! its good to learn :)

#imports
import cv2
import time
from datetime import datetime
import imutils
import numpy as np
#from Collect_Data import *
debugToken=0


def motion_detection(_tps):

    _temps_lancement = datetime.now()
    _temps_maintenant = datetime.now()
    difference = (_temps_maintenant - _temps_lancement).total_seconds()
    first_frame = None # instinate the first fame
    activityFactor = 0
    video_capture = cv2.VideoCapture(0)
    while difference < _tps:
        #video_capture = cv2.VideoCapture('rtsp://Arthur:P0pu$$e@192.168.0.27:554/stream2')
        # value (0) selects the devices default camera
        #cv2.destroyAllWindows()
        print("Round activity factor result :" + str(int(activityFactor))+ "\nTime remaining : " + str(int(_tps-difference)) +"s")


        if not video_capture.isOpened():
            print("Cannot open camera")


        #time.sleep(1)

        frame = video_capture.read()[1] # gives 2 outputs retval,frame - [1] selects frame
        text = 'Unoccupied'

        if debugToken:
            cv2.imshow("frame", frame)
            cv2.waitKey()
            cv2.destroyAllWindows()

        greyscale_frame = cv2.cvtColor(frame, 6) #cv2.COLOR_BGRA2GRAY=6 # make each frame greyscale wich is needed for threshold

        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21,21),0)
        # uses a kernal of size(21,21) // has to be odd number to to ensure there is a valid integer in the centre
        # and we need to specify the standerd devation in x and y direction wich is the (0) if only x(sigma x) is specified
        # then y(sigma y) is taken as same as x. sigma = standerd deveation(mathmetics term)

        blur_frame = cv2.blur(gaussian_frame, (5,5)) # uses a kernal of size(5,5)(width,height) wich goes over 5x5 pixel area left to right
        # does a calculation and the pixel located in the centre of the kernal will become
        # a new value(the sum of the kernal after the calculations) and then it moves to the right one and has a new centre pixel
        # and does it all over again..untill the image is done, obv this can cause the edges to not be changed, but is very minute

        greyscale_image = blur_frame
        # greyscale image with blur etc wich is the final image ready to be used for threshold and motion detecion

        if first_frame is None:
            first_frame = greyscale_image
            # first frame is set for background subtraction(BS) using absdiff and then using threshold to get the foreground mask
            # foreground mask (black background anything that wasnt in image in first frame but is in newframe over the threshold will
            # be a white pixel(white) foreground image is black with new object being white...there is your motion detection
        else:
            pass


        frame = imutils.resize(frame, width=500)
        frame_delta = cv2.absdiff(first_frame, greyscale_image)
        # calculates the absolute diffrence between each element/pixel between the two images, first_frame - greyscale (on each element)
        if debugToken:
            cv2.imshow("frame_delta", frame_delta)
            cv2.waitKey()
            cv2.destroyAllWindows()


        # edit the ** thresh ** depending on the light/dark in room, change the 100(anything pixel value over 100 will become 255(white))
        #thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
        # threshold gives two outputs retval,threshold image. using [1] on the end i am selecting the threshold image that is produced

        thresh_adaptative = cv2.adaptiveThreshold(frame_delta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,11,2)

        dilate_image = cv2.dilate(thresh_adaptative, None, iterations=2)
        # dilate = dilate,grow,expand - the effect on a binary image(black background and white foregorund) is to enlarge/expand the white
        # pixels in the foreground wich are white(255), element=Mat() = default 3x3 kernal matrix and iterartions=2 means it
        # will do it twice

        kernel = np.ones((3,3),np.uint8)
        opened_image = cv2.morphologyEx(thresh_adaptative, cv2.MORPH_OPEN, kernel)

        cnt = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        # contours gives 3 diffrent ouputs image, contours and hierarchy, so using [1] on end means contours = [1](cnt)
        # cv2.CHAIN_APPROX_SIMPLE saves memory by removing all redundent points and comppressing the contour, if you have a rectangle
        # with 4 straight lines you dont need to plot each point along the line, you only need to plot the corners of the rectangle
        # and then join the lines, eg instead of having say 750 points, you have 4 points.... look at the memory you save!

        if debugToken:
            if cnt is None: print("cnt is none!")
            cv2.imshow("thresh", thresh_adaptative)
            cv2.imshow("dilate_image", dilate_image)
            cv2.waitKey()
            cv2.destroyAllWindows()


        if cnt is not None:
            for c in cnt:
                activityFactor = activityFactor + cv2.contourArea(c)
                if cv2.contourArea(c) > 200: # if contour area is less then 800 non-zero(not-black) pixels(white)
                    (x, y, w, h) = cv2.boundingRect(c) # x,y are the top left of the contour and w,h are the width and hieght

                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) # (0, 255, 0) = color R,G,B = lime / 2 = thickness(i think?)(YES IM RITE!)
                    cv2.rectangle(dilate_image, (x,y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(dilate_image, 'Cnt val: %s' % (str(cv2.boundingRect(c))),
                        (x,y-20), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0, 0, 255), 2)#
                    #image used for rectangle is frame so that its on the secruity feed image and not the binary/threshold/foreground image
                    # as its already used the threshold/(binary image) to find the contours this image/frame is what image it will be drawed on

                    text = 'Occupied'
                    # text that appears when there is motion in video feed
                else:
                    pass


        ''' now draw text and timestamp on security feed '''
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(frame, '{+} Room Status: %s' % (text),
            (10,20), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0, 0, 255), 2)
        # frame is the image on wich the text will go. 0.5 is size of font, (0,0,255) is R,G,B color of font, 2 on end is LINE THICKNESS! OK :)
        cv2.putText(frame, '{+} Activity Factor: ' + str(int(activityFactor)) ,
            (10,40), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0, 0, 255), 2)


        cv2.putText(frame, datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX , 0.35, (0, 0, 255),1) # frame.shape[0] = hieght, frame.shape[1] = width,ssssssssssssss
        # using datetime to get date/time stamp, for font positions using frame.shape() wich returns a tuple of (rows,columns,channels)
        # going 10 accross in rows/width so need columns with frame.shape()[0] we are selecting columns so how ever many pixel height
        # the image is - 10 so oppisite end at bottom instead of being at the top like the other text

        cv2.imshow('Security Feed', frame)
        cv2.imshow('frame_delta', frame_delta)
        cv2.imshow('Frame_thresh_adaptative', thresh_adaptative)
        cv2.imshow('Frame_dilate', dilate_image)
        cv2.imshow('Frame_opened_image', opened_image)
        key = cv2.waitKey(1) & 0xFF # (1) = time delay in seconds before execution, and 0xFF takes the last 8 bit to check value or sumin
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

        first_frame = greyscale_image
        time.sleep(0.5)

        _temps_maintenant = datetime.now()
        difference = (_temps_maintenant - _temps_lancement).total_seconds()

    video_capture.release()
    return activityFactor

if __name__=='__main__':
    print(str(motion_detection(35)))
