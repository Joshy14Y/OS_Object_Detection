import json
import os.path

import matplotlib.pyplot as plt
import numpy as np
import os

def plot_general_stats(classes, counts, mean_confidences, path):

    split_path = os.path.splitext(os.path.basename(path))[0].split("-")[-1]
    title = f'{split_path} Class Counts and Mean Confidence'

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Class')
    ax1.set_ylabel('Counts', color=color)
    ax1.bar(classes, counts, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Mean Confidence', color=color)
    ax2.plot(classes, mean_confidences, color=color, marker='o')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Print statistics
    print(f"\n{title}")
    for class_name, count in zip(classes, counts):
        index = classes.index(class_name)  # Get the index of the class name
        mean_confidence = mean_confidences[index]  # Get the mean confidence using the index
        print(f"{class_name}: Count - {count}, Mean Confidence - {mean_confidence}")

def plot_class_and_general_stats(json_data):
    class_stats = {}
    all_class_counts = {}
    all_class_confidences = {}

    # Iterate over each video
    for video, frames in json_data.items():
        class_counts = {}
        class_confidences = {}

        # Iterate over frames in the video
        for frame_info in frames.values():
            detections = frame_info['Detections']
            for detection in detections:
                class_name = detection['Class']
                confidence = detection['Confidence']

                # Update class counts
                if class_name in class_counts:
                    class_counts[class_name] += 1
                    class_confidences[class_name].append(confidence)
                else:
                    class_counts[class_name] = 1
                    class_confidences[class_name] = [confidence]

                # Update overall class counts
                if class_name in all_class_counts:
                    all_class_counts[class_name] += 1
                    all_class_confidences[class_name].append(confidence)
                else:
                    all_class_counts[class_name] = 1
                    all_class_confidences[class_name] = [confidence]

        # Calculate mean confidence for each class in the video
        class_mean_confidence = {class_name: np.mean(confidences) for class_name, confidences in class_confidences.items()}

        # Store class stats in dictionary
        class_stats[video] = {'counts': class_counts, 'mean_confidence': class_mean_confidence}

        # Plot bar plot for each video
        classes = list(class_counts.keys())
        counts = list(class_counts.values())
        mean_confidences = [class_mean_confidence[class_name] for class_name in classes]

        plot_general_stats(classes, counts, mean_confidences, video)

    # Calculate mean confidence for each class across all videos
    all_class_mean_confidence = {class_name: np.mean(confidences) for class_name, confidences in all_class_confidences.items()}

    # Plot bar plot for general statistics
    classes = list(all_class_counts.keys())
    counts = list(all_class_counts.values())
    mean_confidences = [all_class_mean_confidence[class_name] for class_name in classes]

    plot_general_stats(classes, counts, mean_confidences, 'General')

    return class_stats


if __name__ == "__main__":
    # Load JSON data
    with open('results.json', 'r') as f:
        data = json.load(f)

    # Call the function
    class_stats = plot_class_and_general_stats(data)
