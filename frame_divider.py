import os
import cv2
import tempfile


def divide_video(video_path, num_parts):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the number of frames per part
    frames_per_part = total_frames // num_parts

    # Create a list to store paths of temporary video files
    temp_video_files = []

    # Create a list to store VideoWriter objects
    video_writers = []



    # Create a VideoWriter object for each part
    for i in range(num_parts):

        # Get the filename
        filename = video_path.split("/")[-1].split(".")[0]

        # Create a temporary video file
        temp_file = tempfile.NamedTemporaryFile(suffix=f'-{filename}_{i + 1}.avi', delete=False)
        temp_file.close()  # Close the file so it can be written to

        # Append the path of the temporary file to the list
        temp_video_files.append(temp_file.name)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(temp_file.name, fourcc, cap.get(cv2.CAP_PROP_FPS),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # Write the VideoWriter object to a list
        video_writers.append(out)

    # Iterate through the video frames
    current_part = 0
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Write the frame to the current part
        video_writers[current_part].write(frame)

        # Move to the next part if necessary
        frame_count += 1
        if frame_count >= frames_per_part:
            frame_count = 0
            current_part += 1
            if current_part >= num_parts:
                break

    # Release VideoCapture and VideoWriter objects
    cap.release()
    for out in video_writers:
        out.release()

    print(f"Video divided into {num_parts} parts successfully.")

    # Return the list of temporary video file paths
    return temp_video_files


# Example usage:
divided_video_paths = divide_video("videos/full/Antifragile.mp4", 4)
print("Divided video paths:", divided_video_paths)
