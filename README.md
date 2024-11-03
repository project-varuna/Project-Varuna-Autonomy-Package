# Project Varuna

Project Varuna is a versatile framework for modeling, planning, and control of autonomous vehicles, leveraging the Koopman Operator Theory for explainable, data-driven models. This guide will walk you through the setup and usage of Project Varuna, including the steps for navigating the user interface.

![Main](Images/Project-Varuna-Overview.png)

## Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed along with ROS1 noetic.

### Installation

1. **Clone the Repository**  
   First, clone this repository:
   ```bash
   git clone https://github.com/yourusername/Project-Varuna.git
   cd Project-Varuna

2. **Download the package file**  
   Download the latest package file from the [Releases](https://github.com/project-varuna/Project-Varuna-Autonomy-Package/releases) page and place it in the repository's root directory.

3. **Install Requirements**  
   Install the dependencies, primarily `customtkinter` for the front-end application:

   ```bash
   pip install -r requirements.txt

## Running the Application  
To launch the Project Varuna front-end interface, run:

```bash
python3 Project-Varuna-GUI.py
```

---
## Usage Guide  

Once the application is running, follow these key steps for a seamless experience with modeling, planning, and control tasks in Project Varuna.

### Navigating the User Interface
The user application consists of 3 sections for modeling, planning/ controls and deployment.
Following instructions highlight this process:

#### Data Selection & Platform Setup
![Screen1](Images/Project_Varuna_GUI_main.png)


- Select training data or pretrained models from the interface.
- Load your test data and specify the platform for deployment.

#### Configure Motion Planning and Control Parameters
![Screen2](Images/Project_Varuna_GUI_2.png)

- Choose your motion planner and adjust Model Predictive Control (MPC) penalties to optimize performance.
- Set relevant ROS topics based on your chosen platform for system integration.
- Select topics for:
  - **Localized pose**: Can be of type `Point` or `Pose 2D`.
  - **IMU data**: For tracking the vehicle's attitude.
  - **Control topics**: Either using `Twist` messages or decoupled throttle and steering messages with the `Float` message type.

#### Execute Path Tracking
![Screen2](Images/Project_Varuna_GUI_3.png)
- Pick your desired path, configure final settings, and initiate the execution to begin path tracking.

Now, you're ready to go!


## Contact

For questions, feedback, or support, please reach out to the Project Varuna team:

- **Email**: [ajinkya.projectvaruna@gmail.com](ajinkya.projectvaruna@gmail.com)
- **GitHub Issues**: For any bug reports or feature requests, use the [issue tracker](https://github.com/yourusername/Project-Varuna/issues).
- **Contributors**: If you’d like to collaborate or discuss larger contributions, feel free to reach out directly!
