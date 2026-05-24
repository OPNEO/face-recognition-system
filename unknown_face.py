import psycopg2


def save_unknown(
        image_path
):

    connection=psycopg2.connect(

        host="localhost",

        database="face_recognition_db",

        user="postgres",

        password="1234"

    )

    cursor=connection.cursor()

    cursor.execute(

        """

        INSERT INTO unknown_faces(

            image_path

        )

        VALUES(

            %s

        )

        """,

        (

            image_path,

        )

    )

    connection.commit()

    cursor.close()

    connection.close()