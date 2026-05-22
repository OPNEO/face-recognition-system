import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh
from admin_registration import register_user
import shutil
from sqlalchemy import text
import os
"""
Description:
    Auto refresh dashboard.

Args:
    None

Returns:
    None
"""

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)


"""
Description:
    Configure Streamlit page.

Args:
    None

Returns:
    None
"""

st.set_page_config(

    page_title="Face Recognition Dashboard",

    layout="wide"
)


"""
Description:
    Create SQLAlchemy engine.

Args:
    None

Returns:
    SQLAlchemy engine
"""


def connect_db():

    engine = create_engine(

        "postgresql://postgres:1234@localhost:5432/face_recognition_db"

    )

    return engine


"""
Description:
    Load registered users.

Args:
    None

Returns:
        DataFrame
"""


def load_users():

    connection = connect_db()

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
        connection
    )

    connection.dispose()

    return dataframe


"""
Description:
    Load attendance.

Args:
    None

Returns:
        DataFrame
"""


def load_attendance():

    connection = connect_db()

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
        connection
    )

    connection.dispose()

    return dataframe


"""
Description:
    Sidebar navigation

Args:
    None

Returns:
    None
"""

st.sidebar.title(
    "Admin Panel"
)

page = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",

        "Register User",

        "Manage Users"

    ]
)


"""
Description:
    Register page

Args:
    None

Returns:
    None
"""


if page == "Register User":

    st.title(
        "User Registration"
    )

    name = st.text_input(
        "Name"
    )

    employee_id = st.text_input(
        "Employee ID"
    )

    email = st.text_input(
        "Email"
    )

    department = st.text_input(
        "Department"
    )


    if st.button(
            "Start Face Registration"
    ):

        if (

                not name
                or
                not employee_id
                or
                not email
                or
                not department

        ):

            st.error(
                "Fill all fields"
            )

        else:

            with st.spinner(

                "Opening camera..."
            ):

                success, message = register_user(

                    name,
                    employee_id,
                    email,
                    department
                )

                if success:

                    st.success(
                        message
                    )

                else:

                    st.warning(
                        message
                    )


"""
Description:
    Dashboard page

Args:
    None

Returns:
    None
"""


if page == "Dashboard":

    st.title(
        "Face Recognition Dashboard"
    )

    users = load_users()

    attendance = load_attendance()


    col1, col2, col3 = st.columns(
        3
    )


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

        today_count = len(

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

    chart = px.histogram(

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


    search = st.text_input(

        "Search Employee"

    )


    if search:

        filtered = users[

            users[
                "name"
            ].str.contains(

                search,

                case=False
            )

        ]

        st.dataframe(

            filtered,

            width="stretch"
        )

        """
Description:
    Admin user management.

Args:
    None

Returns:
    None
"""


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

            users["name"] ==
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

                    WHERE name=:old_name

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
                    "Updated"
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

                    f"dataset/"
                    f"{selected_user}"

                )

                if os.path.exists(

                        dataset_folder
                ):

                    shutil.rmtree(

                        dataset_folder

                    )


                st.success(
                    "User deleted"
                )