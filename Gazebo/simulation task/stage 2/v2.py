import numpy as np
import cv2

# Open the default camera
video_capture = cv2.VideoCapture(0)

while True:
    # Capture the frames
    ret, frame = video_capture.read()

    # Crop the image
    xframe = 1920
    yframe = 1080
    crop_img = frame[0:yframe, 0:xframe]

    # Display the original frame
    cv2.imshow('Original Frame', crop_img)
    cv2.waitKey(1)

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Display the grayscale frame
    cv2.imshow('Grayscale Frame', gray)
    cv2.waitKey(1)

    # Median blur
    blur = cv2.medianBlur(gray, 37)

    # Display the blurred frame
    cv2.imshow('Blurred Frame', blur)
    cv2.waitKey(1)

    # Apply morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel, iterations=4)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=4)

    # Display the morphological operations frame
    cv2.imshow('Morphological Operations Frame', closing)
    cv2.waitKey(1)

    # Color thresholding
    ret, thresh = cv2.threshold(closing, 60, 255, cv2.THRESH_BINARY_INV)

    # Display the thresholded frame
    cv2.imshow('Thresholded Frame', thresh)
    cv2.waitKey(1)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Get the left and right boundaries of the white line segment
        left_boundary = min(cnt[0][0][0] for cnt in contours if len(cnt) > 0)
        right_boundary = max(cnt[0][0][0] for cnt in contours if len(cnt) > 0)

        cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

        # print(f"Left Boundary: {left_boundary}, Right Boundary: {right_boundary}")

        # Check if the center falls within the boundaries or on the left/right side
        if xframe/2 >= left_boundary and xframe/2 <= right_boundary:
            print("On Track!")
        elif xframe/2 < left_boundary:
            print("Move Right!")
        else:
            print("Move Left!")
    else:
        print("I don't see the line")

    # Display the resulting frame
    cv2.imshow('Processed Frame', crop_img)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()