import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import threading
import subprocess

class FileSelectorGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("ResearchSat Spore Counter")
        self.center_window(self.master, 700, 305)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self, text="ResearchSat Spore Counter", font=("TkDefaultFont", 24))
        self.title_label.pack(pady=10)

        # Weights
        self.frame1 = tk.Frame(self)
        self.frame1.pack(pady=10)

        self.weights_path_label = tk.Label(self.frame1, text="Custom Trained Weights: ")
        self.weights_path_label.pack(side="left")

        self.weights_path_value = tk.Label(self.frame1, text="")
        self.weights_path_value.pack(side="left")

        self.weights_path_button = tk.Button(self.frame1, text="Select Weights File", command=self.select_weights)
        self.weights_path_button.pack(side="left")

        # Image
        self.frame2 = tk.Frame(self)
        self.frame2.pack(pady=10)

        self.image_path_label = tk.Label(self.frame2, text="Image: ")
        self.image_path_label.pack(side="left")

        self.image_path_value = tk.Label(self.frame2, text="")
        self.image_path_value.pack(side="left")

        self.image_path_button = tk.Button(self.frame2, text="Select Image File", command=self.select_image)
        self.image_path_button.pack(side="left")

        # Run button
        self.frame3 = tk.Frame(self)
        self.frame3.pack(pady=10)

        self.run_button = tk.Button(self.frame3, text="Count spores", command=self.count_spores)
        self.run_button.pack(side="left")

        # Spores counted label and value
        self.frame4 = tk.Frame(self)
        self.frame4.pack(pady=10)

        self.spores_counted_label = tk.Label(self.frame4, text="Spores counted: ")
        self.spores_counted_label.pack(side="left")

        self.spores_counted_value = tk.Label(self.frame4, text="")
        self.spores_counted_value.pack(side="left")

        # Quit and help buttons
        self.frame5 = tk.Frame(self)
        self.frame5.pack(pady=10)

        self.quit_button = tk.Button(self.frame5, text=" Quit ", fg="red", command=self.master.destroy)
        self.quit_button.pack(side="left")

        self.help_button = tk.Button(self.frame5, text=" Help ", fg="black", command=self.help)
        self.help_button.pack(side="left")
        self.quit_button.pack(side="left", padx=(0, 10))
        self.help_button.pack(side="left", padx=(10, 0))

    def center_window(self, window, window_width, window_height):
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate x and y coordinates for the window
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def select_weights(self):
        filepath = filedialog.askopenfilename()
        if filepath.endswith(".pt"):
            self.weights_path_value.config(text=filepath)
        else:
            self.show_error_message("Error: Invalid file type (weights file must be '.pt')")

    def select_image(self):
        filepath = filedialog.askopenfilename()
        if filepath.endswith(".jpg") or filepath.endswith(".JPG"):
            self.image_path_value.config(text=filepath)
        else:
            self.show_error_message("Error: Invalid file type (image file must be '.jpg' or '.JPG')")

    def help(self):
        help_window = tk.Toplevel(self.master)
        help_window.title("Help")
        self.center_window(help_window, 450, 300)

        title_label = tk.Label(help_window, text="Spore Counter Tool Information:", font=("TkDefaultFont", 14))
        title_label.pack(pady=4)

        # Welcome
        welcome_frame = tk.Frame(help_window)
        welcome_frame.pack(pady=4)
        # welcome_frame.pack(fill='both', expand=True)
        welcome_label = tk.Label(welcome_frame, text="Welcome to the ResearchSat Spore Counter Tool.")
        welcome_label.pack(side="left", pady=4)

        # Steps
        help_frame = tk.Frame(help_window)
        help_frame.pack(fill='both', expand=True)
        help_label = tk.Label(help_frame, text="How to use:\n\n"
                              + "1. Select a custom weights file (trained to recognise spores in an image)\n"
                                 + "        - found in " + r"yolov7_package\runs\train\yolov713\weights" + "\n"
                                 + "        - 'best.pt' is recommended\n"
                                 + "2. Select the image you want to analyse\n"
                                 + "3. Click 'Count Spores' to run the detection algorithm\n"
                                 + "4. The number of spores identified in the image updates\n"
                                 + "5. The analysed image is saved to " + r"yolov7_package\runs\detect\expXX*" + "\n\n"
                                 + "*The XX number will change depending on the number of times the detect\n"
                                  + "algorithm has run already. To view your most recent detection, just\n"
                                  + "choose the most recent exp folder.", justify="left")
        help_label.pack(pady=4)

    def show_error_message(self, message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Error")
        self.center_window(error_window, 310, 100)
        error_label = tk.Label(error_window, text=message, fg="red")
        error_label.pack(pady=10)

        # Quit button
        quit_button = tk.Button(error_window, text="   Ok   ", fg="black", command=error_window.destroy)
        quit_button.pack(side="bottom", pady=10)

    def count_spores(self):
        if self.weights_path_value.cget("text") == "" or self.image_path_value.cget("text") == "":
            self.show_error_message("Error: Weights file and/or image file not specified")
        else:
            loading_bar_window = tk.Toplevel(self.master)
            loading_bar_window.title("Loading")
            self.center_window(loading_bar_window, 300, 50)
            loading_bar = tk.ttk.Progressbar(loading_bar_window, orient="horizontal", length=280, mode="indeterminate")
            loading_bar.pack(pady=10)
            loading_bar.start()

            def run_detect():
                # Call spore counting script
                command = "python detect.py --weights " + self.weights_path_value.cget("text") + " --source " + self.image_path_value.cget("text")
                subprocess.call(command)

                # Get the spore count from the log file
                dictionary = {}
                with open("log.txt", "r") as file:
                    for line in file:
                        key, value = line.strip().split(" ")
                        dictionary[key] = int(value)

                # Stop loading bar and close window
                loading_bar.stop()
                loading_bar_window.destroy()

                # Update spores counted label
                self.spores_counted_value.config(text=dictionary[self.image_path_value.cget("text").split("/")[-1]])

            # Start the detect.py script in a new thread
            t = threading.Thread(target=run_detect)
            t.start()

            # Update the loading bar window while the script is running
            while t.is_alive():
                loading_bar_window.update()
            
            # # Update spores counted label
            # self.spores_counted_value.config(text=0)

if __name__ == '__main__':
    root = tk.Tk()
    app = FileSelectorGUI(master=root)
    app.mainloop()