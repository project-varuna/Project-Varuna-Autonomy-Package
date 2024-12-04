import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # For displaying a warning dialog
import re # For str comparisons
import math

class Modeling(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.controller.args_dict['Modeling']['Platform']='F1tenth'

        # configure the grid layout for the main frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        # self.grid_rowconfigure(3, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        # self.grid_columnconfigure(3, weight=1)

        # create sidebar frame with widgets
        self.modeling_sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.modeling_sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.modeling_sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.modeling_sidebar_frame, text="Project Varuna", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, command=self.open_directory_selector)
        self.modeling_sidebar_button_1 = ctk.CTkButton(self.modeling_sidebar_frame, text="Modeling",
                       state="disabled",  # Make button non-clickable
                       fg_color="#FF9000",   # Set background color
                       text_color="black", # Set text color
                       text_color_disabled="white"
                      )
        self.modeling_sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.modeling_sidebar_button_2 = ctk.CTkButton(self.modeling_sidebar_frame, text="Planning/Controls",
                       state="disabled",  # Make button non-clickable
                       fg_color="#5180D2",   # Set background color
                       text_color="black", # Set text color
                       text_color_disabled="white"
                      )

        # self.modeling_sidebar_button_2 = ctk.CTkButton(self.modeling_sidebar_frame)
        self.modeling_sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.modeling_sidebar_button_3 = ctk.CTkButton(self.modeling_sidebar_frame, text="Deploy",
                       state="disabled",  # Make button non-clickable
                       fg_color="#5180D2",   # Set background color
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

        self.proceed_button = ctk.CTkButton(master=self,
                                            fg_color="blue",  # Default color (blue)
                                            hover_color="green",  # Color when hovering (green)
                                            text_color="white",  # Text color
                                            text="Proceed →",  # Button label
                                            border_width=2,command=self.next_page)
        self.proceed_button.grid(row=3, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Create the textbox
        self.modeling_textbox = ctk.CTkTextbox(self, width=250, height=20)
        self.modeling_textbox.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # Insert the text while in normal state
        self.modeling_textbox.insert("0.0",
                                     "Welcome to Project Varuna!\n\n"
                                     "This GUI application allows you to generate your own MMPK pipeline for modeling, planning, "
                                     "and control of multi-scale UGVs.\n\n"

                                     "Let's get started!!!\n\n"

                                     "1. **Select the Vehicle Platform:**\n"
                                     "   - By default the 1/10th (F1Tenth) or 1/5th (Hunter SE) are available.\n"
                                     "   - However, if you want to select a custom platform, enter the name and control limits on the right pane.\n\n"
                                     

                                     "2. **Choose Your Model Setup:**\n"
                                     "   - If you have previously trained MMPK models, select the directory where they're stored.\n"
                                     "   - Otherwise, select the training and test data directories.\n\n"

                                     "3. **Identify a New Model (Optional):**\n"
                                     "   - Select a folder where the new model should be saved.\n"
                                     "   - **Note:** Ensure that the folder is empty or contains no other files.\n\n"

                                     "4. **Training/Test Data Format:**\n"
                                     "   - Choose the format for your training/test data (.csv in AutoDRIVE/ISAAC format or rosbag files).\n"
                                     "   - Ensure the IMU information in the training and test data follows the ISO8855 (right hand rule) convention.\n\n"

                                     "5. **Important:**\n"
                                     "   - Check the file format requirements in the README file to avoid data-parsing errors.\n"
                                     )
        self.modeling_textbox.configure(state="disabled")

        # create radiobutton frame
        self.platform_selection_frame = ctk.CTkFrame(self)
        self.platform_selection_frame.grid(row=0, column=3,columnspan=2 ,padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var_platform = tk.IntVar(value=0)
        # Setup default value of MMPK type
        self.controller.args_dict['Modeling']['MMPK_Type'] = 'Static'
        self.label_radio_group = ctk.CTkLabel(master=self.platform_selection_frame, text="Platform")
        self.label_radio_group.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = ctk.CTkRadioButton(master=self.platform_selection_frame, variable=self.radio_var_platform, value=0,text='F1tenth',command=self.update_ui_switch_platform)
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.radio_button_2 = ctk.CTkRadioButton(master=self.platform_selection_frame, variable=self.radio_var_platform, value=1,text='Hunter',command=self.update_ui_switch_platform)
        self.radio_button_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.radio_button_3 = ctk.CTkRadioButton(master=self.platform_selection_frame, variable=self.radio_var_platform, value=2,text='Custom',command=self.update_ui_switch_platform)
        self.radio_button_3.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.data_selection_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.data_selection_frame.grid(row=1,column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.data_selection_frame.grid_columnconfigure(0, weight=1)
        self.data_selection_frame.grid_rowconfigure(4, weight=1)

        self.trained_model_text = ctk.CTkLabel(self.data_selection_frame, text="Select a pretrained model?",anchor="w")
        self.trained_model_text.grid(row=0, column=0, padx=(0, 20), pady=(10, 10), sticky="ew")
        self.radio_var_trained_model = tk.IntVar(value=0)
        trained_model_radio_button = ctk.CTkRadioButton(self.data_selection_frame, text='Yes', variable=self.radio_var_trained_model, value=0, command=self.update_ui_model_data)
        trained_model_radio_button.grid(row=0, column=1, padx=(0, 10), sticky="w")

        trained_model_radio_button = ctk.CTkRadioButton(self.data_selection_frame, text='No', variable=self.radio_var_trained_model, value=1, command=self.update_ui_model_data)
        trained_model_radio_button.grid(row=0, column=2, padx=(10, 0), sticky="w")

        self.update_ui_model_data()


        # create radiobutton frame for training and test data
        self.data_options_frame = ctk.CTkFrame(self)
        self.data_options_frame.grid(row=1, column=3, columnspan=2,padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var_train = tk.IntVar(value=0)
        self.controller.args_dict['Modeling']['Train_data_type'] = 'Project-Varuna-Custom'
        self.train_data_type_label = ctk.CTkLabel(master=self.data_options_frame, text="Training data format")
        self.train_data_type_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.train_autodrive_button = ctk.CTkRadioButton(master=self.data_options_frame, variable=self.radio_var_train, value=0,text='Project-Varuna-Custom',command=self.update_train_data_type)
        self.train_autodrive_button.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.train_isaac_button = ctk.CTkRadioButton(master=self.data_options_frame, variable=self.radio_var_train, value=1,text='AutoDRIVE',command=self.update_train_data_type)
        self.train_isaac_button.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.train_rosbag_button = ctk.CTkRadioButton(master=self.data_options_frame, variable=self.radio_var_train, value=2,text='Rosbag',command=self.update_train_data_type)
        self.train_rosbag_button.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.radio_var_test = tk.IntVar(value=0)
        self.controller.args_dict['Modeling']['Test_data_type'] = 'Project-Varuna-Custom'
        self.test_data_type_label = ctk.CTkLabel(master=self.data_options_frame, text="Test data format")
        self.test_data_type_label.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.test_autodrive_button = ctk.CTkRadioButton(master=self.data_options_frame, variable=self.radio_var_test, value=0,text='Project-Varuna-Custom',command=self.update_test_data_type)
        self.test_autodrive_button.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.test_isaac_button = ctk.CTkRadioButton(master=self.data_options_frame, variable=self.radio_var_test, value=1,text='AutoDRIVE',command=self.update_test_data_type)
        self.test_isaac_button.grid(row=2, column=1, pady=10, padx=20, sticky="n")
        self.test_rosbag_button = ctk.CTkRadioButton(master=self.data_options_frame, variable=self.radio_var_test, value=2,text='Rosbag',command=self.update_test_data_type)
        self.test_rosbag_button.grid(row=3, column=1, pady=10, padx=20, sticky="n")


        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")


    # Event functions
    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        self.controller.show_frame("MotionPlanning")


    '''GUI/data update functions'''

    # Args value update functions
    def update_ui_switch_platform(self):
        for widget in self.data_selection_frame.grid_slaves():
            if int(widget.grid_info()['column']) > 2:
                widget.grid_forget()  # Remove widgets from previous selection

        # Update the dictionary based on the selected radio button
        selected_value = self.radio_var_platform.get()
        # print(selected_value)

        # Map radio button values to platform names
        platform_map = {0: "F1tenth", 1: "Hunter", 2: "Custom"}

        # Update the dictionary with the selected platform
        self.controller.args_dict['Modeling']['Platform'] = platform_map[selected_value]

        # Print the updated dictionary (for debugging purposes)
        # print(self.controller.args_dict['Modeling']['Platform'])
        # print('Selected-value', selected_value)
        if selected_value == 1 or selected_value == 2:
            self.radio_var_mmpk_mode = tk.IntVar(value=0)
            self.label_mmpk_type = ctk.CTkLabel(master=self.platform_selection_frame, text="MMPK Type")
            self.label_mmpk_type.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
            self.mmpk_static_radio_button = ctk.CTkRadioButton(master=self.platform_selection_frame,
                                                               variable=self.radio_var_mmpk_mode,
                                                               value=0, text='Static', command=self.update_mmpk_type)
            self.mmpk_static_radio_button.grid(row=1, column=1, pady=10, padx=20, sticky="n")
            self.mmpk_adaptive_radio_button = ctk.CTkRadioButton(master=self.platform_selection_frame,
                                                                 variable=self.radio_var_mmpk_mode,
                                                                 value=1, text='Adaptive',
                                                                 command=self.update_mmpk_type)
            self.mmpk_adaptive_radio_button.grid(row=2, column=1, pady=10, padx=20, sticky="n")

        # If F1tenth is selected, remove the MMPK options
        else:
            self.controller.args_dict['Modeling']['MMPK_Type'] = 'Static'
            # Remove MMPK related widgets if they exist
            if hasattr(self, 'label_mmpk_type'):
                self.label_mmpk_type.grid_forget()
            if hasattr(self, 'mmpk_static_radio_button'):
                self.mmpk_static_radio_button.grid_forget()
            if hasattr(self, 'mmpk_adaptive_radio_button'):
                self.mmpk_adaptive_radio_button.grid_forget()

        # Update GUI for custom platform
        if selected_value == 2:
            self.update_ui_custom_platform()
        else:
            # Remove MMPK related widgets if they exist
            if hasattr(self, 'label_platform_name'):
                self.label_platform_name.grid_forget()
            # Forget custom platform name
            if hasattr(self, 'platform_name_text'):
                self.platform_name_text.grid_forget()
            if hasattr(self, 'entry_platform_name'):
                self.entry_platform_name.grid_forget()
            # Forget custom platform vel
            if hasattr(self, 'platform_vel_lim_text'):
                self.platform_vel_lim_text.grid_forget()
            if hasattr(self, 'entry_platform_vel_lim'):
                self.entry_platform_vel_lim.grid_forget()
            # Forget custom platform steer
            if hasattr(self, 'platform_steer_lim_text'):
                self.platform_steer_lim_text.grid_forget()
            if hasattr(self, 'entry_platform_steer_lim'):
                self.entry_platform_steer_lim.grid_forget()
            # # Forget apply button
            if hasattr(self, 'platform_save_button'):
                self.platform_save_button.grid_forget()
            # Delete the data entry in dict
            self.controller.args_dict['Modeling'].pop('Platform_Custom_Name', None)
            self.controller.args_dict['Modeling'].pop('Platform_Custom_Vel_Lim', None)
            self.controller.args_dict['Modeling'].pop('Platform_Custom_Steer_Lim',None)


    def update_ui_custom_platform(self):
        self.label_platform_name = ctk.CTkLabel(master=self.platform_selection_frame, text="Platform details")
        self.label_platform_name.grid(row=0, column=2, columnspan=1, pady=10, sticky="")



        # Add Entry: Platform name
        self.platform_name_text = ctk.CTkLabel(self.platform_selection_frame, text="Name:",anchor="w")
        self.platform_name_text.grid(row=1, column=2, pady=(10, 10), sticky="ew")
        self.entry_platform_name = ctk.CTkEntry(master=self.platform_selection_frame)
        self.entry_platform_name.grid(row=1, column=3, pady=10, sticky="w")

        # Add Entry: Platform velocity limit
        self.platform_vel_lim_text = ctk.CTkLabel(self.platform_selection_frame, text="Max velocity (m/s):",anchor="w")
        self.platform_vel_lim_text.grid(row=2, column=2, pady=(10, 10), sticky="ew")
        self.entry_platform_vel_lim = ctk.CTkEntry(master=self.platform_selection_frame)
        self.entry_platform_vel_lim.grid(row=2, column=3, pady=10, sticky="w")

        # Add Entry: Platform steering limit
        self.platform_steer_lim_text = ctk.CTkLabel(self.platform_selection_frame, text="Steering limits (rad): \u00B1",anchor="w")
        self.platform_steer_lim_text.grid(row=3, column=2, pady=(10, 10), sticky="ew")
        self.entry_platform_steer_lim = ctk.CTkEntry(master=self.platform_selection_frame)
        self.entry_platform_steer_lim.grid(row=3, column=3, pady=10, sticky="w")

        # Add a Button to trigger saving num of MMPK models
        self.platform_save_button = ctk.CTkButton(master=self.platform_selection_frame, text="Apply", command=self.save_custom_platform)
        self.platform_save_button.grid(row=4, column=2, pady=10)

    def update_ui_model_data(self):
        """Updates the UI based on the radio button selection."""
        self.update_trained_model()
        for widget in self.data_selection_frame.grid_slaves():
            if int(widget.grid_info()['row']) > 0:
                widget.grid_forget()  # Remove widgets from previous selection

        # Check the value of the radio button
        # Condition for saved model loading
        if self.radio_var_trained_model.get() == 0:
            # Show UI for loading an existing model
            self.model_label = ctk.CTkLabel(self.data_selection_frame, text="Load Model", anchor="w")
            self.model_label.grid(row=1, column=0, columnspan=2, sticky="ew")

            self.select_file_model = ctk.CTkButton(self.data_selection_frame, text="Select Folder",
                                                     command=self.select_model)
            self.select_file_model.grid(row=2, column=0, padx=(0, 20), pady=(5, 10), sticky="ew")

            self.folder_label_model = ctk.CTkLabel(self.data_selection_frame, text="No folder selected", anchor="w")
            self.folder_label_model.grid(row=2, column=1, padx=(10, 10), pady=(5, 10), sticky="ew")
            '''Delete parameters from dict related to train model if this option is selected'''
            self.controller.args_dict['Modeling'].pop('Num_models',None)
            self.controller.args_dict['Modeling'].pop('Train_data_folder',None)
            self.controller.args_dict['Modeling'].pop('Save_Trained_Model',None)
            self.controller.args_dict['Modeling'].pop('Model_save_dir',None)


        # Condition for training a model
        else:
            # Show UI for selecting a directory to train a new model
            self.train_label = ctk.CTkLabel(self.data_selection_frame, text="Training Data Directory", anchor="w")
            self.train_label.grid(row=1, column=0, columnspan=2, sticky="ew")

            self.select_folder_train = ctk.CTkButton(self.data_selection_frame, text="Select Folder",
                                                     command=self.select_train_dir)
            self.select_folder_train.grid(row=2, column=0, padx=(0, 20), pady=(5, 10), sticky="ew")

            self.folder_label_train = ctk.CTkLabel(self.data_selection_frame, text="No folder selected", anchor="w")
            self.folder_label_train.grid(row=2, column=1, padx=(10, 10), pady=(5, 10), sticky="ew")

            self.num_models_text = ctk.CTkLabel(self.data_selection_frame, text="Number of models in MMPK setup?",
                                                   anchor="w")
            self.num_models_text.grid(row=5, column=0, padx=(0, 20), pady=(10, 10), sticky="ew")

            # Add Entry: Num models in MMPK
            self.entry_num_models = ctk.CTkEntry(master=self.data_selection_frame)
            self.entry_num_models.grid(row=5, column=1, padx=10, pady=10, sticky="w")

            # Add a Button to trigger saving num of MMPK models
            save_button = ctk.CTkButton(master=self.data_selection_frame, text="Apply", command=self.save_num_models)
            save_button.grid(row=5, column=2, pady=10)

            self.save_model_text = ctk.CTkLabel(self.data_selection_frame, text="Save the trained model?",
                                                   anchor="w")
            self.save_model_text.grid(row=6, column=0, padx=(0, 20), pady=(10, 10), sticky="ew")

            self.radio_var_save_model = tk.IntVar(value=0)
            save_model_radio_button = ctk.CTkRadioButton(self.data_selection_frame, text='Yes',
                                                            variable=self.radio_var_save_model, value=0,
                                                            command=self.update_ui_save_model)
            save_model_radio_button.grid(row=6, column=1, padx=(0, 10), sticky="w")

            save_model_radio_button = ctk.CTkRadioButton(self.data_selection_frame, text='No',
                                                            variable=self.radio_var_save_model, value=1,
                                                            command=self.update_ui_save_model)
            save_model_radio_button.grid(row=6, column=2, padx=(10, 0), sticky="w")
            self.update_ui_save_model()

        self.test_label = ctk.CTkLabel(self.data_selection_frame, text="Test Data Directory",
                                               anchor="w")
        self.test_label.grid(row=3, column=0, columnspan=2, pady=(10, 0),sticky="ew")
        self.select_folder_test = ctk.CTkButton(self.data_selection_frame, text="Select Folder",
                                                  command=self.select_test_dir)
        self.select_folder_test.grid(row=4, column=0, padx=(0, 20), pady=(0, 10), sticky="ew")
        self.folder_label_test = ctk.CTkLabel(self.data_selection_frame, text="No folder selected", anchor="w")
        self.folder_label_test.grid(row=4, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")


    def update_ui_save_model(self):
        save_model_map = {0: True, 1: False}
        for widget in self.data_selection_frame.grid_slaves():
            # print(widget.grid_info())
            if int(widget.grid_info()['row']) > 6:
                widget.grid_forget()  # Remove widgets from previous selection
        if self.radio_var_save_model.get() == 0:
            self.controller.args_dict['Modeling']['Save_Trained_Model'] = save_model_map[int(self.radio_var_save_model.get())]
            self.save_model_folder = ctk.CTkButton(self.data_selection_frame, text="Select Folder",
                                                      command=self.select_model_save_dir)
            self.save_model_folder.grid(row=7, column=0, padx=(0, 20), pady=(0, 10), sticky="ew")
            self.save_model_folder_text = ctk.CTkLabel(self.data_selection_frame, text="No folder selected", anchor="w")
            self.save_model_folder_text.grid(row=7, column=1, padx=(10, 10), pady=(0, 10), sticky="ew")
        else:
            self.controller.args_dict['Modeling']['Save_Trained_Model'] = save_model_map[int(self.radio_var_save_model.get())]
            for widget in self.data_selection_frame.grid_slaves():
                if int(widget.grid_info()['row']) > 6:
                    widget.grid_forget()  # Hide widgets by forgetting them


    ''' Helper functions'''
    # Directory/ model selection functions
    def select_train_dir(self):
        # Open the directory selector dialog
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.folder_label_train.configure(text=selected_directory)
            self.controller.args_dict['Modeling']['Train_data_folder'] = selected_directory


    def select_test_dir(self):
        # Open the directory selector dialog
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.folder_label_test.configure(text=selected_directory)
            self.controller.args_dict['Modeling']['Test_data_folder'] = selected_directory

    def select_model_save_dir(self):
        # Open the directory selector dialog
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.save_model_folder_text.configure(text=selected_directory)
            self.controller.args_dict['Modeling']['Model_save_dir'] = selected_directory

    def select_model(self):
        selected_file = filedialog.askopenfilename(title="Select Model File",
                                                   filetypes=[("Model Files", "*.h5 *.pkl *.pt"),
                                                              ("Binary Files", "*.bin"),  # Binary file extension
                                                              # You can specify file extensions
                                                              ("All Files", "*")])
        if selected_file:
            self.folder_label_model.configure(text=selected_file)
            self.controller.args_dict['Modeling']['Saved_model_file'] = selected_file


    def save_num_models(self):
        num_models = self.entry_num_models.get()  # Get value from state penalty entry
        # Validation: Check if the input is two integers separated by a space
        if not self.validate_num_models(num_models):
            self.show_warning_num_models("Number of Models")
            return

        self.controller.args_dict['Modeling']['Num_models'] = num_models


    def save_custom_platform(self):
        platform_name = self.entry_platform_name.get()  # Get value from state penalty entry
        platform_vel_lim = self.entry_platform_vel_lim.get()
        platform_steering_lim = self.entry_platform_steer_lim.get()

        '''Perform checks'''
        # Validation: Check if name is valid
        if not self.validate_platform_name(platform_name):
            self.show_warning_name("Name")
            return
        # Validation: Check if vel lim is valid
        if not self.validate_velocity_limit(platform_vel_lim):
            self.show_warning_vel_lim("Max velocity")
            return
        # Validation: Check if vel lim is valid
        if not self.validate_steering_limits(platform_steering_lim):
            self.show_warning_steer_lim("Steering limits")
            return

        '''Update data to dict'''
        self.controller.args_dict['Modeling']['Platform_Custom_Name'] = platform_name
        self.controller.args_dict['Modeling']['Platform_Custom_Vel_Lim'] = platform_vel_lim
        self.controller.args_dict['Modeling']['Platform_Custom_Steer_Lim'] = platform_steering_lim

    def update_mmpk_type(self):
        mmpk_map = {0: "Static", 1: "Adaptive"}
        mmpk_type = self.radio_var_mmpk_mode.get()
        self.controller.args_dict['Modeling']['MMPK_Type'] = mmpk_map[mmpk_type]
        # print(self.controller.args_dict['Modeling']['MMPK_Type'])

    def update_trained_model(self):
        selected_mode = self.radio_var_trained_model.get()
        if  selected_mode == 0:
            self.controller.args_dict['Modeling']['Trained_model'] = True
        else:
            self.controller.args_dict['Modeling']['Trained_model'] = False


    def update_train_data_type(self):
        # Update the dictionary based on the selected radio button
        selected_value = self.radio_var_train.get()

        # Map radio button values to platform names
        data_type_map = {0: "Project-Varuna-Custom", 1: "AutoDRIVE", 2: "Rosbag"}

        # Update the dictionary with the selected platform
        self.controller.args_dict['Modeling']['Train_data_type'] = data_type_map[int(selected_value)]
        # print(self.controller.args_dict['Modeling']['Train_data_type'])

        # Print the updated dictionary (for debugging purposes)
        # print(self.controller.args_dict['Modeling']['Platform'])

    def update_test_data_type(self):
        # Update the dictionary based on the selected radio button
        selected_value = self.radio_var_test.get()

        # Map radio button values to platform names
        data_type_map = {0: "Project-Varuna-Custom", 1: "AutoDRIVE", 2: "Rosbag"}

        # Update the dictionary with the selected platform
        self.controller.args_dict['Modeling']['Test_data_type'] = data_type_map[int(selected_value)]

    '''Functions for value check'''

    def validate_num_models(self, input_str):
        try:
            # Attempt to convert the input string to an integer
            int_val = int(input_str)
            # Ensure the input string is not a float (check for a decimal point)
            if '.' in input_str:
                return False
            return True
        except ValueError:
            # If conversion to integer fails, return False
            return False

    def validate_platform_name(self, input_str):
        # Regular expression to check if the string contains only alphanumeric characters (no spaces, no special characters)
        if re.match("^[a-zA-Z0-9]*$", input_str):
            return True
        else:
            return False

    def validate_velocity_limit(self, input_str):
        try:
            # Attempt to convert the input string to a float
            float_val = float(input_str)

            # Check if the float value is positive
            if float_val > 0:
                return True
            else:
                return False
        except ValueError:
            # If conversion to float fails, return False
            return False

    def validate_steering_limits(self, input_str):
        try:
            # Attempt to convert the input string to a float
            float_val = float(input_str)

            # Check if the float value is between -π/2 and π/2
            if 0 <= float_val <= math.pi / 2:
                return True
            else:
                return False
        except ValueError:
            # If conversion to float fails, return False
            return False

    def show_warning_num_models(self,field_name):
        messagebox.showwarning("Input Error",
                               f"Invalid input for {field_name}. Please enter 1 integer value denoting number of models in MMPK setup.")

    def show_warning_name(self,field_name):
        messagebox.showwarning("Input Error",
                               f"Invalid input for {field_name}. Please enter name of platform without spaces and special characters.")

    def show_warning_vel_lim(self,field_name):
        messagebox.showwarning("Input Error",
                               f"Invalid input for {field_name}. Please enter a single int/float value denoting velocity limit of the platform.")

    def show_warning_steer_lim(self,field_name):
        messagebox.showwarning("Input Error",
                               f"Invalid input for {field_name}. Please enter a single positive int/float denoting just magnitude of steering limit for the platform. Must not exceed pi/2 i.e 1.5708 rad")

    def next_page(self):
        next_frame = self.controller.show_frame("Planning_Controls")
        # Adjusts window size when switching frames
        self.update_idletasks()
        if hasattr(next_frame, 'refresh'):
            next_frame.refresh()