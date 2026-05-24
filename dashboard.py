import os
import shutil

import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine
from sqlalchemy import text

from streamlit_autorefresh import st_autorefresh

from admin_registration import register_user
from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image
from streamlit_webrtc import webrtc_streamer
from live_attendance import video_frame_callback
import base64

def autoplay_audio(
        file_path
):

    with open(

            file_path,

            "rb"

    ) as file:

        data=file.read()


    b64=base64.b64encode(

        data

    ).decode()


    md=f"""

    <audio autoplay>

    <source

    src="data:audio/mp3;base64,{b64}"

    type="audio/mp3">

    </audio>

    """


    st.markdown(

        md,

        unsafe_allow_html=True

    )
st.set_page_config(

    page_title="SSIEMS Face Recognition Dashboard",

    layout="wide"

)




st_autorefresh(

    interval=5000,

    key="dashboard_refresh"

)




if "logged_in" not in st.session_state:

    st.session_state.logged_in = False





def connect_db():

    engine = create_engine(

        "postgresql://postgres:1234@localhost:5432/face_recognition_db"

    )

    return engine





def authenticate(

        username,
        password

):

    engine = connect_db()

    connection = engine.connect()

    query = text(
        """

        SELECT *

        FROM admin_users

        WHERE

        username=:username

        AND

        password=:password

        """
    )

    result = connection.execute(

        query,

        {

            "username":
            username,

            "password":
            password

        }

    ).fetchone()

    connection.close()

    return result is not None





def load_users():

    engine = connect_db()

    query = """

    SELECT

        name,
        employee_id,
        department,
        email

    FROM people_master

    ORDER BY name

    """

    dataframe = pd.read_sql(

        query,

        engine

    )

    engine.dispose()

    return dataframe





def load_attendance():

    engine = connect_db()

    query = """

    SELECT

        employee_id,
        name,
        event_type,
        attendance_date,
        log_time

    FROM attendance_logs

    ORDER BY log_time DESC

    """

    dataframe = pd.read_sql(

        query,

        engine

    )

    engine.dispose()

    return dataframe


def load_unknown_faces():

    engine = connect_db()

    query = """

    SELECT

        image_path,
        detected_at

    FROM unknown_faces

    ORDER BY detected_at DESC

    """

    dataframe = pd.read_sql(

        query,

        engine

    )

    engine.dispose()

    return dataframe


if not st.session_state.logged_in:

    st.title(

        "Admin Login"

    )

    username = st.text_input(

        "Username"

    )

    password = st.text_input(

        "Password",

        type="password"

    )

    if st.button(

            "Login"

    ):

        if authenticate(

                username,

                password

        ):

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error(

                "Invalid credentials"

            )

    st.stop()




st.sidebar.title(

    "Admin Panel"

)


if st.sidebar.button(

        "Logout"

):

    st.session_state.logged_in = False

    st.rerun()


page = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",

        "Register User",

        "Manage Users",

        "Unknown Faces",

        "Live Attendance"

    ]

)




if page == "Register User":

    st.title(
        "Student Registration"
    )

    name = st.text_input(
        "Student Name"
    )

    employee_id = st.text_input(
        "Student ID"
    )

    email = st.text_input(
        "Email"
    )

    department = st.text_input(
        "Department/Class"
    )


    if "embeddings" not in st.session_state:

        st.session_state.embeddings=[]


    st.subheader(
        "Camera"
    )


    image = st.camera_input(
        "Open Camera"
    )


    if image:

        image_file = Image.open(
            image
        )

        frame = np.array(
            image_file
        )

        frame = cv2.cvtColor(

            frame,

            cv2.COLOR_RGB2BGR

        )


        st.image(

            frame,

            channels="BGR"

        )


        try:

            embedding = DeepFace.represent(

                img_path=frame,

                model_name="Facenet",

                enforce_detection=False

            )


            vector=np.array(

                embedding[0][
                    "embedding"
                ]

            )


            if len(
                    st.session_state.embeddings
            ) < 5:

                st.session_state.embeddings.append(

                    vector

                )


                st.success(

                    f"Captured "

                    f"{len(st.session_state.embeddings)}/5"

                )


                st.progress(

                    len(
                        st.session_state.embeddings
                    )/5

                )

        except:

            st.warning(
                "Face not detected"
            )


    if st.button(
            "Complete Registration"
    ):

        if len(
                st.session_state.embeddings
        ) < 5:

            st.warning(
                "Waiting for 5 captures"
            )

        else:

            average = np.mean(

                st.session_state.embeddings,

                axis=0

            )


            success,message=register_user(

                name,

                employee_id,

                email,

                department,

                average

            )


            if success:

                st.success(
                    message
                )

            else:

                st.warning(
                    message
                )


            st.session_state.embeddings=[]




if page == "Dashboard":

    st.title(

        "SSIEMS Face Recognition Dashboard"

    )

    users = load_users()

    attendance = load_attendance()

    col1,col2,col3=st.columns(3)


    with col1:

        st.metric(

            "Registered Users",

            len(users)

        )


    with col2:

        st.metric(

            "Attendance Records",

            len(attendance)

        )


    with col3:

        today_count=len(

            attendance[

                attendance[
                    "attendance_date"
                ]

                ==

                pd.Timestamp.today().date()

            ]

        )

        st.metric(

            "Today's Events",

            today_count

        )


    st.divider()


    st.subheader(

        "IN / OUT Distribution"

    )


    chart=px.histogram(

        attendance,

        x="event_type"

    )


    st.plotly_chart(

        chart,

        width="stretch"

    )


    st.divider()


    st.subheader(

        "Registered Users"

    )


    st.dataframe(

        users,

        width="stretch"

    )


    st.divider()


    st.subheader(

        "Attendance History"

    )


    st.dataframe(

        attendance,

        width="stretch"

    )


    st.divider()


    st.subheader(

        "Student Attendance Lookup"

    )


    student_list=users[

        "name"

    ].unique()


    selected_student=st.selectbox(

        "Select Student",

        student_list

    )


    student_history=attendance[

        attendance[
            "name"
        ]

        ==

        selected_student

    ]


    if len(

        student_history

    )>0:


        col1,col2=st.columns(2)


        with col1:

            total_in=len(

                student_history[

                    student_history[
                        "event_type"
                    ]

                    ==

                    "IN"

                ]

            )


            st.metric(

                "Total IN",

                total_in

            )


        with col2:

            total_out=len(

                student_history[

                    student_history[
                        "event_type"
                    ]

                    ==

                    "OUT"

                ]

            )


            st.metric(

                "Total OUT",

                total_out

            )


        st.dataframe(

            student_history,

            width="stretch"

        )


    else:

        st.warning(

            "No attendance found"

        )

    st.divider()

    st.subheader(

        "Attendance History"

    )

    st.dataframe(

        attendance,

        width="stretch"

    )




if page == "Manage Users":

    st.title(

        "Manage Users"

    )

    users = load_users()

    if len(users) == 0:

        st.warning(

            "No users found"

        )

    else:

        selected_user = st.selectbox(

            "Select User",

            users["name"]

        )

        selected_data = users[

            users["name"]
            ==
            selected_user

        ].iloc[0]


        updated_name = st.text_input(

            "Name",

            selected_data["name"]

        )

        updated_emp = st.text_input(

            "Employee ID",

            selected_data["employee_id"]

        )

        updated_email = st.text_input(

            "Email",

            selected_data["email"]

        )

        updated_department = st.text_input(

            "Department",

            selected_data["department"]

        )


        col1, col2 = st.columns(2)


        with col1:

            if st.button(

                    "Update User"

            ):

                engine = connect_db()

                connection = engine.connect()

                query = text(
                    """

                    UPDATE people_master

                    SET

                    name=:name,

                    employee_id=:emp,

                    email=:email,

                    department=:dept

                    WHERE

                    name=:old_name

                    """
                )

                connection.execute(

                    query,

                    {

                        "name":
                        updated_name,

                        "emp":
                        updated_emp,

                        "email":
                        updated_email,

                        "dept":
                        updated_department,

                        "old_name":
                        selected_user

                    }

                )

                connection.commit()

                connection.close()

                st.success(

                    "User Updated"

                )


        with col2:

            if st.button(

                    "Delete User"

            ):

                engine = connect_db()

                connection = engine.connect()

                query = text(
                    """

                    DELETE

                    FROM people_master

                    WHERE

                    name=:name

                    """
                )

                connection.execute(

                    query,

                    {

                        "name":
                        selected_user

                    }

                )

                connection.commit()

                connection.close()

                dataset_folder = (

                    f"dataset/{selected_user}"

                )

                if os.path.exists(

                        dataset_folder

                ):

                    shutil.rmtree(

                        dataset_folder

                    )

                st.success(

                    "User Deleted"

                )

                st.rerun()
if page == "Unknown Faces":

    st.title(
        "Unknown Face Logs"
    )

    unknown_data = load_unknown_faces()


    if len(unknown_data)==0:

        st.warning(
            "No unknown faces detected"
        )

    else:

        for _, row in unknown_data.iterrows():

            st.image(

                row["image_path"],

                width=300

            )

            st.write(

                f"Detected: "

                f"{row['detected_at']}"

            )

            st.divider()

if page=="Live Attendance":

    st.title(
        "Live Gate Camera"
    )

    webrtc_streamer(

        key="attendance",

        video_frame_callback=
        video_frame_callback,

        media_stream_constraints={

            "video":True,

            "audio":False

        }

    )