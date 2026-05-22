import os
import numpy as np
import psycopg2
from deepface import DeepFace
from psycopg2.extras import Json


"""
Description:
    Create PostgreSQL connection.

Args:
    None

Returns:
    connection object
"""


def connect_db():

    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="face_recognition_db",
        user="postgres",
        password="1234"
    )

    return connection


"""
Description:
    Create one average embedding
    for each registered person.

Args:
    None

Returns:
    None
"""


def build_master_embeddings():

    connection = connect_db()

    cursor = connection.cursor()

    dataset_folder="dataset"

    for person_name in os.listdir(
        dataset_folder
    ):

        print(
            f"\nRegistering {person_name}"
        )

        employee_id = input(
            "Employee ID: "
        )

        email = input(
            "Email: "
        )

        department = input(
            "Department: "
        )

        person_path=os.path.join(
            dataset_folder,
            person_name
        )

        all_vectors=[]

        for image_name in os.listdir(
            person_path
        ):

            image_path = os.path.join(
                person_path,
                image_name
            )

            try:

                """
                Description:
                    Generate embedding
                    from image.

                Args:
                    image path

                Returns:
                    vector
                """

                embedding = DeepFace.represent(

                    img_path=image_path,

                    model_name="Facenet",

                    enforce_detection=False
                )

                vector = np.array(

                    embedding[0][
                        "embedding"
                    ]

                )

                all_vectors.append(
                    vector
                )

                print(
                    f"Processed: {image_name}"
                )

            except Exception as error:

                print(error)

        if len(all_vectors) == 0:
            continue

        """
        Description:
            Average vectors.

        Args:
            all vectors

        Returns:
            one master vector
        """

        average_vector = np.mean(
            all_vectors,
            axis=0
        )

        cursor.execute(
            """
            INSERT INTO people_master
            (
                name,
                employee_id,
                email,
                department,
                embedding
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )

            ON CONFLICT (name)

            DO UPDATE

            SET embedding=
            EXCLUDED.embedding
            """,

            (
                person_name,
                employee_id,
                email,
                department,
                Json(
                    average_vector.tolist()
                )
            )
        )

        connection.commit()

        print(
            f"Saved master: "
            f"{person_name}"
        )

    cursor.close()

    connection.close()


if __name__ == "__main__":

    build_master_embeddings()