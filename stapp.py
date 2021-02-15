"""
INSTALLATION GUIDE

Activate the virtual environment : source venv/bin/activate
Installation : 
pip3 install face_recognition
pip3 install opencv-python
pip3 install pyrebase
pip install mysql-connector-python
pip3 install streamlit

"""

import cv2, time, os, face_recognition, streamlit as st, pyrebase, mysql.connector
from datetime import datetime
import datetime

#Firebase configuration SECRET
firebaseConfig = {
    'apiKey': "AIzaSyAltyq3D5_TW8GluZ4goEBmwP2kGD41vY8",
    'authDomain': "attendancesystem-1c820.firebaseapp.com",
    'databaseURL': "https://attendancesystem-1c820-default-rtdb.firebaseio.com",
    'projectId': "attendancesystem-1c820",
    'storageBucket': "attendancesystem-1c820.appspot.com",
    'messagingSenderId': "1064805715401",
    'appId': "1:1064805715401:web:c2d8aab5ca364f12022c18",
    'measurementId': "G-5TFT24ZJ55"
  };

from PIL import Image
# Create an encoding for the known image of the student
known_image = face_recognition.load_image_file("") # PLEASE ENTER THE PATH TO YOUR IMAGE FOR FACE RECOGNITION
original_encoding = face_recognition.face_encodings(known_image)[0]


st.header("Student Companion for Attendance")
name=st.text_input("Enter your Name")
reg=st.text_input("Enter registration ID")
classID=st.text_input("Enter class ID")
min =st.number_input("Enter the duration of the meeting in MINUTES", step=1.0)
capture_frequency=10 #Intervals of frame capture in seconds
cap = cv2.VideoCapture(0)
i=1;FaceFound=0
TotalPictures=int(min*60/capture_frequency)
threshold=int(round(0.8*TotalPictures)) #Keeping threshold at 80%
while (cap.isOpened() and i<=min*60/capture_frequency):
    ret, frame = cap.read()
    if ret == False:
        break
    img_path = '/unknown' + str(i) + '.jpg' # PLEASE ENTER THE PATH WHERE YOU WANT TO STORE THE IMAGES TAKEN FOR FACE RECOGNITION BY THIS WEBAPP
    cv2.imwrite(img_path, frame)

    image = face_recognition.load_image_file(img_path)
    face_locations = face_recognition.face_locations(image)
   # img = Image.open(img_path)  # To load the latest captured image from the path
   # st.image(img, caption="Latest capture")  # display latest image
    if not face_locations:  # in case no face locations are returned i.e., []
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        st.write("No face detected at TIME", current_time)
    else:
        unknown_image = face_recognition.load_image_file(img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([original_encoding], unknown_encoding)

        if (results[0] == True):
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            st.write("Student recognised at TIME ", current_time)
            FaceFound += 1
        else:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            st.write("ANOTHER PERSON found at TIME", current_time)
    i+=1
    time.sleep(capture_frequency) # delays the execution by 10 seconds/makes the thread sleep

st.header("Detection Metrics")
st.write("FaceRecognised",FaceFound)
st.write("Total capture",TotalPictures)

# Keep today's date in variable x
# _____________
x = datetime.datetime.now()
today_date=str(x.strftime("%d-%m-%Y"))
# ______________

if(FaceFound>threshold):
    st.write("PRESENT")
    att="PRESENT"
else:
    st.write("ABSENT")
    att="ABSENT"

# Database Implementation
firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
data = {'name': name, 'class': classID, 'Date': today_date, "Attendance": att}
db.child("Students").child(reg).push(data)




cap.release()
cv2.destroyAllWindows()