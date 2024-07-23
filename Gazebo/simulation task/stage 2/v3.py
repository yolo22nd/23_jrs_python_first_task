import numpy as np
import cv2

video_capture = cv2.VideoCapture('changed.mp4')
# video_capture.set(3, 160)
# video_capture.set(4, 120)


video_capture.set(3, 1912)
video_capture.set(4, 850)

while True:
    # Capture the frames
    ret, frame = video_capture.read()

    totalx=1912
    totaly=850
    xframe = 1912//2
    yframe = 850
    # Crop the image
    # crop_img = frame[0:4000, 250:4000]
    crop_img = frame[0:yframe, xframe//2: 3* xframe//2]


    # Display the original frame
    # cv2.imshow('Original Frame', crop_img)
    # cv2.waitKey(1)

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the grayscale frame
    # cv2.imshow('Grayscale Frame', gray)
    # cv2.waitKey(1)

    # Median blur
    blur = cv2.medianBlur(gray, 37)


    # Display the blurred frame
    # cv2.imshow('Blurred Frame', blur)
    # cv2.waitKey(1)

    # Apply morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel, iterations=4)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=4)



    # Display the morphological operations frame
    # cv2.imshow('Morphological Operations Frame', closing)
    # cv2.waitKey(1)

    # Color thresholding
    ret, thresh = cv2.threshold(closing, 60, 255, cv2.THRESH_BINARY_INV)



    # Display the thresholded frame
    # cv2.imshow('Thresholded Frame', thresh)
    # cv2.waitKey(1)

    # Find the contours of the frame
    # contours, hierarchy = cv2.findContours(thresh_crop.copy(), 1, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)


        # Get the bounding rectangle of the largest contour
        x, y, w, h = cv2.boundingRect(c)
        # print(x,y,w,h)
        # the frame is indexed from top left!!!
        left_boundary = x
        right_boundary = x + w
        down_boundary = y + h
        up_boundary = y

        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.line(crop_img, (cx, 0), (cx, yframe), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (xframe, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img, [c], -1, (0, 255, 0), 1)

        # cv2.line(frame, (cx, 0), (cx, 720), (255, 0, 0), 1)
        # cv2.line(frame, (0, cy), (1280, cy), (255, 0, 0), 1)
        # cv2.drawContours(frame, [c], -1, (0, 255, 0), 1)


        print(f"Left Boundary: {left_boundary}, Right Boundary: {right_boundary}")
        print(f"up Boundary: {up_boundary}, down Boundary: {down_boundary}")
        print("cx: ", cx, "cy: ", cy)

        # Check if the line segment is in the bottom 30% of the frame
        upper_80_percent = yframe * 0.8
        upper_70_percent = yframe * 0.7
        upper_60_percent = yframe * 0.6
        upper_10_percent = yframe * 0.1
        # if up_boundary < bottom_40_percent:
        #     # Initiate turning event
        #     if cx < xframe / 2:
        #         print("Rotate Left!")
        #     else:
        #         print("Rotate Right!")
        # else:
        #     # Check if the center falls within the boundaries or on the left/right side
        #     if up_boundary < yframe / 2:
        #         # Line segment is below half the frame, slow down
        #         print("Slow Down!")
        #     elif xframe / 2 >= left_boundary and xframe / 2 <= right_boundary:
        #         print("On Track!")
        #     elif xframe / 2 < left_boundary:
        #         print("Move Right!")
        #     else:
        #         print("Move Left!")
        # Check if the centroid is too far to the left or right

        # Initiate turning event
        if cy > upper_60_percent:
            if cx < xframe * 0.4:
                print("Rotate left!")
            elif cx > xframe *0.6:
                print("Rotate right!")
            else:
                print("rotate cx thingy thing")
        # Check if the bounding rectangle occupies a large portion of the frame
        elif up_boundary > upper_10_percent:
            print("approching turn!")
        # Check if the centroid is slightly off to the left or right
        elif cx < xframe * 0.4:
            print("Move left!")
        elif cx > xframe * 0.6:
            print("Move right!")
        else:
            print("On Track!")

    else:
        print("I don't see the line")


    # Display the resulting frame
    cv2.imshow('Processed Frame', crop_img)
    # cv2.imshow('Processed Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()