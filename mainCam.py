from adafruit_motorkit import MotorKit
import cv2
import numpy as np

# Initialize MotorKit
kit = MotorKit()

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from the webcam
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Define a region of interest (ROI) to focus on the lane
    roi_vertices = np.array([[(0, frame.shape[0]), (frame.shape[1] // 2, frame.shape[0] // 2),
                              (frame.shape[1], frame.shape[0])]], dtype=np.int32)
    roi_edges = cv2.fillPoly(np.zeros_like(edges), roi_vertices, 255)
    roi = cv2.bitwise_and(edges, roi_edges)

    # Apply Hough transform to detect lines in the ROI
    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=30)

    # If lines are detected, calculate average slope and intercept
    if lines is not None:
        slopes = []
        intercepts = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            slopes.append(slope)
            intercepts.append(intercept)

        average_slope = np.mean(slopes)
        average_intercept = np.mean(intercepts)

        # Calculate the x-coordinate of the bottom of the frame (where the robot is)
        y_bottom = frame.shape[0]
        x_bottom = int((y_bottom - average_intercept) / average_slope)

        # Control the motors based on the lane position
        motor_speed = (x_bottom - frame.shape[1] // 2) / (frame.shape[1] // 2)

        # Forward and backward motion
        kit.motor1.throttle = 0.5 + motor_speed
        kit.motor2.throttle = 0.5 + motor_speed

        # Rotate motion
        rotate_speed = 0.2
        kit.motor3.throttle = rotate_speed * motor_speed

    else:
        # If no lines are detected, stop the motors
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0

    # Display the frame
    cv2.imshow("Frame", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
