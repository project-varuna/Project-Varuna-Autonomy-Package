import customtkinter as ctk
import tkinter as tk  # Needed for some underlying functionalities
from modeling import Modeling
from planning_controls import Planning_Controls
from deploy import Deploy
import signal
import sys

def signal_handler(sig, frame):
    print('Closing the application...')
    app.quit()  # Close the Tkinter window
    sys.exit(0)  # Exit the program

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Project Varuna MMPK GUI Client")

        # Allow the window to resize automatically based on content
        self.resizable(True, True)  # Allow window to be resized

        # Set the appearance mode and color theme
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        # Container to stack frames on top of each other
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        # Configure the grid system
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the frames
        self.frames = {}
        # Main dictionary to store values from GUI
        self.args_dict = {'Modeling':{},'Planning_Controls':{},'Deploy':{}}

        for F in (Modeling, Planning_Controls,Deploy):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # Place all frames in the same location; the one on top will be visible
            frame.grid(row=0, column=0, sticky="nsew")

        # Initially show the "Modeling" frame
        self.show_frame("Modeling")

        # Update the window size to fit content
        self.update_idletasks()  # Updates the geometry of the window to fit content

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        return frame

        # Ensure window resizes to fit new frame content
        self.update_idletasks()  # Adjusts window size when switching frames


if __name__ == "__main__":
    app = App()
    # Set up the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    app.mainloop()
