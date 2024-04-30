from frame_divider import divide_video
from process_video import process_videos_with_threading
from plot_data import plot_class_and_general_stats

def main(video_path, num_parts):

    # Divide the video into parts
    divided_videos = divide_video(video_path, num_parts)

    # Process the divided videos using threading
    results_dict = process_videos_with_threading(divided_videos)

    plot_class_and_general_stats(results_dict)

if __name__ == '__main__':
    main("videos/full/Antifragile.mp4", 8)