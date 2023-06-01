from Kalman_Filter_Custom_2D import KalmanFilter
from Code.Bounding_Box_Center import get_bounding_box_center_frame
import cv2
import os
from ultralytics import YOLO

# Get the current directory
current_directory = os.getcwd()
print(current_directory)

# Go back to the parent directory
parent_directory = os.path.dirname(current_directory)
print(parent_directory)

# Set input and output directory
video_path = os.path.join(parent_directory, 'Data', 'running_4.mp4')
output_video_path = os.path.join(parent_directory, 'Output', 'running_4_kf.mp4')
print(video_path)

# Instantiate model
weights_path = os.path.join(parent_directory, 'Weights', 'yolov8n.pt')
model = YOLO(weights_path)
names = model.names
print(names)

# Kalman filter parameters
dt = 1/30  # Sampling time = FPS
INIT_POS_STD = 10  # Initial position standard deviation
INIT_VEL_STD = 10  # Initial velocity standard deviation
ACCEL_STD = 40  # Acceleration standard deviation
GPS_POS_STD = 1  # Measurement position standard deviation

# Kalman filter initialization
kf = KalmanFilter(dt, INIT_POS_STD, INIT_VEL_STD, ACCEL_STD, GPS_POS_STD)


# Open the video file
cap = cv2.VideoCapture(video_path)
isFirstFrame = True

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))


while True:
    # Read frame from the video
    ret, frame = cap.read()

    # Break the loop if there are no more frames to read
    if not ret:
        break

    # Create the legend circles
    true_circle_position = (20, 20)
    predict_circle_position = (20, 50)
    update_circle_position = (20, 80)
    circle_radius = 6
    true_circle_color = (0, 255, 0)  # Green color for data
    predict_circle_color = (255, 0, 0)  # Blue color for forecast
    update_circle_color = (0, 0, 255)  # Red color for forecast
    circle_thickness = 2  # Filled circle

    # Draw the legend circles
    cv2.circle(frame, true_circle_position, circle_radius, true_circle_color, circle_thickness)
    cv2.circle(frame, predict_circle_position, circle_radius, predict_circle_color, circle_thickness)
    cv2.circle(frame, update_circle_position, circle_radius, update_circle_color, circle_thickness)

    # Draw the legend
    cv2.putText(frame, "True", (40, 25), cv2.FONT_HERSHEY_SIMPLEX, .5, true_circle_color, 2)
    cv2.putText(frame, "Predict", (40, 55), cv2.FONT_HERSHEY_SIMPLEX, .5, predict_circle_color, 2)
    cv2.putText(frame, "Update", (40, 85), cv2.FONT_HERSHEY_SIMPLEX, .5, update_circle_color, 2)

    # Process the frame to get bounding box centers
    centers = get_bounding_box_center_frame(frame, model, names, object_class='person')

    # Check if center is detected
    if len(centers) > 0:
        center = centers[0]  # Extract the first center tuple

        # Example: Draw circle at the center
        if isinstance(center, tuple):
            print("Center = ", center)
            cv2.circle(frame, center, radius=8, color=(0, 255, 0), thickness=4) # Green

            x_pred, y_pred = kf.predict()
            if isFirstFrame:  # First frame
                x_pred = round(x_pred[0])
                y_pred = round(y_pred[0])
                print("Predicted: ", (x_pred, y_pred))
                isFirstFrame = False
            else:
                x_pred = round(x_pred[0])
                y_pred = round(y_pred[1])
                print("Predicted: ", (x_pred, y_pred))

            cv2.circle(frame, (x_pred, y_pred), radius=8, color=(255, 0, 0), thickness=4) #  Blue

            # Update
            (x1, y1) = kf.update(center)
            x_updt = round(x1[0])
            y_updt =  round(x1[1])
            print("Update: ", (x_updt, y_updt))
            cv2.circle(frame, (x_updt, y_updt), radius=8, color= (0, 0, 255), thickness=4) # Red

    # Write frame to the output video
    out.write(frame)

    # Display the frame with circles
    cv2.imshow("Frame", frame)

    # Wait for the 'q' key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
out.release()
cv2.destroyAllWindows()