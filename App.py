import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import time
import json
import datetime
from frame_divider import divide_video
from process_video import process_videos_with_threading
from plot_data import plot_class_and_general_stats


class VideoProcessingApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Video Processing App")
        self.master.geometry("1000x680")  # Window size

        custom_font = ("Roboto", 11)  # Desired size and font

        # Frame for controls on the top
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(pady=20)

        # Frame for the first row
        self.row1_frame = tk.Frame(self.top_frame)
        self.row1_frame.pack(anchor="w", pady=10)
        self.label = tk.Label(self.row1_frame, text="Selecciona el video a procesar:", font=custom_font)
        self.label.pack(side="left", padx=(30, 10))
        self.video_path_entry = tk.Entry(self.row1_frame, width=50, font=custom_font)
        self.video_path_entry.pack(side="left", padx=(0, 15))
        self.browse_button = tk.Button(self.row1_frame, text="Buscar video", command=self.select_video, font=custom_font)
        self.browse_button.pack(side="left")

        # Frame for the second row
        self.row2_frame = tk.Frame(self.top_frame)
        self.row2_frame.pack(anchor="w", pady=10)
        self.parts_label = tk.Label(self.row2_frame, text="¿En cuantas partes quieres dividir?", font=custom_font)
        self.parts_label.pack(side="left", padx=(30, 10))
        self.num_parts_entry = tk.Entry(self.row2_frame, width=10, font=custom_font)
        self.num_parts_entry.pack(side="left", padx=10)

        # Frame for the process button
        self.process_button_frame = tk.Frame(self.top_frame)
        self.process_button_frame.pack(anchor="center", pady=20)
        self.process_button = tk.Button(self.process_button_frame, text="Procesar", width=15, height=1, command=self.process_video, font=custom_font)
        self.process_button.pack()

        # Frame for the messages
        self.message_frame = tk.Frame(self.top_frame)
        self.message_frame.pack(anchor="center", pady=10)
        self.processing_label = tk.Label(self.message_frame, text="", font=custom_font)
        self.processing_label.pack()

        # Frame for results
        self.results_frame = tk.Frame(master)
        self.results_frame.pack(pady=20)

        self.image_labels = []  # List to store references to image labels

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            self.video_path_entry.delete(0, tk.END)
            self.video_path_entry.insert(0, file_path)

    def process_video(self):
        file_path = self.video_path_entry.get()
        if not file_path:
            self.processing_label.config(text="Error: Debes seleccionar un video.")
            return

        num_parts_str = self.num_parts_entry.get()
        if not num_parts_str.isdigit():
            self.processing_label.config(text="Error: Debes ingresar un número válido de partes.")
            return
        num_parts = int(num_parts_str)

        # Disable text fields and process button
        self.video_path_entry.config(state="disabled")
        self.browse_button.config(state="disabled")
        self.num_parts_entry.config(state="disabled")
        self.process_button.config(state="disabled")

        self.processing_label.config(text="Procesando video... Por favor, espera.")
        self.master.update() # Update interface to display the message

        # Process video in a separate thread (sino se pega)
        processing_thread = threading.Thread(target=self.process_video_thread, args=(file_path, num_parts))
        processing_thread.start()

    def process_video_thread(self, file_path, num_parts):
        # Start timing
        start_time = time.time()

        # Divide video into parts
        divided_videos = divide_video(file_path, num_parts)

        # Process video parts using threading
        results_dict = process_videos_with_threading(divided_videos)

        # Save results to a temporary JSON file
        temp_json_path = "temp_results.json"
        with open(temp_json_path, 'w') as json_file:
            json.dump(results_dict, json_file)

        # Show completion message
        self.processing_label.config(text="¡Procesamiento completado!")

        # Calculate and print the execution time in hours
        end_time = time.time()
        exec_time_seconds = end_time - start_time
        exec_time_hours = exec_time_seconds / 3600
        print(f"Execution time: {exec_time_hours} hours")

        # Enable text fields and process button again
        self.video_path_entry.config(state="normal")
        self.browse_button.config(state="normal")
        self.num_parts_entry.config(state="normal")
        self.process_button.config(state="normal")

        # Call plot_and_show_results in the main thread
        self.master.after(0, self.plot_and_show_results, temp_json_path)

    def plot_and_show_results(self, json_path):
        # Read JSON file
        with open(json_path, 'r') as json_file:
            results_dict = json.load(json_file)

        # Call plot_class_and_general_stats in the main thread
        plot_class_and_general_stats(results_dict)

        # Show result images
        self.show_results(json_path)

    def show_results(self, json_path):
        base_name = os.path.splitext(os.path.basename(json_path))[0]

        # Extract original video file name
        video_name = os.path.splitext(os.path.basename(self.video_path_entry.get()))[0]

        stats_folder = os.path.join("detections", video_name, datetime.datetime.now().strftime('%Y-%m-%d'), "stats")

        print(f"Buscando imágenes en: {stats_folder}")  # stats directory path

        if os.path.exists(stats_folder):
            for widget in self.image_labels:
                widget.destroy()
            self.image_labels = []

            images = [f for f in os.listdir(stats_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if not images:
                print("No se encontraron imágenes en el directorio de estadísticas.")

            row = 0
            column = 0
            max_columns = 4  # Maximum number of columns

            for i, image_file in enumerate(images):
                img_path = os.path.join(stats_folder, image_file)
                print(f"Cargando imagen: {img_path}")  # path of each image

                try:
                    img = Image.open(img_path)
                    img = img.resize((200, 150), Image.LANCZOS)  # Resize image
                    img = ImageTk.PhotoImage(img)

                    label = tk.Label(self.results_frame, image=img)
                    label.image = img  # Save reference to avoid garbage collection
                    label.grid(row=row, column=column, padx=5, pady=5)
                    self.image_labels.append(label)

                    column += 1
                    if column >= max_columns:
                        column = 0
                        row += 1
                except Exception as e:
                    print(f"Error al cargar la imagen {img_path}: {e}")


def main():
    root = tk.Tk()
    VideoProcessingApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
