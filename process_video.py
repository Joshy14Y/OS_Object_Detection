import cv2
from ultralytics import YOLO
from threading import Thread
import os
import json


def thread_safe_predict(video_path):
    # Load the YOLOv8 model
    local_model = YOLO("weights/train18/weights/best.pt")

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get frames per second (FPS) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Initialize frame counter
    frame_number = 0

    # Get video filename without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0].split("-")[-1]
    file_name = video_name.split("_")[0]

    # Create directory to save detections for this video
    detection_dir = f"detections/{file_name}/{video_name}"
    os.makedirs(detection_dir, exist_ok=True)

    # Dictionary with info:
    analysis_info = {}

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Increment frame number
            frame_number += 1

            results = local_model.predict(source=frame, stream=False, save=False, imgsz=640, conf=0.75, half=True,
                                          device="0", verbose=False)

            names = results[0].names
            box = results[0].boxes.cpu()
            conf = box.conf.tolist()
            cls = box.cls.tolist()

            if len(conf) > 0:
                # Create a list of dictionaries for detections
                detections = []
                for cf, cl in zip(conf, cls):
                    detection = {
                        "Class": names.get(cl, "Unknown"),
                        "Confidence": cf
                    }
                    detections.append(detection)

                analysis_info[frame_number] = {
                    "Filename": video_path,
                    "Frame Number": frame_number,
                    "Frame Time (s)": frame_number / fps,
                    "Detections": detections
                }

                annotated_frame = results[0].plot()

                # Save the frame to a file
                frame_filename = os.path.join(detection_dir, f"frame_{frame_number}.jpg")
                cv2.imwrite(frame_filename, annotated_frame)
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    # Return the analysis_info dictionary
    return analysis_info

    # results = local_model.predict(source=video_path, stream=True, save=True, imgsz=640, conf=0.75, half=True, device="0", verbose=False)
    # for r in results:
    #     box = r.boxes.cpu()
    #     conf = box.conf
    #     cls = box.cls
    #     dict = r.names
    #     np = r.verbose()
    #     if conf.numel() > 0:
    #         print(f"Conf: {conf}, Class: {cls}")
    #         print(f"Hello:{np}")


# Define function to process videos using threading
def process_videos_with_threading(video_paths):

    # Dictionary to store results for each video
    results_dict = {}

    # Process each video in a separate thread
    threads = []
    for video_path in video_paths:
        thread = Thread(target=lambda path: results_dict.update({path: thread_safe_predict(path)}), args=(video_path,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Return the results dictionary
    return results_dict


# Example usage:
if __name__ == "__main__":
    # List of video paths
    video_paths = ["videos/divided/part_1.avi", "videos/divided/part_2.avi", "videos/divided/part_3.avi",
                   "videos/divided/part_4.avi"]

    # Process videos using threading
    results = process_videos_with_threading(video_paths)

    # Save the results dictionary as JSON
    with open("results.json", "w") as json_file:
        json.dump(results, json_file)

    print("Results saved as JSON.")