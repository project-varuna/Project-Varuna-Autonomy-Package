import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # For displaying a warning dialog
import rospy

class Planning_Controls(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # configure the grid layout for the main frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        # self.grid_rowconfigure(3, weight=1)
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
                       fg_color="#FF9000",   # Set background color
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

        # Previous Button
        self.previous_button = ctk.CTkButton(master=self,
                                             fg_color="blue",  # Default color (red)
                                             hover_color="red",  # Color when hovering (darker red)
                                             text_color="white",  # Text color
                                             text="← Previous",  # Button label
                                             border_width=2,
                                             command=self.previous_page)
        # self.previous_button.grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky="nsew")
        self.previous_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Proceed Button
        self.proceed_button = ctk.CTkButton(master=self,
                                            fg_color="blue",  # Default color (blue)
                                            hover_color="green",  # Color when hovering (green)
                                            text_color="white",  # Text color
                                            text="Proceed →",  # Button label
                                            border_width=2,
                                            command=self.next_page)
        # self.proceed_button.grid(row=0, column=1, padx=(0, 10), pady=(0, 0), sticky="nsew")
        self.proceed_button.grid(row=3, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # Create the textbox
        self.modeling_textbox = ctk.CTkTextbox(self, width=250, height=20)
        self.modeling_textbox.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # Insert the text while in normal state
        self.modeling_textbox.insert("0.0", "Setting up parameters for motion planning and controls! \n\n"

                                     "1. **Select rostopics for state estimation**\n"
                                     "   - First we select the topic to obtain pose estimate. Select the data type (rosmsg type) between Point and Pose2D\n"
                                     "   - Next choose the IMU topic from dropdown. Select the frame type between ISO 8855 and SAE J670\n"
                                     "   - Even if you select SAE J670, it will be converted to ISO8855 internally to maintain that convention for your training and test data \n\n"

                                     "2. **Select rostopic for controls:**\n"
                                     "   - The user has the option to select either separate topics for throttle and steering or a single topic\n"
                                     "   - If separate topics are selected, they use the Float32 msg type, else we use the Twist message structure.\n\n"

                                     "3. **Setup state and control penalties for MPC:**\n"
                                     "   - Since we opearte in Polar space and control vehicle via linear velocity/steering angle, the MPC costs should be 2 integers separated by a space.\n"
                                     "   - Don't forget to click apply!.\n\n"

                                     "4. **Select the preview horizon for controller and motion planner:**\n"
                                     "   - The preview horizon for controller will also be used to bin the data in case of training and select operating mode in outer control loop\n"
                                     "   - The preview horizon for planner does not affect the model switching and can be larger if needed. \n"
                                     "   - Both entires should be  single float values, and don't forget to hit apply! \n"

                                     "5. **Select motion planner:**\n"
                                     "   - Depending on type of MMPK approach selected, the user can choose between Curvature-based Reachability Planner (best for on-road) or Load-transfer based Reachability Planner (best for off-road) \n")

        # Disable the textbox to prevent user editing
        self.modeling_textbox.configure(state="disabled")

        # create radiobutton frame
        self.cost_matrix_frame = ctk.CTkFrame(self)
        self.cost_matrix_frame.grid(row=0, column=3,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # MPC Cost Label
        self.label_mpc_cost = ctk.CTkLabel(master=self.cost_matrix_frame, text="MPC Cost")
        self.label_mpc_cost.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add Label: State Penalty
        self.label_state_penalty = ctk.CTkLabel(master=self.cost_matrix_frame, text="State Penalty")
        self.label_state_penalty.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Add Entry: State Penalty Entry Box
        self.entry_state_penalty = ctk.CTkEntry(master=self.cost_matrix_frame)
        self.entry_state_penalty.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Add Label: Control Action Penalty
        self.label_control_penalty = ctk.CTkLabel(master=self.cost_matrix_frame, text="Control Action Penalty")
        self.label_control_penalty.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Add Entry: Control Action Penalty Entry Box
        self.entry_control_penalty = ctk.CTkEntry(master=self.cost_matrix_frame)
        self.entry_control_penalty.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Add a Button to trigger saving into the dictionary
        save_button = ctk.CTkButton(master=self.cost_matrix_frame, text="Apply", command=self.save_mpc_costs)
        save_button.grid(row=3, column=1,  pady=10)


        # Topic selection frame
        self.topic_selection_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.topic_selection_frame.grid(row=1,column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.topic_selection_frame.grid_columnconfigure(0, weight=1)
        self.topic_selection_frame.grid_rowconfigure(4, weight=1)
        # Label for state estimation rostopic selection
        self.rostopic_state_label = ctk.CTkLabel(self.topic_selection_frame,
                                                 text="Select rostopic for state estimation", anchor="w")
        self.rostopic_state_label.grid(row=0, column=0, padx=(0, 20), pady=(10, 10), sticky="ew")
        # Label for pose topic
        self.rostopic_pose_label = ctk.CTkLabel(self.topic_selection_frame, text="Pose topic", anchor="w")
        self.rostopic_pose_label.grid(row=1, column=0, columnspan=2, sticky="ew")
        # Label for pose topic type
        self.rostopic_pose_type_label = ctk.CTkLabel(self.topic_selection_frame, text="Type", anchor="w")
        self.rostopic_pose_type_label.grid(row=1, column=2, columnspan=1, sticky="ew")

        # Dropdown for ROS topics (under Pose topic)
        self.available_topics = self.get_available_rostopics()  # Get available ROS topics
        self.selected_pose_topic = ctk.StringVar(value=self.available_topics[0])  # Initialize variable
        self.pose_topic_dropdown = ctk.CTkOptionMenu(self.topic_selection_frame, variable=self.selected_pose_topic,
                                                     values=self.available_topics,command=self.save_pose_topic_info)
        self.pose_topic_dropdown.grid(row=2, column=0, padx=(0, 10), pady=(10, 10), sticky="ew")

        # Radio buttons for selecting Pose Type
        self.pose_type_selection = ctk.StringVar(value=0)  # Default to 0
        self.pose_type_point = ctk.CTkRadioButton(self.topic_selection_frame, text="Point",
                                                  variable=self.pose_type_selection,
                                                  value=0, command=self.save_pose_topic_type)
        self.pose_type_point.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.pose_type_2d = ctk.CTkRadioButton(self.topic_selection_frame, text="Pose 2D",
                                               variable=self.pose_type_selection,
                                               value=1, command=self.save_pose_topic_type)
        self.pose_type_2d.grid(row=2, column=3, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.rostopic_imu_label = ctk.CTkLabel(self.topic_selection_frame, text="IMU topic", anchor="w")
        self.rostopic_imu_label.grid(row=3, column=0, columnspan=2, sticky="ew")
        # Label for pose topic type
        self.rostopic_imu_type_label = ctk.CTkLabel(self.topic_selection_frame, text="Frame Type", anchor="w")
        self.rostopic_imu_type_label.grid(row=3, column=2, columnspan=1, sticky="ew")
        # Dropdown for ROS topics (under Pose topic)
        self.available_topics = self.get_available_rostopics()  # Get available ROS topics
        self.selected_imu_topic = ctk.StringVar(value=self.available_topics[0])  # Initialize variable
        self.imu_topic_dropdown = ctk.CTkOptionMenu(self.topic_selection_frame, variable=self.selected_imu_topic,
                                                values=self.available_topics,command=self.save_imu_topic_info)
        self.imu_topic_dropdown.grid(row=4, column=0, padx=(0, 10), pady=(10, 10), sticky="ew")
        # Button for pose standard

        self.imu_frame_type_selection = ctk.StringVar(value=0)  # Default to 0
        self.pose_type_point = ctk.CTkRadioButton(self.topic_selection_frame, text="ISO 8855",
                                                  variable=self.imu_frame_type_selection,
                                                  value=0, command=self.save_imu_type)
        self.pose_type_point.grid(row=4, column=2, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.pose_type_2d = ctk.CTkRadioButton(self.topic_selection_frame, text="SAE J670",
                                               variable=self.imu_frame_type_selection,
                                               value=1, command=self.save_imu_type)
        self.pose_type_2d.grid(row=4, column=3, padx=(10, 10), pady=(10, 10), sticky="ew")



        # Control type selection pane
        self.control_type_text = ctk.CTkLabel(self.topic_selection_frame, text="Single or independent control topics for steering and velocity",
                                              anchor="w")
        self.control_type_text.grid(row=5, column=0, padx=(0, 20), pady=(10, 10), sticky="ew")

        # Control type button
        self.control_type = tk.IntVar(value=0)
        trained_model_radio_button = ctk.CTkRadioButton(self.topic_selection_frame, text='Single',
                                                        variable=self.control_type, value=0,
                                                        command=self.update_ui_control_topic_select)
        trained_model_radio_button.grid(row=5, column=2, padx=(0, 10), sticky="w")

        trained_model_radio_button = ctk.CTkRadioButton(self.topic_selection_frame, text='Separate',
                                                        variable=self.control_type, value=1,
                                                        command=self.update_ui_control_topic_select)
        trained_model_radio_button.grid(row=5, column=3, padx=(10, 0), sticky="w")
        self.update_ui_control_topic_select()


        # create radiobutton frame for training and test data
        self.planner_control_horizon_frame = ctk.CTkFrame(self)
        self.planner_control_horizon_frame.grid(row=1, column=3,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # MPC Cost Label
        self.label_preview = ctk.CTkLabel(master=self.planner_control_horizon_frame, text="Planner-Controller Preview")
        self.label_preview.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add Label: State Penalty
        self.label_mpc_horizon = ctk.CTkLabel(master=self.planner_control_horizon_frame, text="Prediction horizon for Model/Controller:")
        self.label_mpc_horizon.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Add Entry: State Penalty Entry Box
        self.entry_mpc_horizon = ctk.CTkEntry(master=self.planner_control_horizon_frame)
        self.entry_mpc_horizon.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Add Label: Control Action Penalty
        self.label_planner_horizon = ctk.CTkLabel(master=self.planner_control_horizon_frame, text="Prediction horizon for Motion Planner:")
        self.label_planner_horizon.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Add Entry: Control Action Penalty Entry Box
        self.entry_planner_horizon = ctk.CTkEntry(master=self.planner_control_horizon_frame)
        self.entry_planner_horizon.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        #Add a Button to trigger saving into the dictionary
        save_button = ctk.CTkButton(master=self.planner_control_horizon_frame, text="Apply", command=self.save_horizon_values)
        save_button.grid(row=3, column=1,  pady=10)



        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")


    '''Event functions'''
    def refresh(self):
        mmpk_type = self.controller.args_dict['Modeling'].get('MMPK_Type')
        if hasattr(self, 'rostopic_imu_label'):
            self.rostopic_imu_label.grid_forget()
        # if hasattr(self, 'imu_topic_dropdown'):
            # self.imu_topic_dropdown.grid_forget()
        # self.update_ui_rostopic_select(mmpk_type)
        self.update_ui_motion_planner_type(mmpk_type)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def update_ui_control_topic_select(self):
        # Map radio button values to platform names
        control_topic_map = {0: "Single", 1: "Separate"}
        selection = self.control_type.get()
        self.controller.args_dict['Planning_Controls']['Control_Type'] = control_topic_map[selection]


        for widget in self.topic_selection_frame.grid_slaves():
            if int(widget.grid_info()['row']) > 6:
                widget.grid_forget()  # Remove widgets from previous selection

        # Label for state estimation rostopic selection
        self.rostopic_controls_selection_label = ctk.CTkLabel(self.topic_selection_frame,
                                                 text="Select rostopic for control: The script publishes a Twist msg with command velocity (m/s) and steering angle (rad)", anchor="w")
        self.rostopic_controls_selection_label.grid(row=6, column=0, padx=(0, 20), pady=(10, 10), sticky="ew")

        if selection == 0:
            # Label for velocity topic
            self.rostopic_control_label = ctk.CTkLabel(self.topic_selection_frame, text="Combined control topic", anchor="w")
            self.rostopic_control_label.grid(row=7, column=0, columnspan=2, sticky="ew")
            # Select velocity topic
            self.selected_control_topic = ctk.StringVar(value=self.available_topics[0])  # Initialize variable
            self.control_topic_dropdown = ctk.CTkOptionMenu(self.topic_selection_frame,
                                                             variable=self.selected_control_topic,
                                                             values=self.available_topics,command=self.save_control_topic_single)
            self.control_topic_dropdown.grid(row=8, column=0, padx=(0, 10), pady=(10, 10), sticky="ew")
        else:
            # Label for velocity topic
            self.rostopic_velocity_label = ctk.CTkLabel(self.topic_selection_frame, text="Throttle topic: The script with publish a percentage throttle (v/v_max set for the platform)", anchor="w")
            self.rostopic_velocity_label.grid(row=7, column=0, columnspan=2, sticky="ew")
            # Select velocity topic
            self.selected_velocity_topic = ctk.StringVar(value=self.available_topics[0])  # Initialize variable
            self.velocity_topic_dropdown = ctk.CTkOptionMenu(self.topic_selection_frame, variable=self.selected_velocity_topic,
                                                         values=self.available_topics,command=self.save_control_topic_vel)
            self.velocity_topic_dropdown.grid(row=8, column=0, padx=(0, 10), pady=(10, 10), sticky="ew")

            # Label for steering topic
            self.rostopic_steering_label = ctk.CTkLabel(self.topic_selection_frame, text="Steering topic: The script with publish a percentage steering \u00B1 (delta/delta_max set for the platform)", anchor="w")
            self.rostopic_steering_label.grid(row=9, column=0, columnspan=2, sticky="ew")
            # Select steering topic
            self.selected_steering_topic = ctk.StringVar(value=self.available_topics[0])  # Initialize variable
            self.steering_topic_dropdown = ctk.CTkOptionMenu(self.topic_selection_frame, variable=self.selected_steering_topic,
                                                         values=self.available_topics,command=self.save_control_topic_steering)
            self.steering_topic_dropdown.grid(row=10, column=0, padx=(0, 10), pady=(10, 10), sticky="ew")

    def update_ui_motion_planner_type(self,mmpk_type):
    # create radiobutton frame for type of planer
        self.planner_type_frame = ctk.CTkFrame(self)
        self.planner_type_frame.grid(row=2, column=3, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Planner Type Label
        self.label_planner_type = ctk.CTkLabel(master=self.planner_type_frame, text="Planner-Controller Preview")
        self.label_planner_type.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Radio button to save planner_type
        self.radio_var_planner_type = tk.IntVar(value=0)

        self.controller.args_dict['Planning_Controls']['Planner_type'] = 'Curvature_based'

        # Curvature-based Reachability Planner radio button
        self.radio_button_curvature_planner = ctk.CTkRadioButton(master=self.planner_type_frame,
                                                                 variable=self.radio_var_planner_type,
                                                                 value=0, text='Curvature-based Reachability Planner',command=self.save_planner_type)
        self.radio_button_curvature_planner.grid(row=1, column=0, pady=(5, 10), padx=(20, 10), sticky="w")

        # Load-transfer based Reachability Planner radio button (only for 'Adaptive' type)
        if mmpk_type == 'Adaptive':
            self.radio_button_load_transfer_planner = ctk.CTkRadioButton(master=self.planner_type_frame,
                                                                         variable=self.radio_var_planner_type,
                                                                         value=1,
                                                                         text='Load-transfer based Reachability Planner',command=self.save_planner_type)
            self.radio_button_load_transfer_planner.grid(row=2, column=0, pady=(5, 10), padx=(20, 10), sticky="w")

    ''' Helper functions'''
    # Rostopic functions
    def get_available_rostopics(self):
        # Get list of available ROS topics
        # print('List of published topics:',rospy.get_published_topics())
        return [topic[0] for topic in rospy.get_published_topics()]



    '''Args value save functions'''

    def save_mpc_costs(self):
        state_penalty = self.entry_state_penalty.get()  # Get value from state penalty entry
        control_penalty = self.entry_control_penalty.get()  # Get value from control action penalty entry

        # Validation: Check if the input is two integers separated by a space
        if not self.validate_input_cost(state_penalty):
            self.show_warning_cost("State Penalty")
            return
        if not self.validate_input_cost(control_penalty):
            self.show_warning_cost("Control Action Penalty")
            return

        self.controller.args_dict['Planning_Controls']['Q'] = state_penalty
        self.controller.args_dict['Planning_Controls']['R'] = control_penalty

        # print("MPC costs:",self.controller.args_dict['Modeling']['Q'])

    def save_horizon_values(self):
        model_control_horizon = self.entry_mpc_horizon.get()  # Get value from state penalty entry
        planner_horizon = self.entry_planner_horizon.get()  # Get value from control action penalty entry
        # Validation: Check if the input is two integers separated by a space
        if not self.validate_input_horizon(model_control_horizon):
            self.show_warning_horizon("State Penalty")
            return
        if not self.validate_input_horizon(planner_horizon):
            self.show_warning_horizon("Control Action Penalty")
            return

        self.controller.args_dict['Planning_Controls']['N'] = model_control_horizon
        self.controller.args_dict['Planning_Controls']['N_p'] = planner_horizon

    def save_pose_topic_type(self):
        pose_type_map = {0: "Point", 1: "Pose2D"}
        # pose_topic = self.selected_pose_topic.get()
        # print('Pose topic is:*************',pose_topic)
        topic_type = self.pose_type_selection.get()
        # self.controller.args_dict['Planning_Controls']['Pose_topic'] = pose_topic
        self.controller.args_dict['Planning_Controls']['Pose_type'] = pose_type_map[int(topic_type)]

    def save_pose_topic_info(self,value):
        self.controller.args_dict['Planning_Controls']['Pose_topic'] = value


    def save_imu_topic_info(self,value):
        self.controller.args_dict['Planning_Controls']['IMU_topic'] = value

    def save_imu_type(self):
        imu_type_map = {0: "ISO-8855", 1: "SAE-J670"}
        imu_type = self.imu_frame_type_selection.get()
        self.controller.args_dict['Planning_Controls']['IMU_frame_type'] = imu_type_map[int(imu_type)]

    def save_control_topic_single(self,value):
        self.controller.args_dict['Planning_Controls']['Control_topic'] = value


    def save_control_topic_vel(self,value):
        self.controller.args_dict['Planning_Controls']['Velocity_topic'] = value

    def save_control_topic_steering(self,value):
        self.controller.args_dict['Planning_Controls']['Steering_topic'] = value


    def save_planner_type(self):
        planner_type_map = {0: "Curvature_based", 1: "Load_transfer_based"}
        planner_type = self.radio_var_planner_type.get()
        self.controller.args_dict['Planning_Controls']['Planner_type'] = planner_type_map[int(planner_type)]


    '''Validation Functions'''

    # Validation function to check if input is two integers seselected_velocity_topicparated by a space
    def validate_input_cost(self,input_str):
        try:
            # Split the input by spaces and check if there are exactly two integers
            parts = input_str.split()
            if len(parts) == 2 and all(part.isdigit() for part in parts):
                return True
            return False
        except ValueError:
            return False

    def validate_input_horizon(self, input_str):
        try:
            # Attempt to convert the input string to a float
            float_val = float(input_str)
            return True
        except ValueError:
            # If conversion to float fails, return False
            return False

    # Function to show a warning dialog
    def show_warning_cost(self,field_name):
        messagebox.showwarning("Input Error",
                               f"Invalid input for {field_name}. Please enter two integers separated by a space.")

    def show_warning_horizon(self,field_name):
        messagebox.showwarning("Input Error",
                               f"Invalid input for {field_name}. Please enter 1 float value denoting preview in seconds.")


    '''Page switch'''

    def next_page(self):
        # print(self.controller.args_dict)
        next_frame = self.controller.show_frame("Deploy")
        # self.update_idletasks()
        # if hasattr(next_frame, 'print_arg_var'):
        #     next_frame.print_arg_var()
        if hasattr(next_frame, 'refresh'):
                next_frame.refresh()
        if hasattr(next_frame,'test_trajectory_selection_pane'):
            next_frame.test_trajectory_selection_pane()


    def previous_page(self):
        self.controller.show_frame("Modeling")
        self.update_idletasks()