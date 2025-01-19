import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import json
import subprocess

class Deploy(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.controller.args_dict['Modeling']['Platform']='F1tenth'

        # configure the grid layout for the main frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        # self.grid_columnconfigure(3, weight=1)
        # self.grid_columnconfigure(4, weight=1)

        # create sidebar frame with widgets
        self.modeling_sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.modeling_sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.modeling_sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.modeling_sidebar_frame, text="Project Varuna", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, command=self.open_directory_selector)
        self.modeling_sidebar_button_1 = ctk.CTkButton(self.modeling_sidebar_frame, text="Modeling",
                       state="disabled",  # Make button non-clickable
                       fg_color="green",   # Set background color
                       text_color="black", # Set text color
                       text_color_disabled="white"
                      )
        self.modeling_sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.modeling_sidebar_button_2 = ctk.CTkButton(self.modeling_sidebar_frame, text="Planning/Controls",
                       state="disabled",  # Make button non-clickable
                       fg_color="green",   # Set background color
                       text_color="black", # Set text color
                       text_color_disabled="white"
                      )

        # self.modeling_sidebar_button_2 = ctk.CTkButton(self.modeling_sidebar_frame)
        self.modeling_sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.modeling_sidebar_button_3 = ctk.CTkButton(self.modeling_sidebar_frame, text="Deploy",
                       state="disabled",  # Make button non-clickable
                       fg_color="#FF9000",   # Set background color
                       text_color="black", # Set text color
                       text_color_disabled="white"
                      )

        # self.modeling_sidebar_button_3 = ctk.CTkButton(self.modeling_sidebar_frame)
        self.modeling_sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(self.modeling_sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.modeling_sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.modeling_sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.modeling_sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Create a frame to hold both buttons
        # self.button_frame = ctk.CTkFrame(master=self)
        # self.button_frame.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        #
        # # Configure the grid layout of the button_frame to make buttons scalable
        # self.button_frame.grid_columnconfigure(0, weight=1)  # Make first column (Previous button) scalable
        # self.button_frame.grid_columnconfigure(1, weight=1)  # Make second column (Proceed button) scalable

        # Previous Button
        self.previous_button = ctk.CTkButton(master=self,
                                             fg_color="blue",  # Default color (red)
                                             hover_color="red",  # Color when hovering (darker red)
                                             text_color="white",  # Text color
                                             text="← Previous",  # Button label
                                             border_width=2,
                                             command=self.previous_page)
        self.previous_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Proceed Button
        self.proceed_button = ctk.CTkButton(master=self,
                                            fg_color="blue",  # Default color (blue)
                                            hover_color="green",  # Color when hovering (green)
                                            text_color="white",  # Text color
                                            text="Run! →",  # Button label
                                            border_width=2,
                                            command=self.next_page)
        self.proceed_button.grid(row=3, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")



        # Create the textbox
        self.modeling_textbox = ctk.CTkTextbox(self, width=150, height=20)
        self.modeling_textbox.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # Insert the text while in normal state
        self.modeling_textbox.insert("0.0", "We're at the final step now! Ready for deploy! \n\n"

                                     "1. **Select reference trajectory from training data**\n"
                                     "   - Simply move the slider and the name of the trajectory will be displayed next to it! \n\n"
                                            
                                     "2. **Choose if the tracking and telemetry data should be saved:**\n"
                                     "   - The user has the option to select either separate topics for throttle and steering or a single topic\n"
                                     "   - If separate topics are selected, they use the Float32 msg type, else we use the Twist message structure.\n\n"

                                     "3. **Review your options from modeling planning and controls on the right pane **\n\n"
               

                                     "4. **Hit run and off we go! **\n\n")
        # Disable the textbox to prevent user editing
        self.modeling_textbox.configure(state="disabled")


        # Save test record and run selection pane
        self.test_record_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.test_record_frame.grid(row=1,column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.test_record_frame.grid_columnconfigure(0, weight=1)
        self.test_record_frame.grid_rowconfigure(4, weight=1)
        self.label_select_traj = ctk.CTkLabel(master=self.test_record_frame, text="Select the trajectory index from test data folder")
        self.label_select_traj.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add Scroll Wheel (Slider) to select from 0 to len of files
        self.test_data_count = 0
        self.scroll_wheel = ctk.CTkSlider(master=self.test_record_frame, from_=0, to=self.test_data_count,
                                          number_of_steps=self.test_data_count)
        self.scroll_wheel.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Display the selected file index

        self.selected_file_label = ctk.CTkLabel(master=self.test_record_frame, text="Selected File Index: 0")
        self.selected_file_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Bind the slider's value change event to update the label
        self.scroll_wheel.bind("<B1-Motion>", self.update_file_label)
        self.controller.args_dict['Deploy']['Traj_index'] = 0

        self.save_data_text = ctk.CTkLabel(self.test_record_frame, text="Save data post deployment?",anchor="w")
        self.save_data_text.grid(row=2, column=0, padx=(0, 20), pady=(10, 10), sticky="ew")
        self.radio_var_save_data = tk.IntVar(value=0)
        # Setup default value
        self.controller.args_dict['Deploy']['Save_data'] = True
        self.radio_button_save_model_yes = ctk.CTkRadioButton(self.test_record_frame, text='Yes', variable=self.radio_var_save_data, value=0, command=self.update_ui_save_data)
        self.radio_button_save_model_yes.grid(row=2, column=1, padx=(0, 10), sticky="w")
        self.radio_button_save_model_no = ctk.CTkRadioButton(self.test_record_frame, text='No', variable=self.radio_var_save_data, value=1, command=self.update_ui_save_data)
        self.radio_button_save_model_no.grid(row=2, column=2, padx=(10, 0), sticky="w")

        self.update_ui_save_data()


        # Create a frame for summary
        self.modeling_summary_frame = ctk.CTkFrame(self)
        self.modeling_summary_frame.grid(row=0, column=3, columnspan=2,padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_modeling_summary = ctk.CTkLabel(master=self.modeling_summary_frame, text="Modeling Summary")
        self.label_modeling_summary.grid(row=0, column=0, padx=10, pady=10, sticky="")
        self.modeling_summary = self.format_dict_for_display(self.controller.args_dict['Modeling'])
        self.modeling_summary_text = ctk.CTkLabel(master=self.modeling_summary_frame, text=self.modeling_summary,
                                                  anchor="w",  # Left-align the text
                                                  justify="left",  # Justify the text to the left to make it look neat
                                                  font=("Arial", 15),  # Set font and size (customize as you like)
                                                  width=600,  # Optional: specify a fixed width to make it look uniform
                                                  height=150,  # Optional: specify a fixed height
                                                  corner_radius=10,  # Optional: round corners for a soft look
                                                  fg_color=("white", "gray25"),  # Background color for light/dark mode
                                                  text_color=("black", "white"),  # Text color for light/dark mode
                                                  padx=10,  # Padding inside the label
                                                  pady=10,  # Padding inside the label
                                                  )
        self.modeling_summary_text.grid(row=1, column=0, padx=10, pady=10, sticky="")
        # self.label_modeling_coming_soon = ctk.CTkLabel(master=self.modeling_summary_frame, text="Coming soon in next v1.0.1 update")
        # self.label_modeling_coming_soon.grid(row=1, column=0, padx=10, pady=10, sticky="")

        # Create a frame for summary
        self.planner_controller_summary_frame = ctk.CTkFrame(self)
        self.planner_controller_summary_frame.grid(row=1, column=3, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_planner_controller_summary = ctk.CTkLabel(master=self.planner_controller_summary_frame, text="Motion Planner -- Controller Summary")
        self.label_planner_controller_summary.grid(row=0, column=0, padx=10, pady=10, sticky="")
        self.planning_control_summary = self.format_dict_for_display(self.controller.args_dict['Planning_Controls'])
        self.planning_control_summary_text = ctk.CTkLabel(
            master=self.planner_controller_summary_frame,
            text=self.planning_control_summary,
            anchor="w",  # Left-align the text
            justify="left",  # Justify the text to the left to make it look neat
            font=("Arial", 15),  # Set font and size (customize as you like)
            width=600,  # Optional: specify a fixed width to make it look uniform
            height=150,  # Optional: specify a fixed height
            corner_radius=10,  # Optional: round corners for a soft look
            fg_color=("white", "gray25"),  # Background color for light/dark mode
            text_color=("black", "white"),  # Text color for light/dark mode
            padx=10,  # Padding inside the label
            pady=10,  # Padding inside the label
        )
        self.planning_control_summary_text.grid(row=1, column=0, padx=10, pady=10, sticky="")
        # self.label_planner_controller_coming_soon = ctk.CTkLabel(master=self.planner_controller_summary_frame, text="Coming soon in next v1.0.1 update")
        # self.label_planner_controller_coming_soon.grid(row=1, column=0, padx=10, pady=10, sticky="")




        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")



    '''Event functions'''

    def test_trajectory_selection_pane(self):
        self.file_list = os.listdir(self.controller.args_dict['Modeling']['Test_data_folder'])
        file_count = len(self.file_list)
        self.test_data_count = file_count
        self.scroll_wheel = ctk.CTkSlider(master=self.test_record_frame, from_=0, to=self.test_data_count-1,
                                          number_of_steps=self.test_data_count-1)
        self.scroll_wheel.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Display the selected file index

        self.selected_file_label = ctk.CTkLabel(master=self.test_record_frame, text="Selected File Name: 0")
        self.selected_file_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Bind the slider's value change event to update the label
        self.scroll_wheel.bind("<B1-Motion>", self.update_file_label)

    def update_file_label(self, event):
        selected_index = int(self.scroll_wheel.get())
        self.selected_file_label.configure(text=f"Selected File Name: {self.file_list[selected_index]}")
        self.controller.args_dict['Deploy']['Traj_index'] = selected_index

    def print_arg_var(self):
        print(self.controller.args_dict)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        self.controller.show_frame("MotionPlanning")


    '''GUI/data update functions'''

    def update_ui_summary(self):
        # Remove old summary labels if they exist
        if hasattr(self, 'modeling_summary_text'):
            self.modeling_summary_text.grid_forget()
        if hasattr(self, 'planning_control_summary_text'):
            self.planning_control_summary_text.grid_forget()
        # self.label_modeling_summary = ctk.CTkLabel(master=self.modeling_summary_frame, text="Modeling Summary")
        # self.label_modeling_summary.grid(row=0, column=0, padx=10, pady=10, sticky="")
        #
        # # Format the Modeling and Planning_Controls summaries
        # self.modeling_summary = self.format_dict_for_display(self.controller.args_dict['Modeling'])
        # self.planning_controls_summary = self.format_dict_for_display(self.controller.args_dict['Planning_Controls'])
        #
        # # Combine both sections into one summary string
        # self.final_summary = f"Modeling Selection:\n{self.modeling_summary}\nPlanning Controls Selection:\n{self.planning_controls_summary}"
        #
        # # Label to display the summary
        # self.label_modeling_summary_details = ctk.CTkLabel(master=self.modeling_summary_frame, text=self.final_summary,
        #                                                    anchor="w",
        #                                                    justify="left")
        # self.label_modeling_summary_details.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.modeling_summary = self.format_dict_for_display(self.controller.args_dict['Modeling'])
        self.modeling_summary_text = ctk.CTkLabel(master=self.modeling_summary_frame,
                                                  text=self.modeling_summary,
                                                  anchor="w",  # Left-align the text
                                                  justify="left",  # Justify the text to the left to make it look neat
                                                  font=("Arial", 15),  # Set font and size (customize as you like)
                                                  width=600,  # Optional: specify a fixed width to make it look uniform
                                                  height=150,  # Optional: specify a fixed height
                                                  corner_radius=10,  # Optional: round corners for a soft look
                                                  fg_color=("white", "gray25"),  # Background color for light/dark mode
                                                  text_color=("black", "white"),  # Text color for light/dark mode
                                                  padx=10,  # Padding inside the label
                                                  pady=10,  # Padding inside the label
                                                  )
        self.modeling_summary_text.grid(row=1, column=0, padx=10, pady=10, sticky="")
        # Update Motion Planner and Controller Selection
        self.planning_control_summary = self.format_dict_for_display(self.controller.args_dict['Planning_Controls'])
        self.planning_control_summary_text = ctk.CTkLabel(
            master=self.planner_controller_summary_frame,
            text=self.planning_control_summary,
            anchor="w",  # Left-align the text
            justify="left",  # Justify the text to the left to make it look neat
            font=("Arial", 15),  # Set font and size (customize as you like)
            width=600,  # Optional: specify a fixed width to make it look uniform
            height=150,  # Optional: specify a fixed height
            corner_radius=10,  # Optional: round corners for a soft look
            fg_color=("white", "gray25"),  # Background color for light/dark mode
            text_color=("black", "white"),  # Text color for light/dark mode
            padx=10,  # Padding inside the label
            pady=10,  # Padding inside the label
        )
        self.planning_control_summary_text.grid(row=1, column=0, padx=10, pady=10, sticky="")


    def update_ui_save_data(self):
        """Updates the UI based on the radio button selection."""
        self.update_save_data()
        for widget in self.test_record_frame.grid_slaves():
            if int(widget.grid_info()['row']) > 2:
                widget.grid_forget()  # Remove widgets from previous selection

        # Check the value of the radio button
        # Condition for saved model loading
        if self.radio_var_save_data.get() == 0:
            # Show UI for loading an existing model
            self.save_data_label = ctk.CTkLabel(self.test_record_frame, text="Save tracking data", anchor="w")
            self.save_data_label.grid(row=3, column=0, columnspan=2, sticky="ew")

            self.record_data_folder = ctk.CTkButton(self.test_record_frame, text="Select Folder",
                                                     command=self.select_record_data_folder)
            self.record_data_folder.grid(row=4, column=0, padx=(0, 20), pady=(5, 10), sticky="ew")

            self.record_data_folder_label = ctk.CTkLabel(self.test_record_frame, text="No folder selected", anchor="w")
            self.record_data_folder_label.grid(row=4, column=1, padx=(10, 10), pady=(5, 10), sticky="ew")

        # Condition for training a model
        else:
            # Show UI for loading an existing model
            self.save_data_label = ctk.CTkLabel(self.test_record_frame, text="Tracking data will not be saved", anchor="w")
            self.save_data_label.grid(row=3, column=0, columnspan=2, sticky="ew")



    ''' Helper functions'''
    '''Function to combine key value data from dict'''

    def refresh(self):
        self.update_ui_summary()

    def format_dict_for_display(self,dictionary):
        summary = ""
        for key, value in dictionary.items():
            summary += f"{key}: {value}\n"
        return summary


    '''Directory/ model selection functions'''

    def select_record_data_folder(self):
        # Open the directory selector dialog
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.record_data_folder_label.configure(text=selected_directory)
            self.controller.args_dict['Deploy']['Save_tracking_dir'] = selected_directory




    '''Args value update functions'''

    def update_save_data(self):
        selected_mode = self.radio_var_save_data.get()
        if  selected_mode == 0:
            self.controller.args_dict['Deploy']['Save_data'] = True
        else:
            self.controller.args_dict['Deploy']['Save_data'] = False


    def next_page(self):
        args_json = json.dumps(self.controller.args_dict)
        # Path to the package in parent folder

        dev_mode =True
        if dev_mode == True:
            print('Running app in dev mode: Running koopman.py script')
            parent_dir = '/home/ajoglek/Project-Varuna-RZR/Project-Varuna-MMPK-Package'
            script_path = os.path.join(parent_dir, "koopman.py")
            # If in dev mode, run the Python script with the arguments
            try:
                result = subprocess.run(
                    ["python3", script_path, "--arg_dict", args_json, "--dev_mode", "True"],  # Add 'python' to run the script
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Print the output from the Python script
                print(f"Python script output: {result.stdout}")

            except subprocess.CalledProcessError as e:
                print(f"Error occurred while running the Python script: {e.stderr}")

        else: # Condition for running in user mode
            print('Running app as user through binary')
            # Get the parent directory of the current script's directory
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

            # Define the path to the target file in the parent directory
            script_path = os.path.join(parent_dir, "koopman")

            try:
                result = subprocess.run(
                    [script_path,  "--arg_dict", args_json],
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Print the output from the target script (or handle it in any way)
                print(f"Script output: {result.stdout}")

            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e.stderr}")

    def previous_page(self):
        self.controller.show_frame("Planning_Controls")
        self.update_idletasks()