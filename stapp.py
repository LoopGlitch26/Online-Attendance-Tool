import cv2, time, os, face_recognition, streamlit as st, mysql.connector
from datetime import datetime
import datetime
from PIL import Image

# Create an encoding for the known image of the student
known_image = face_recognition.load_image_file("/Users/loopglitch/Desktop/me.jpg")
original_encoding = face_recognition.face_encodings(known_image)[0]

st.header("Student Companion for Attendance")
name=st.text_input("Enter your Name")
classID=st.text_input("Enter Course ID")
email=st.text_input("Enter your Email")
min =st.number_input("Enter the duration of the meeting in MINUTES", step=1.0)

now = datetime.datetime.now()
start_time = now.strftime("%H:%M")
reg=st.text_input("Enter registration ID")

capture_frequency=10 #Intervals of frame capture in seconds
cap = cv2.VideoCapture(0)# Set webcam as video capture device
i=1;FaceFound=0 # intitialise variables for counters
TotalPictures=int(min*60/capture_frequency)# Calculate total frames captured in a given duration
threshold=int(round(0.7*TotalPictures)) #Keeping threshold at 70%
flag=0

while (cap.isOpened() and i<=min*60/capture_frequency):
    ret, frame = cap.read()
    if ret == False:
        break
    img_path = '/Users/loopglitch/aot/img_folder/unknown' + str(i) + '.jpg'
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
        # Code to compare the face in captured frame with given student image
        unknown_image = face_recognition.load_image_file(img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([original_encoding], unknown_encoding)

        if (results[0] == True): # If face is successfully recognisedv
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            st.write("Student recognised at TIME ", current_time)
            FaceFound += 1
        else: # If face is not recognised but a face is present
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            st.write("ANOTHER PERSON found at TIME", current_time)
    i+=1
    time.sleep(capture_frequency) # delays the execution by 10 seconds/makes the thread sleep

flag=1
# Displaying the results of attendance to user
st.header("Detection Metrics")
st.write("FaceRecognised",FaceFound)
st.write("Total capture",TotalPictures)

# Keep today's date in variable x
# _____________________________________
x = datetime.datetime.now()
today_date=str(x.strftime("%d-%m-%Y"))
# ______________________________________

if(FaceFound>threshold):
    st.write("PRESENT")
    att="PRESENT"
else:
    st.write("ABSENT")
    att="ABSENT"


# SQL Integration
@st.cache
def insertBLOB(reg, name, email, classID, Date, start_time, att):
    mydb = mysql.connector.connect(host="sql12.freemysqlhosting.net", database="sql12396097", user="sql12396097", password="cfjfrv3qcA")
    my_cursor = mydb.cursor()
    sql_insert_blob_query = "INSERT INTO attendancelist (reg, name, email, classID, date, time, status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    # Convert data into tuple format
    insert_blob_tuple = (reg, name, email, classID, Date, start_time, att)
    result = my_cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    mydb.commit()
    print("Entry updated successfully in Attendance table")

try:
    insertBLOB(reg, name, email, classID, today_date, start_time, att)
    st.success("Successfully Inserted")
except:
    st.warning("Enter your details")

cap.release()
cv2.destroyAllWindows()

