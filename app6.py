import streamlit as st
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd
import json
from typing import Dict, List, Tuple

# Set page config
st.set_page_config(page_title="Face Recognition Attendance System", layout="wide")

# Load student metadata
@st.cache_resource
def load_student_metadata() -> Dict[str, Dict[str, str]]:
    with open('student_metadata.json', 'r') as f:
        return json.load(f)

student_metadata = load_student_metadata()

# Directory containing images
path = 'images/'

# Load and encode images
@st.cache_data
def load_images() -> Tuple[List[np.ndarray], List[str]]:
    images = []
    classNames = []
    for cl in os.listdir(path):
        img = cv2.imread(f'{path}/{cl}')
        if img is not None:
            images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            classNames.append(os.path.splitext(cl)[0])
    return images, classNames

images, classNames = load_images()

# Find face encodings
@st.cache_data
def find_encodings(images: List[np.ndarray]) -> List[np.ndarray]:
    return [face_recognition.face_encodings(img)[0] for img in images if len(face_recognition.face_encodings(img)) > 0]

encode_list_known = find_encodings(images)

# Initialize session state
if 'captured_students' not in st.session_state:
    st.session_state.captured_students = []

# Streamlit UI
st.title("Face Recognition Attendance System")

# Sidebar for course details
with st.sidebar:
    st.header("Course Details")
    course_name = st.text_input("Course Name")
    course_code = st.text_input("Course Code")

# Main content
if course_name and course_code:
    st.subheader(f"Attendance for {course_name} ({course_code})")
    
    # Camera input
    camera_image = st.camera_input("Capture Student")

    if camera_image is not None:
        # Convert the image to numpy array
        image = cv2.imdecode(np.frombuffer(camera_image.getvalue(), np.uint8), cv2.IMREAD_COLOR)
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Find faces in the frame
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        # Process each detected face
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(encode_list_known, face_encoding)
            face_distances = face_recognition.face_distance(encode_list_known, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                image_name = f"{classNames[best_match_index]}.jpg"
                if image_name in student_metadata:
                    name = student_metadata[image_name]["name"]
                    student_id = student_metadata[image_name]["id"]
                else:
                    name = classNames[best_match_index].upper()
                    student_id = f"Unknown-{best_match_index:03d}"
                
                # Check if student is already captured
                if student_id not in [s['id'] for s in st.session_state.captured_students]:
                    st.session_state.captured_students.append({
                        "name": name,
                        "id": student_id,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                
                # Draw rectangle and name on the image
                top, right, bottom, left = face_location
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(image, f"{name} ({student_id})", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        # Display the processed image
        st.image(image, channels="BGR", use_column_width=True)

    # Display captured students
    if st.session_state.captured_students:
        st.subheader("Captured Students")
        for student in st.session_state.captured_students:
            st.write(f"{student['name']} ({student['id']}) - Captured at {student['time']}")

    # Generate Attendance button
    if st.button("Generate Attendance"):
        if st.session_state.captured_students:
            # Create DataFrame
            df = pd.DataFrame(st.session_state.captured_students)
            df = df.rename(columns={"name": "Student Name", "id": "Student ID", "time": "Time of Attendance"})
            
            # Add course details
            df = pd.concat([pd.DataFrame([{"Student Name": f"Course: {course_name}", "Student ID": f"Code: {course_code}", "Time of Attendance": datetime.now().strftime("%Y-%m-%d")}]), df])
            
            # Save to Excel
            excel_file = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(excel_file, index=False)
            
            # Provide download link
            with open(excel_file, "rb") as file:
                st.download_button(
                    label="Download Attendance Sheet",
                    data=file,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            st.success(f"Attendance generated for {len(st.session_state.captured_students)} students.")
        else:
            st.warning("No students captured yet. Please capture students before generating attendance.")

else:
    st.info("Please enter Course Name and Course Code in the sidebar to start capturing attendance.")

# Instructions
st.sidebar.markdown("---")
st.sidebar.subheader("Instructions")
st.sidebar.markdown("""
1. Enter the Course Name and Course Code in the sidebar.
2. Use the camera to capture each student.
3. Captured students will be listed below the camera.
4. Click 'Generate Attendance' when all students are captured.
5. Download the attendance sheet.
""")

# Reset session
if st.sidebar.button("Reset Session"):
    st.session_state.captured_students = []
    st.success("Session reset. All captured students cleared.")