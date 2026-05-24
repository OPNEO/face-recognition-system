import psycopg2
from datetime import datetime,timedelta


"""
    Description:
        Connect PostgreSQL

    Args:
        None

    Returns:
        connection
"""


def connect_db():

    return psycopg2.connect(

        host="localhost",
        port="5432",
        database="face_recognition_db",
        user="postgres",
        password="1234"

    )


"""
    Description:
        Toggle attendance.

    Args:
        employee_id(str)
        name(str)

    Returns:
        str
"""


def mark_attendance(
        employee_id,
        name
):

    connection=connect_db()

    cursor=connection.cursor()

    cursor.execute(
        """

        SELECT

            event_type,
            log_time

        FROM attendance_logs

        WHERE

            employee_id=%s

            AND attendance_date=
            CURRENT_DATE

        ORDER BY log_time DESC

        LIMIT 1

        """,

        (employee_id,)

    )


    result=cursor.fetchone()


    """
        Description:
            Avoid duplicate scans
            within 1 minute.
    """


    if result:

        last_event,last_time=result


        if (

            datetime.now()
            -
            last_time

        ) < timedelta(

            minutes=1

        ):

            cursor.close()

            connection.close()

            return None


        if last_event=="IN":

            new_event="OUT"

        else:

            new_event="IN"

    else:

        new_event="IN"


    cursor.execute(
        """

        INSERT INTO attendance_logs(

            employee_id,
            name,
            event_type

        )

        VALUES(

            %s,
            %s,
            %s

        )

        """,

        (

            employee_id,

            name,

            new_event

        )

    )


    connection.commit()


    print(

        f"{name} : {new_event}"

    )


    cursor.close()

    connection.close()


    return new_event