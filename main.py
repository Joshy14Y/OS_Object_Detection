import time
from frame_divider import divide_video
from process_video import process_videos_with_threading
from plot_data import plot_class_and_general_stats

def main(video_path, num_parts):

    # Start timing
    start_time = time.time()

    # Divide the video into parts
    divided_videos = divide_video(video_path, num_parts)

    # Process the divided videos using threading
    results_dict = process_videos_with_threading(divided_videos)

    # Plot the results
    plot_class_and_general_stats(results_dict)

    # Calculate and print the execution time in hours
    end_time = time.time()
    exec_time_seconds = end_time - start_time
    exec_time_hours = exec_time_seconds / 3600
    print(f"Execution time: {exec_time_hours} hours")

if __name__ == '__main__':
    main("videos/full/Antifragile.mp4", 16)