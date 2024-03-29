import cv2
import numpy as np
from jetbot import Robot
from PIL import Image

robot = Robot()
robot.stop()


# Pointer to the on-board camera
def gstreamer_pipeline(
   capture_width=400,
   capture_height=300,
   display_width=800,
   display_height=600,
   framerate=24,
   flip_method=0,
):
   return (
      "nvarguscamerasrc ! "
      "video/x-raw(memory:NVMM), "
      "width=(int)%d, height=(int)%d, "
      "format=(string)NV12, framerate=(fraction)%d/1 ! "
      "nvvidconv flip-method=%d ! "
      "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
      "videoconvert ! "
      "video/x-raw, format=(string)BGR ! appsink"
      % (
         capture_width,
         capture_height,
         framerate,
         flip_method,
         display_width,
         display_height,
      )
   )

left_speed = 0
right_speed = 0
looming = 0
looming_text = ""
moving_text = ""
location_text = ""
looming_started = False
speed_constant = 1
LEFT = 0
RIGHT = 0
mid_threshold = 0.1
adjust_rate = 0.01
left_adjust = 0
right_adjust = 0

def nothing(x):
    pass

# Make seperate window for HSV sliders 
# Hue, Saturation, Value

cv2.namedWindow('Trackbars')

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

# Start Video Cap

cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture(0)

cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    _, frame = cap.read()

    # Blur the frame with gaussian noise

    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
   
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    # enable to select color from slider
    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    # color for JETBOT
    # lower_bound = np.array([79, 108, 44])
    # upper_bound = np.array([153, 255, 255])   

    # color for WINDOWS
    # lower_bound = np.array([28, 85, 114])
    # upper_bound = np.array([179, 255, 255])
    # lower_bound = np.array([91, 80, 66])
    # upper_bound = np.array([166, 255, 255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    largest_area = 0
    largest_contour = 0

    # Checks to make sure there are contours before traversing
    if len(contours) > 0:
        largest_contour = contours[0]
    # Goes through each contour and selects the largest
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_contour = contour

        # Finding center point of largest contour

        center = cv2.moments(largest_contour)
        
        if center["m00"] > 0:
            center_x = int(center["m10"] / center["m00"])
            center_y = int(center["m01"] / center["m00"])

            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            center_error = np.interp(center_x,[0,cap_width],[-1,1])                     # Set center_error to range mapped to center_x position in frame




    area_text = "Area = " + str(largest_area) + " pixels"



    if looming_started == True and (largest_area+begining_area) != 0:
        looming = (largest_area - begining_area)/(2*((largest_area + begining_area)/2))
        looming_text = "Looming from spacebar action = " + str(looming)
        LEFT = speed_constant * looming * -1
        RIGHT = speed_constant * looming * -1

        if center_error < mid_threshold * -1:
            left_adjust -= adjust_rate * center_error * -1
            right_adjust += adjust_rate * center_error * -1
        elif center_error > mid_threshold:
            left_adjust += adjust_rate * center_error
            right_adjust -= adjust_rate * center_error
        else:
            left_adjust = 0
            right_adjust = 0

        LEFT += left_adjust
        RIGHT += right_adjust

        if LEFT > 1:
            LEFT = 1
        elif LEFT < -1:
            LEFT = -1
        if RIGHT > 1:
            RIGHT = 1
        elif RIGHT < -1:
            RIGHT = -1

        if largest_area > area_threshold:
            robot.left_motor.value = LEFT
            robot.right_motor.value = RIGHT
        else:
            robot.left_motor.value = 0
            robot.right_motor.value = 0

        if looming < -0.05:
            # robot.left_motor.value = left_speed * speed_constant
            # robot.right_motor.value = right_speed * speed_constant

            moving_text = "Move Forward: Left: " + str(LEFT) + " , Right: " + str(RIGHT)
        elif looming > 0.05:
            # robot.right_motor.value = left_speed * speed_constant * -1
            # robot.left_motor.value = right_speed * speed_constant * -1

            moving_text = "Move Backward: Left" + str(LEFT) + ", Right " + str(RIGHT)
        else:
            # robot.left_motor.value = 0
            # robot.right_motor.value = 0

            moving_text = "Stay: Left" + str(LEFT) + ", Right " + str(RIGHT)




    if cv2.waitKey(1) == 32:
        looming_text = "Looming from spacebar action = 0"
        begining_area = largest_area
        looming_started = True

    if cv2.waitKey(1) == ord('s'):
        print(f"lower_bound = np.array([{l_h}, {l_s}, {l_v}])")
        print(f"upper_bound = np.array([{u_h}, {u_s}, {u_v}])")

    cv2.putText(img=frame, text=area_text, org=(50, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.4, color=(0, 0, 0),thickness=1)
    cv2.putText(img=frame, text=looming_text, org=(50, 100), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.4, color=(0, 0, 0),thickness=1)
    cv2.putText(img=frame, text=location_text, org=(50, 150), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.4, color=(0, 0, 0),thickness=1)
    cv2.putText(img=frame, text=moving_text, org=(50, 200), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.4, color=(0, 0, 0),thickness=1)

    # Visualize Left and Right wheel speeds

    cv2.line(frame, (50, int(cap_height - 50)), (50, int(cap_height - 150)), (255, 255, 255), thickness=9, lineType=12)
    cv2.line(frame, (100, int(cap_height - 50)), (100, int(cap_height - 150)), (255, 255, 255), thickness=9, lineType=12)

    if LEFT >= 0:
        cv2.line(frame, (50, int(cap_height - 100)), (50, int(cap_height - 100 - (LEFT*50))), (0, 255, 0), thickness=8, lineType=8)
    else:
        cv2.line(frame, (50, int(cap_height - 100)), (50, int(cap_height - 100 - (LEFT*50))), (0, 0, 255), thickness=8, lineType=8)

    if RIGHT >= 0:
        cv2.line(frame, (100, int(cap_height - 100)), (100, int(cap_height - 100 - (RIGHT*50))), (0, 255, 0), thickness=8, lineType=8)
    else:
        cv2.line(frame, (100, int(cap_height - 100)), (100, int(cap_height - 100 - (RIGHT*50))), (0, 0, 255), thickness=8, lineType=8)

    
    if len(contours) > 0:
    	cv2.drawContours(frame, largest_contour, -1, (0, 255, 0), 3)
        
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    # cv2.imshow("Blur", blurred_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()