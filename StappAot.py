# Importing mandatory Dependencies
import streamlit as st, mysql.connector, cv2, os, face_recognition, time, re, sys
from PIL.Image import Image

st.title("Welcome")
# ------------------Subject Config-------------------------------------
subject_ID = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']
subject_config = ['MTH1001', 'CSE1001', 'EET1001', 'CHM1001', 'ENG1001']
# ------------------Subject Config--------------------------------------

# Navigation toolbar to go to pages
add_selectbox = st.sidebar.selectbox(
    "NAVIGATION",  # Title of sidebar
    (
        "Student Registration", "Faculty Registration", "Student Dashboard", "Faculty Dashboard",
        "Attendance Capture Tool")
    # List of all options in sidebar
)

# ----------Creates a temporary folder----------
def CreateTempDir():
    k = os.path.exists("temp")
    if not k:
        os.mkdir("temp")

# ---------------------------------------------
CreateTempDir()

# -------------------Validate Email, Name, RegistrationID---------------------------

def email_check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.]\w{2,3}$)|(\w+[.]\w+[.]\w{2,3}$)'
    if (re.search(regex, email)):
        return True
    else:
        return False

def name_check(name):
    regex='^[A-Za-z\s]+$'
    if(re.search(regex,name)):
        return True
    else:
        return False

def reg_check(reg):
    regex='^[0-9]+$'
    if(re.search(regex,reg)):
        return True
    else:
        return False
# -------------------------------------------------------------------------------

# ++++++++++++++++++++STUDENT REGISTRATION+++++++++++++++++++++++++++++++

if add_selectbox == "Student Registration":
    st.header("Student Registration")

    # ------------Input fields--------------------------------------------
    Name = st.text_input("Name")
    Email = st.text_input("Email")
    reg = st.text_input("Registration Number")
    password = st.text_input("Password", type="password")
    password_check = st.text_input("Re enter Password", type="password")
    if password != password_check:  # Check whether the entered passwords match
        st.warning("Passwords don't match")

    # Email Verification------------------------------------------------------
    import pyrebase, time, streamlit as st

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

    # auth.delete_user_account(user['idToken']) ---------A code snippet
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()


    @st.cache(suppress_st_warning=True)
    def once():
        email =Email
        password = password_check
        if (email != None and password != None):
            user = auth.create_user_with_email_and_password(email, password)
            st.info('Verification link sent to your email')
            auth.send_email_verification(user['idToken'])
            return user
    try:
        once()
    except:
        pass


    def isemailverified():
        user = once()
        k = auth.get_account_info(user['idToken'])
        verify_status = ((k['users'])[0])['emailVerified']
        return verify_status  # Return True or False


    # st.write('You need to verify your email please check your inbox. ')
    v = st.button('I agree that I\'ve verified my email')
    if (v == True):
        while (isemailverified() != True):
            st.write('Sorry, you haven\'t verified your email, Please verify\n and wait ')
            time.sleep(7)
        if (isemailverified()):
            st.success('You have successfully verified your email')


    #-------------------------------------------------------------------------------

    known_img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    # ------------ Input fields---------------------------------------------
    if st.button("Submit") and password == password_check and isemailverified():
        if not name_check(Name):
            st.warning("Invalid Name")
            sys.exit()
        elif not email_check(Email):
            st.warning("Invalid Email")
            sys.exit()
        elif not reg_check(reg):
            st.warning("Invalid Registration ID")
            sys.exit()
        elif not known_img:
            st.warning("Input an image")
            sys.exit()
        elif not password:
            st.warning("Password must be set")
            sys.exit()
        else:
            st.balloons()

        # ------Convert digital data to binary format----------
        def convertToBinaryData(filename):
            with open(filename, 'rb') as file:
                binaryData = file.read()
            return binaryData


        # ------------------------------------------------------

        # --------------------------------------------SQL Code to insert data------------------------------------------
        def insertBLOB(reg_num, Name, Email, Photo, password):
            mydb = mysql.connector.connect(host="localhost", database="giraffe", user="root", password="1234")
            my_cursor = mydb.cursor()
            sql_insert_blob_query = "INSERT INTO registration (Reg, NAME, EMAIL, Photo, password) VALUES (%s,%s,%s,%s,%s)"
            converted_picture = convertToBinaryData(Photo)
            # Convert data into tuple format
            insert_blob_tuple = (reg_num, Name, Email, converted_picture, password)
            result = my_cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            mydb.commit()
            print("Image inserted successfully as a BLOB into students table", result)


        # ------------------------------------------SQL Code to Insert Data--------------------------------------------

        # --------- Pass the uploaded file through streamlit to SQL----------------
        def save_uploadedfile(uploadedfile):
            with open(os.path.join("temp", uploadedfile.name), "wb") as f:
                f.write(uploadedfile.getbuffer())  # Writes the file to directory Local
            # Calls function to insert the photo and details into SQL
            insertBLOB(reg, Name, Email, 'temp/{}'.format(uploadedfile.name), password)
            return st.success("Successfully Registered")


        # -------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        if (known_img != None):
            save_uploadedfile(known_img)

# ++++++++++++++++++++FACULTY REGISTRATION+++++++++++++++++++++++++++++++
elif add_selectbox == "Faculty Registration":

    st.header("Faculty Registration")
    # ------------Input fields--------------------------------------
    Name = st.text_input("Name")
    Email = st.text_input("Email")
    reg = st.text_input("Enter Faculty ID")
    password = st.text_input("Password", type="password")
    password_check = st.text_input("Re enter Password", type="password")
    if password != password_check:  # Checks if entered passwords match
        st.warning("Passwords don't match")
    classID = st.selectbox("Select your subject", subject_config)
    auth = st.text_input("Enter Authorisation Code",type='password')
    # -------------Input fields--------------------------------------
    if (st.button("Submit") == True) and password == password_check:
        idx = subject_config.index(classID)
        classID = subject_ID[idx]

        if not name_check(Name):
            st.warning("Invalid Name")
            sys.exit()
        elif not email_check(Email):
            st.warning("Invalid Email")
            sys.exit()
        elif not reg_check(reg):
            st.warning("Invalid Faculty ID")
            sys.exit()
        elif not password:
            st.warning("Password must be set")
            sys.exit()
        elif not auth:
            st.warning("Enter the auth code")
            sys.exit()

        # -------------------------------SQL Code for faculty registration--------------------------------------------
        def facultyregistration(Reg, Name, Email, Password, Subject):
            mydb = mysql.connector.connect(host="localhost", database="giraffe", user="root", password="1234")
            my_cursor = mydb.cursor()
            sql_insert_blob_query = "INSERT INTO facultyreg (Reg, Name, Email,Password, Subject) VALUES (%s,%s,%s,%s,%s)"
            insert_blob_tuple = (Reg, Name, Email, Password, Subject)
            result = my_cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            mydb.commit()


        # -------------------------------SQL Code for faculty registration-------------------------------------------
        if(auth=='1020SOA'):
            facultyregistration(reg, Name, Email, password, classID)
            st.success("You are registered")
            st.balloons()


# ++++++++++++++++++++ STUDENT DASHBOARD ++++++++++++++++++++++++++++++++
elif add_selectbox == "Student Dashboard":

    st.header("Student Dashboard")
    # ------------Input fields--------------------------------------
    reg = st.text_input("Enter your registrationID")
    password = st.text_input("Enter your password", type="password")
    classID = st.selectbox("Select your subject", subject_config)


    # ------------Input fields--------------------------------------

    # --------- Extract password from student registration database-------------------
    def password_validate(password):
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_validate = "select password FROM registration where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        return result[0][0]


    # -------------Extract password from student registration database-----------------

    # --------------Extract student name from registration database-------------------------------------------
    def findstudent(reg):
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_validate = "select NAME FROM registration where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        st.write("The details are")
        for x in result:
            st.write("Name:", x[0])


    # -------------Extract student name from registration database-----------------------------------------

    # --------------Find attendance for a given reg no. ------------------------------------------------------
    def findattendance1(reg, subject_num):
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
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


    # -----------Find attendance for a given reg no. ---------------------------------------------------------

    if st.button("Submit") == True:
        if password == password_validate(reg):  # Checks whether the entered password matches
            st.success("Successfully Logged In")
            findstudent(reg)  # Extracts student's name from database
            idx = subject_config.index(classID)  # Maps subject number to subject CODE
            classID_mapped = subject_ID[idx]
            findattendance1(reg, classID_mapped)  # Finds attendance for a student
        else:
            st.error("Incorrect RegID or Password")

# ++++++++++++++++++++ FACULTY DASHBOARD ++++++++++++++++++++++++++++++++
elif add_selectbox == "Faculty Dashboard":

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
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_validate = "select Password FROM facultyreg where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        return result[0][0]


    # -----------------------------------------------------------------------------------------------------

    # ----------------------Find Student Name--------------------------------------------------------------
    def findstudent(reg):
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
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
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_validate = "select Name, Subject FROM facultyreg where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        st.write("The details are")
        for x in result:
            st.write("Name:", x[0])
            st.write("Subject:", subject_mapping(x[1]))
        return x[1]


    # This function prints faculty name and subject. It returns subject_number
    # --------------------------------------------------------------------------------------------------------

    # ----------------------------Find All students' attendance-----------------------------------------------
    def findattendance(subject_num):
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_attendance_subject = "select * from `{subject}`".format(subject=subject_num)
        cursor.execute(sql_attendance_subject)
        result = cursor.fetchall()
        st.write("Attendance for:", )
        for entry in result:
            st.write(findstudent(entry[0]))  # Shows student name
            findattendancepercent(entry[0], subject_num)  # Finds attendance percent


    # ----------------------------------------------------------------------------------------------------------

    # ------------------------Find attendance for each student with percentage-------------------------------
    def findattendancepercent(reg, subject_num):
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_attendance_subject = "select * from `{subject}` where reg={registration}".format(subject=subject_num,
                                                                                             registration=reg)
        cursor.execute(sql_attendance_subject)
        result = cursor.fetchall()
        count = 0;
        total_present = 0
        for k in result[0]:
            count += 1
            if (k == '1'):
                total_present += 1
        st.write("Present", total_present, "out of", count - 1, "classes", "Attendance Percentage",
                 round((total_present / (count - 1) * 100), 2))
        # -----------------------Find attendance for each student with percentage---------------------------


    # Calls another function findattendance with input as subject_encoded
    def show_All_attendance():
        findattendance(subject_encoded)


    if st.button("Submit"):
        if password == password_validate(reg):
            st.success("Successfully Logged In")
            subject_encoded = find_faculty_and_subject(reg)  # Subject encoded stores the subject of a given faculty
            show_All_attendance()
        else:
            st.error("Incorrect RegID or Password")

# ++++++++++++++++++++ ATTENDANCE TOOL ++++++++++++++++++++++++++++++++++
else:
    import cv2, time, os, face_recognition, streamlit as st, pyrebase, mysql.connector
    from datetime import datetime, timedelta
    import datetime
    from PIL import Image

    CreateTempDir()  # Create a Temporary Directory


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
        image = face_recognition.load_image_file(path)  # loads the image from path
        face_locations = face_recognition.face_locations(image)  # finds the locations of the face
        image1 = cv2.imread(path, cv2.COLOR_BGR2RGB)  # Converts the color to RGB from default BGR in OpenCV
        for top, right, bottom, left in face_locations:
            image1 = cv2.rectangle(image, (left, top), (right, bottom), (R, G, 0), 3)  # creates a rectangle on face
        RGB_img = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)  # Keeps the RGB image
        cv2.imwrite('temp/face_highlight.jpg',
                    RGB_img)  # Writes the RGB image with face highlighted into temp directory
        disp_img = Image.open('temp/face_highlight.jpg')  # Loads the image from given path
        img_area.image(disp_img, width=300, caption="Current capture")  # Displays the image in streamlit


    # --------------------------------HighLight Faces END-----------------------------------------------

    def write_file(data, filename):
        with open(filename, 'wb') as file:
            file.write(data)


    # Code to extract image from student registration database
    # --------- Extract Photo-------------------------------------------------------------------------
    def readBLOB(reg, filename):
        print("Reading BLOB image data from registration table")
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_fetch_blob_query = "SELECT Photo FROM registration WHERE Reg = %s"
        cursor.execute(sql_fetch_blob_query, (reg,))
        image = cursor.fetchone()[0]
        write_file(image, filename)
        cursor.close()
        connection.close()


    # ------------------------------ Validate Student------------------------------------------------------------
    def findstudent(reg):
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_validate = "select NAME, EMAIL FROM registration where Reg={}".format(reg)
        cursor.execute(sql_validate)
        result = cursor.fetchall()
        st.write("The details are")
        for x in result:
            st.write("Name:", x[0])
            st.write("Email:", x[1])


    # -----------------------------Student Regularity Check---------------------------------------------------
    # Checks whether the student was present in the previous class
    def isregular(reg, subject_num):
        from datetime import datetime, timedelta
        d = datetime.today() - timedelta(days=1)  # Finds yesterday's date
        yesterday_date = str(d.strftime("%d-%m-%Y"))  # Keeps yesterday's date as a formatted string
        connection = mysql.connector.connect(host='localhost', database='giraffe', user='root', password='1234')
        cursor = connection.cursor()
        sql_find_attendance = "select `{date}` from `{subject}` where Reg={registration}".format(date=yesterday_date,
                                                                                                 subject=subject_num,
                                                                                                 registration=reg)
        cursor.execute(sql_find_attendance)
        result = cursor.fetchall()
        for x in result:
            return x[0]  # returns '1' or '0'


    # -----------------------------------------------------------------------------------------------------------

    st.header("Student Companion for Attendance")
    classID = st.selectbox("Select your subject", subject_config)
    # min =st.number_input("Enter the duration of the meeting in MINUTES", step=1.0)
    min = 1  # Setting default values of class

    now = datetime.datetime.now()
    start_time = now.strftime("%H:%M")
    reg = st.text_input("Enter registration ID")
    if st.button("Submit"):

        try:
            findstudent(reg)
            readBLOB(reg, "temp\\me.jpg")
        except:
            st.error("Student isn't registered")
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
        threshold = int(round(0.75 * TotalPictures))  # Keeping threshold at 75%
        flag = 0
        img_area = st.empty()  # Placeholder for image area
        while (cap.isOpened() and i <= min * 60 / capture_frequency):
            ret, frame = cap.read()
            if ret == False:
                break
            img_path = 'temp\\unknown' + str(i) + '.jpg'
            cv2.imwrite(img_path, frame)

            image = face_recognition.load_image_file(img_path)
            face_locations = face_recognition.face_locations(image)

            if not face_locations:  # in case no face locations are returned i.e., []
                disp_img = Image.open(img_path)  # Loads the image from given path
                img_area.image(disp_img, width=300,
                               caption="Current capture - NO FACE")  # Displays the image in area of placeholder img_area
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                st.write("No face detected at TIME", current_time)

            else:
                # Code to compare the face in captured frame with given student image
                unknown_image = face_recognition.load_image_file(img_path)
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.compare_faces([original_encoding], unknown_encoding, tolerance=0.5)

                if (results[0] == True):  # If face is successfully recognised
                    mark_faces(img_path)  # Calls the function which highlights the face location in Green and Red
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
            mydb = mysql.connector.connect(host="localhost", database="giraffe", user="root", password="1234")
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
