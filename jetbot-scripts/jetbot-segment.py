
import cv2
import numpy as np
import time
# from jetbot import Robot
# from PIL import Image

# robot = Robot()
# robot.stop()

# speed = 0.3


# Pointer to the on-board camera
# def gstreamer_pipeline(
#    capture_width=100,
#    capture_height=100,
#    display_width=100,
#    display_height=100,
#    framerate=21,
#    flip_method=0,
# ):
#    return (
#       "nvarguscamerasrc ! "
#       "video/x-raw(memory:NVMM), "
#       "width=(int)%d, height=(int)%d, "
#       "format=(string)NV12, framerate=(fraction)%d/1 ! "
#       "nvvidconv flip-method=%d ! "
#       "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
#       "videoconvert ! "
#       "video/x-raw, format=(string)BGR ! appsink"
#       % (
#          capture_width,
#          capture_height,
#          framerate,
#          flip_method,
#          display_width,
#          display_height,
#       )
#    )

# cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)



looming = 0
looming_text = ""
moving_text = ""
looming_started = False
pixel_value = 30



while(True):
    
    (fail, img) = cap.read(0)
    if fail == 0:
        break

    img_gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    x = img_gray_scale<pixel_value
            
    area = np.count_nonzero(x == True)
    b_filtered = np.where(x,0,img[:, :, 0])
    g_filtered = np.where(x,0,img[:, :, 1])
    r_filtered = np.where(x,255,img[:, :, 2])

    merged_filtered = cv2.merge([b_filtered, g_filtered, r_filtered])

    area_text = "Area = " + str(area) + " pixels"

    if looming_started == True and (area+begining_area) != 0:
        looming = (area - begining_area)/(2*((area + begining_area)/2))
        looming_text = "Looming from spacebar action = " + str(looming)
        if looming < 0:
            moving_text = "Move Forward"
            # robot.forward(speed)
        elif looming == 0:
            moving_text = "Stay"
            # robot.stop()
        else:
            moving_text = "Move Backward"
            # robot.backward(speed)


    if cv2.waitKey(1) == 32:
        looming_text = "Looming from spacebar action = 0"
        begining_area = area
        looming_started = True

    cv2.putText(img=merged_filtered, text=area_text, org=(50, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.2, color=(0, 0, 0),thickness=1)
    cv2.putText(img=merged_filtered, text=looming_text, org=(50, 100), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.2, color=(0, 0, 0),thickness=1)
    cv2.putText(img=merged_filtered, text=moving_text, org=(50, 150), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.2, color=(0, 0, 0),thickness=1)


    cv2.imshow("cam", merged_filtered)


    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
cap.release()