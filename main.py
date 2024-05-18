import tkinter as tk
from App import VideoProcessingApp

def main():
    root = tk.Tk()
    app = VideoProcessingApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
