import cv2
import numpy as np

looming = 0
looming_text = ""
moving_text = ""
location_text = ""
looming_started = False


left_speed = 0
right_speed = 0

def nothing(x):
    pass

# Make seperate window for HSV sliders 
# Hue, Saturation, Value

cv2.namedWindow('Trackbars')

cv2.createTrackbar("c range", "Trackbars", 0, 10, nothing)

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

# Start Video Cap

cap = cv2.VideoCapture(0)

cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

while True:
    _, frame = cap.read()

    # Blur the frame with gaussian noise

    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([38, 86, 0])
    upper_blue = np.array([121, 255, 255])
   
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    # enable to select color from slider
    # lower_bound = np.array([l_h, l_s, l_v])
    # upper_bound = np.array([u_h, u_s, u_v])

    lower_bound = np.array([28, 85, 114])
    upper_bound = np.array([179, 255, 255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    largest_area = 0

    # Checks to make sure there are contours before traversing
    if len(contours) > 0:
        largest_contour = contours[0]
    # Goes through each contour and selects the largest
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_contour = contour

        # Findin center point of largest contour

        center = cv2.moments(largest_contour)

        if center["m00"] > 0:
            center_x = int(center["m10"] / center["m00"])
            center_y = int(center["m01"] / center["m00"])

            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            if center_x < (cap_width/5):
                location_text = "Left Zone"
                left_speed = 0.5
                right_speed = 1
            elif center_x > (cap_width/5) and center_x < (cap_width/5 * 2):
                location_text = "Mid-Left Zone"
                left_speed = 0.8
                right_speed = 1
            elif center_x > (cap_width/5 * 2) and center_x < (cap_width/5 * 3):
                location_text = "Middle Zone"
                left_speed = 1
                right_speed = 1
            elif center_x > (cap_width/5 * 3) and center_x < (cap_width/5 * 4):
                location_text = "Mid-Right Zone"
                left_speed = 1
                right_speed = 0.8
            else:
                location_text = "Right Zone"
                left_speed = 1
                right_speed = 0.5

    area_text = "Area = " + str(largest_area) + " pixels"



    if looming_started == True and (largest_area+begining_area) != 0:
        looming = (largest_area - begining_area)/(2*((largest_area + begining_area)/2))
        looming_text = "Looming from spacebar action = " + str(looming)
        if looming < -0.05:
            moving_text = "Move Forward"
            # robot.left(speed=left_speed)
            # robot.right(speed=right_speed)
        elif looming > 0.05:
            moving_text = "Move Backward"
            # robot.left(speed=left_speed * -1)
            # robot.right(speed=right_speed * -1)
        else:
            moving_text = "Stay"
            # robot.stop()


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

    

    cv2.drawContours(frame, largest_contour, -1, (0, 255, 0), 3)
        
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    # cv2.imshow("Blur", blurred_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
