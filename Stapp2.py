# master code:

import streamlit as st, mysql.connector

st.title("Welcome")
import streamlit as st

add_selectbox = st.sidebar.selectbox(
    "NAVIGTION",
    ("Student Registration", "Faculty Registration","Student Dashboard","Faculty Dashboard","Attendance Capture Tool")
)
if(add_selectbox=="Student Registration"):
    import streamlit as st, pyrebase, mysql.connector, cv2
    import os
    import PIL.Image
    from PIL.Image import Image

    k = os.path.exists("temp")
    if (k == False):
        os.mkdir("temp")
    st.header("Student Registration")
    Name = st.text_input("Name")
    Email = st.text_input("Email")
    reg = st.text_input("Registration Number")
    password = st.text_input("Password", type="password")
    password_check = st.text_input("Re enter Password", type="password")
    if (password != password_check):
        st.warning("Passwords don't match")
    known_img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if ((st.button("Submit") == True) and password == password_check):

        def convertToBinaryData(filename):
            # Convert digital data to binary format
            with open(filename, 'rb') as file:
                binaryData = file.read()
            return binaryData


        def insertBLOB(reg_num, Name, Email, Photo, password):
            mydb = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
            my_cursor = mydb.cursor()
            sql_insert_blob_query = "INSERT INTO registration (Reg, NAME, EMAIL, Photo, password) VALUES (%s,%s,%s,%s,%s)"
            converted_picture = convertToBinaryData(Photo)
            # Convert data into tuple format
            insert_blob_tuple = (reg_num, Name, Email, converted_picture, password)
            result = my_cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            mydb.commit()
            print("Image inserted successfully as a BLOB into students table", result)


        def save_uploadedfile(uploadedfile):
            with open(os.path.join("temp", uploadedfile.name), "wb") as f:
                f.write(uploadedfile.getbuffer())  # Writes the file to directory Local
            insertBLOB(reg, Name, Email, 'temp/{}'.format(uploadedfile.name),
                       password)  # Calls function to insert the photo and details into SQL
            return st.success("Successfully Registered")


        if (known_img != None):
            save_uploadedfile(known_img)
elif(add_selectbox=="Faculty Registration"):

    # ------------------Subject Config---------------------------------
    subject_ID = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']
    subject_config = ['MTH1001', 'CSE1001', 'EET1001', 'CHM1001', 'ENG1001']
    # ------------------Subject Config---------------------------------

    st.header("Faculty Registration")
    Name = st.text_input("Name")
    Email = st.text_input("Email")
    reg = st.text_input("Enter Faculty ID")
    password = st.text_input("Password", type="password")
    password_check = st.text_input("Re enter Password", type="password")
    if (password != password_check):
        st.warning("Passwords don't match")

    classID = st.selectbox("Select your subject", subject_config)
    if ((st.button("Submit") == True) and password == password_check):
        idx = subject_config.index(classID)
        classID = subject_ID[idx]
        def facultyregistration(Reg, Name, Email, Password, Subject):
            mydb = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
            my_cursor = mydb.cursor()
            sql_insert_blob_query = "INSERT INTO facultyreg (Reg, Name, Email,Password, Subject) VALUES (%s,%s,%s,%s,%s)"
            insert_blob_tuple = (Reg, Name, Email,Password, Subject)
            result = my_cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            mydb.commit()
        facultyregistration(reg, Name, Email, password, classID)
        st.success("You are registered")


elif(add_selectbox=="Student Dashboard"):
    import mysql.connector, streamlit as st

    # ------------------Subject Config---------------------------------
    subject_ID = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']
    subject_config = ['MTH1001', 'CSE1001', 'EET1001', 'CHM1001', 'ENG1001']
    # ------------------Subject Config---------------------------------

    st.header("Student Dashboard")
    reg = st.text_input("Enter your registrationID")
    password = st.text_input("Enter your password", type="password")
    classID = st.selectbox("Select your subject", subject_config)


    def password_validate(password):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_validate = "select password FROM registration where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        return result[0][0]


    def findstudent(reg):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_validate = "select NAME FROM registration where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        st.write("The details are")
        for x in result:
            st.write("Name:", x[0])


    def findattendance1(reg, subject_num):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_attendance_subject = "select * from `{subject}` where reg={registration}".format(subject=subject_num,
                                                                                             registration=reg)
        cursor.execute(sql_attendance_subject)
        result = cursor.fetchall()
        st.write("Attendance for:", classID)
        count = 0;
        total_present = 0;
        # print(result[0][1])
        for k in result[0]:
            count += 1
            if (k == '1'):
                total_present += 1

        st.write("Total classes", count - 1)
        st.write("Total present", total_present)
        st.write("Attendance Percentage", round((total_present / (count - 1) * 100), 2))


    if ((st.button("Submit") == True)):
        if (password == password_validate(reg)):
            st.success("Sucessfully Logged In")
            findstudent(reg)
            idx = subject_config.index(classID)
            classID_mapped = subject_ID[idx]
            findattendance1(reg, classID_mapped)
        else:
            st.error("Incorrect RegID or Password")

elif(add_selectbox=="Faculty Dashboard"):
    import mysql.connector, streamlit as st

    # ------------------Subject Config---------------------------------
    subject_ID = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']
    subject_config = ['MTH1001', 'CSE1001', 'EET1001', 'CHM1001', 'ENG1001']
    # ------------------Subject Config---------------------------------

    st.header("Faculty Dashboard")
    reg = st.text_input("Enter your Faculty ID")
    password = st.text_input("Enter your password", type="password")


    # ----------Coverts subject1 to MTH1001-------------------------------
    def subject_mapping(sub):
        idx = subject_ID.index(sub)
        return subject_config[idx]


    # -----------------------------------------------------------------------

    # -----------------Validate Password------------------------------------------------------------------
    def password_validate(password):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_validate = "select Password FROM facultyreg where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        return result[0][0]


    # -----------------------------------------------------------------------------------------------------

    # ----------------------Find Student Name--------------------------------------------------------------
    def findstudent(reg):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_validate = "select NAME FROM registration where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        # st.write("The details are")
        for x in result:
            return x[0]


    # -------------------------------------------------------------------------------------------------------

    # -------------------------------Finding Faculty and their subject---------------------------------------
    def find_faculty_and_subject(reg):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_validate = "select Name, Subject FROM facultyreg where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        st.write("The details are")
        for x in result:
            st.write("Name:", x[0])
            st.write("Subject:", subject_mapping(x[1]))
        return x[1]


    # -------------------------------------------------------------------------------------------------------

    # ----------------------------Find All students' attendance-----------------------------------------------
    def findattendance(subject_num):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_attendance_subject = "select * from `{subject}`".format(subject=subject_num)
        cursor.execute(sql_attendance_subject)
        result = cursor.fetchall()
        st.write("Attendance for:", )
        for entry in result:
            st.write(findstudent(entry[0]))
            findattendancepercent(entry[0], subject_num)


    # ----------------------------------------------------------------------------------------------------------

    def findattendancepercent(reg, subject_num):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_attendance_subject = "select * from `{subject}` where reg={registration}".format(subject=subject_num,
                                                                                             registration=reg)
        cursor.execute(sql_attendance_subject)
        result = cursor.fetchall()
        # st.write("Attendance for:")
        count = 0;
        total_present = 0
        for k in result[0]:
            count += 1
            if (k == '1'):
                total_present += 1
        # st.write("Total classes", count-1)
        st.write("Present", total_present, "out of", count - 1, "classes", "Attendance Percentage",
                 round((total_present / (count - 1) * 100), 2))
        # st.write("Attendance Percentage", round((total_present/(count-1)*100),2))


    def show_All_attendance():
        # if (st.button("Show All Attendance")):
        findattendance(subject_encoded)


    if ((st.button("Submit") == True)):
        if (password == password_validate(reg)):
            st.success("Sucessfully Logged In")
            subject_encoded = find_faculty_and_subject(reg)
            show_All_attendance()
        else:
            st.error("Incorrect RegID or Password")
else:
    import cv2, time, os, face_recognition, streamlit as st, pyrebase, mysql.connector
    from datetime import datetime, timedelta
    import datetime
    from PIL import Image
    k = os.path.exists("temp")
    if (k == False):
        os.mkdir("temp")


    def clear_dir():
        filelist = [f for f in os.listdir("temp") if f.endswith(".jpg")]
        for f in filelist:
            os.remove(os.path.join("temp", f))


    clear_dir()


    # --------------------------------HighLight Faces--------------------------------------------
    def mark_faces(path):
        if k == '1':
            G = 255;
            R = 0;
        else:
            G = 0;
            R = 255
        image = face_recognition.load_image_file(path)
        face_locations = face_recognition.face_locations(image)
        image1 = cv2.imread(path, cv2.COLOR_BGR2RGB)
        for top, right, bottom, left in face_locations:
            image1 = cv2.rectangle(image, (left, top), (right, bottom), (R, G, 0), 3)
        RGB_img = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        cv2.imwrite('temp/face_highlight.jpg', RGB_img)
        disp_img = Image.open('temp/face_highlight.jpg')  # Loads the image from given path
        img_area.image(disp_img, width=300, caption="Current capture")


    # --------------------------------HighLight Faces-------------------------------------------------

    def write_file(data, filename):
        with open(filename, 'wb') as file:
            file.write(data)


    # Code to extract image from student registration database
    # --------- Extract Photo-------------------------------------------------------------------------
    def readBLOB(reg, filename):
        print("Reading BLOB image data from registration table")
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_fetch_blob_query = "SELECT Photo FROM registration WHERE Reg = %s"
        cursor.execute(sql_fetch_blob_query, (reg,))
        image = cursor.fetchone()[0]
        write_file(image, filename)
        cursor.close()
        connection.close()


    # ------------------------------ Validate Student------------------------------------------------------------
    def findstudent(reg):
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_validate = "select NAME, EMAIL FROM registration where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        st.write("The details are")
        for x in result:
            st.write("Name:", x[0])
            st.write("Email:", x[1])


    # -----------------------------Student Regularity Check---------------------------------------------------

    def isregular(reg, subject_num):
        from datetime import datetime, timedelta
        d = datetime.today() - timedelta(days=1)
        yesterday_date = str(d.strftime("%d-%m-%Y"))
        connection = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
        cursor = connection.cursor()
        sql_find_attendance = "select `{date}` from `{subject}` where Reg={registration}".format(date=yesterday_date,
                                                                                                 subject=subject_num,
                                                                                                 registration=reg)
        cursor.execute(sql_find_attendance)
        result = cursor.fetchall()
        for x in result:
            return x[0]


    # ------------------Subject Config---------------------------------
    subject_ID = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']
    subject_config = ['MTH1001', 'CSE1001', 'EET1001', 'CHM1001', 'ENG1001']
    # ------------------Subject Config---------------------------------

    st.header("Student Companion for Attendance")
    # name=st.text_input("Enter your Name")
    # classID = (st.text_input("Enter Course ID")).upper()
    classID = st.selectbox("Select your subject", subject_config)
    # email=st.text_input("Enter your Email")
    # min =st.number_input("Enter the duration of the meeting in MINUTES", step=1.0)
    min = 1  # Setting default values of class

    now = datetime.datetime.now()
    start_time = now.strftime("%H:%M")
    reg = st.text_input("Enter registration ID")
    if (st.button("Submit") == True):
        # ___________________________
        try:
            findstudent(reg)
            readBLOB(reg, "temp\\me.jpg")
        except:
            st.error("Student isn't registered")

        # ___________________________
        try:
            idx = subject_config.index(classID)
            classID = subject_ID[idx]
        except:
            st.error("Please enter valid Course ID")

        k = isregular(reg, classID)  # k=1 if student is present in previous class else 0

        # Code to take known image from Offline System directory
        # Create an encoding for the known image of the student
        known_image = face_recognition.load_image_file("temp\\me.jpg")
        original_encoding = face_recognition.face_encodings(known_image)[0]

        capture_frequency = 10  # Intervals of frame capture in seconds
        cap = cv2.VideoCapture(0)  # Set webcam as video capture device
        i = 1;
        FaceFound = 0  # intitialise variables for counters
        TotalPictures = int(min * 60 / capture_frequency)  # Calculate total frames captured in a given duration
        threshold = int(round(0.7 * TotalPictures))  # Keeping threshold at 70%
        flag = 0
        img_area = st.empty()  # Placeholder for image area
        while (cap.isOpened() and i <= min * 60 / capture_frequency):
            ret, frame = cap.read()
            if ret == False:
                break
            img_path = 'temp\\unknown' + str(i) + '.jpg'
            cv2.imwrite(img_path, frame)

            # disp_img = Image.open(img_path) # Loads the image from given path
            # img_area.image(disp_img,width=300, caption="Current capture") # Displays the image in area of placeholder img_area

            # mark_faces(img_path)

            image = face_recognition.load_image_file(img_path)
            face_locations = face_recognition.face_locations(image)

            if not face_locations:  # in case no face locations are returned i.e., []
                disp_img = Image.open(img_path)  # Loads the image from given path
                img_area.image(disp_img, width=300,
                               caption="Current capture")  # Displays the image in area of placeholder img_area
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                st.write("No face detected at TIME", current_time)

            else:
                # Code to compare the face in captured frame with given student image
                unknown_image = face_recognition.load_image_file(img_path)
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.compare_faces([original_encoding], unknown_encoding)

                if (results[0] == True):  # If face is successfully recognised
                    mark_faces(img_path)
                    now = datetime.datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    st.write("Student recognised at TIME ", current_time)
                    FaceFound += 1

                else:  # If face is not recognised but a face is present
                    disp_img = Image.open(img_path)  # Loads the image from given path
                    img_area.image(disp_img, width=300,
                                   caption="Current capture")  # Displays the image in area of placeholder img_area
                    now = datetime.datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    st.write("ANOTHER PERSON found at TIME", current_time)
            i += 1
            time.sleep(capture_frequency)  # delays the execution by 10 seconds/makes the thread sleep

        flag = 1
        # Displaying the results of attendance to user
        st.header("Detection Metrics")
        st.write("FaceRecognised", FaceFound)
        st.write("Total capture", TotalPictures)

        # Keep today's date in variable x
        # _____________________________________
        x = datetime.datetime.now()
        today_date = str(x.strftime("%d-%m-%Y"))
        # ______________________________________

        if (FaceFound > threshold):
            st.write("PRESENT")
            att = 1
        else:
            st.write("ABSENT")
            att = 0


        # SQL Integration

        def insertBLOB(Reg, today_date, att, subject_num):
            mydb = mysql.connector.connect(host="sql6.freemysqlhosting.net", database="sql6409330", user="sql6409330", password="dvjW6YhuvB")
            my_cursor = mydb.cursor()
            try:
                # To insert a row into the table with reg no. as primary key
                sql_insert = "INSERT INTO {subject} (Reg) VALUES ({registration})".format(subject=subject_num,
                                                                                          registration=Reg)
                print(sql_insert)
                my_cursor.execute(sql_insert)
            except:
                print("Already present")
            # To create a columm of a certain date
            sql_create_column = "ALTER TABLE {subject} ADD `{day}` varchar(20)".format(subject=subject_num,
                                                                                       day=today_date)
            # To update an existing column with the attendance
            sql_insert_blob_query = "update {subject} set `{day}`={attendance} where Reg={registration}".format(
                subject=subject_num, day=today_date, attendance=att, registration=Reg)
            try:
                my_cursor.execute(sql_create_column)
            except:
                print("the date column already exists")
            finally:
                my_cursor.execute(sql_insert_blob_query)
                mydb.commit()
                print("Entry updated successfully in Attendance table")


        insertBLOB(reg, today_date, att, classID)

        # Delete the files in temporary folder after the end of class
        clear_dir()
        # Close the webcam
        cap.release()
        cv2.destroyAllWindows()




# SQL commands



# To create a table for faculty registration:

# create table facultyreg (Reg INT NOT NULL PRIMARY KEY, Name varchar(30) NOT NULL, Email varchar(30) NOT NULL, Password varchar(30) NOT NULL, Subject varchar(20));



# To create a table for student registration:

# create table registration (Reg INT NOT NULL PRIMARY KEY, NAME varchar(30) NOT NULL, EMAIL varchar(30) NOT NULL,Photo LONGBLOB, password varchar(30) NOT NULL);



# To create a table for each subject:

# create table subject1 (Reg INT NOT NULL PRIMARY KEY);
# create table subject2 (Reg INT NOT NULL PRIMARY KEY);
# create table subject3 (Reg INT NOT NULL PRIMARY KEY);
# create table subject4 (Reg INT NOT NULL PRIMARY KEY);
# create table subject5 (Reg INT NOT NULL PRIMARY KEY);








###

