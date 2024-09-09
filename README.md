# Face-Recognition-Attendance-System
A computer vission system to mark student attendance with name and Index number through a Recognition System

# Face Recognition Attendance System

## Overview
This project is a **Face Recognition Attendance System** built using **Streamlit**. The system allows the detection and recognition of students' faces in real time through a camera, captures their attendance, and stores the results in an Excel sheet. The system compares faces detected from the camera input against a pre-loaded dataset of known faces and generates an attendance report for the course.

## Features
- Real-time face recognition using camera input.
- Attendance tracking based on recognized faces.
- Ability to reset the session and start a new attendance capture.
- Generates an Excel sheet of attendance records, including the time of attendance.
- Course name and course code entry for record association.
- Simple and user-friendly interface with instructions provided.

## Installation and Requirements
1. Clone the repository.
2. Install the required Python packages:
   
   ```pip install streamlit opencv-python numpy face-recognition pandas```
4. Place your images (labeled with student names) in the `images/` directory.
5. Create a `student_metadata.json` file with student information, where the keys are the image filenames and values are student details in the following format:
   ```{
       "student_image.jpg": {
           "name": "John Doe",
           "id": "12345"
       }
   }```

## Running the Application
Run the following command to start the Streamlit app:
streamlit run app.py
Once the app is running, you can:
1. Enter the course name and course code in the sidebar.
2. Use the camera to capture students' faces.
3. Recognized students' names and IDs will be shown along with the time of capture.
4. Generate the attendance report by clicking the **Generate Attendance** button.
5. Download the generated attendance sheet in Excel format.

## Usage
- **Course Details**: Enter the course name and code in the sidebar.
- **Camera Input**: Capture each student using the camera interface.
- **Generate Attendance**: Once all students have been captured, generate the attendance sheet.
- **Reset Session**: Clear the captured students and restart the attendance process.

## Instructions
1. Enter the Course Name and Course Code in the sidebar.
2. Capture each student's face using the camera.
3. The system will display the captured students and their attendance time.
4. Click 'Generate Attendance' to download the Excel sheet.
5. Use the reset button to start a new session.

## Reset Functionality
If you need to restart the process, you can reset the session by clicking the **Reset Session** button in the sidebar. This will clear all captured students and allow you to start fresh.

## License
This project is open-source and available under the MIT License.

---

Enjoy using the **Face Recognition Attendance System**!
