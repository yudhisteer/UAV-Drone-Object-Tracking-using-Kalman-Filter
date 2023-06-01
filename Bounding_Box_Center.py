import cv2
from ultralytics import YOLO
import time
import os


def get_bounding_box_center_video(video_path, model, names, object_class):
    cap = cv2.VideoCapture(video_path)
    centers = []
    frame_num = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_num += 1
        results = model(frame)
        person_detected = False

        for result in results:
            detections = []
            print("Frame number: ", frame_num)

            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)

                class_name = names.get(class_id)

                if class_name == object_class and score > 0.5:
                    if not person_detected:
                        person_detected = True
                        detections.append([x1, y1, x2, y2, round(score, 2), class_name])
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        centers.append((center_x, center_y))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

            if not detections:
                centers.append("Not detected")

    cap.release()
    return centers


def get_bounding_box_center_frame(frame, model, names, object_class):
    centers = []
    results = model(frame)
    person_detected = False

    for result in results:
        detections = []

        for r in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)

            class_name = names.get(class_id)

            if class_name == object_class and score > 0.5:
                if not person_detected:
                    person_detected = True
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    centers.append((center_x, center_y))

    if not person_detected:
        centers.append("Not detected")

    return centers






if __name__ == '__main__':
    # Get the current directory
    current_directory = os.getcwd()
    print(current_directory)

    # Go back to the parent directory
    parent_directory = os.path.dirname(current_directory)
    print(parent_directory)

    # Set input and output directory
    video_path = os.path.join(parent_directory, '../Data', 'Occlusion.mp4')
    print(video_path)

    # Instantiate model
    weights_path = os.path.join(parent_directory, '../Weights', 'yolov8n.pt')
    model = YOLO(weights_path)
    names = model.names
    print(names)

    # Example usage:
    bounding_box_centers = get_bounding_box_center_video(video_path)




    # Example usage within the while loop:
    while True:
        ret, frame = VideoCap.read()

        if not ret:
            break

        centers = get_bounding_box_center_frame(frame)

        # Rest of your code...
