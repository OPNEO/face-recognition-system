import psycopg2
import numpy as np

from psycopg2.extras import Json
from sklearn.metrics.pairwise import cosine_similarity


def connect_db():

    return psycopg2.connect(

        host="localhost",
        port="5432",
        database="face_recognition_db",
        user="postgres",
        password="1234"

    )


def face_exists(
        new_embedding
):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """

        SELECT
            name,
            embedding

        FROM people_master

        """
    )

    records = cursor.fetchall()

    cursor.close()

    connection.close()


    for (

        existing_name,
        existing_embedding

    ) in records:

        existing_vector=np.array(

            existing_embedding

        )


        score=cosine_similarity(

            new_embedding.reshape(
                1,
                -1
            ),

            existing_vector.reshape(
                1,
                -1
            )

        )[0][0]


        if score > 0.75:

            return (

                True,

                existing_name

            )


    return (

        False,

        None

    )


def register_user(

        name,

        employee_id,

        email,

        department,

        average

):

    exists,matched_person=face_exists(

        average

    )


    if exists:

        return (

            False,

            f"Face already registered as {matched_person}"

        )


    connection=connect_db()

    cursor=connection.cursor()


    cursor.execute(
        """

        INSERT INTO people_master(

            name,
            employee_id,
            email,
            department,
            embedding

        )

        VALUES(

            %s,
            %s,
            %s,
            %s,
            %s

        )

        ON CONFLICT(name)

        DO NOTHING

        """,

        (

            name,

            employee_id,

            email,

            department,

            Json(
                average.tolist()
            )

        )

    )


    connection.commit()

    cursor.close()

    connection.close()


    return (

        True,

        "Registration completed"

    )