import os
import json
from deepface import DeepFace
import psycopg2


"""
Description:
    Connect to PostgreSQL and
    store face embeddings.

Args:
    None

Returns:
    None
"""


def connect_db():

    """
    Description:
        Create PostgreSQL connection.

    Args:
        None

    Returns:
        connection object
    """

    connection = psycopg2.connect(

        host="localhost",
        port="5432",
        database="face_recognition_db",
        user="postgres",
        password="1234"
    )

    return connection


def save_embeddings():

    connection = connect_db()

    cursor = connection.cursor()

    dataset_folder = "dataset"

    for person_name in os.listdir(
            dataset_folder
    ):

        person_path = os.path.join(
            dataset_folder,
            person_name
        )

        if not os.path.isdir(
                person_path
        ):
            continue

        print(
            f"\nProcessing {person_name}"
        )

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
                    Generate face embedding.

                Args:
                    image path

                Returns:
                    face vector
                """

                embedding = DeepFace.represent(

                    img_path=image_path,

                    model_name="Facenet",

                    enforce_detection=False
                )

                vector = embedding[0][
                    "embedding"
                ]

                """
                Description:
                    Store embedding as JSON.

                Args:
                    vector

                Returns:
                    database insert
                """

                query = """

                INSERT INTO people
                (
                    name,
                    image_name,
                    embedding
                )

                VALUES
                (
                    %s,
                    %s,
                    %s
                )

                """

                cursor.execute(

                    query,

                    (
                        person_name,
                        image_name,
                        json.dumps(vector)
                    )
                )

                connection.commit()

                print(
                    f"Saved: {image_name}"
                )

            except Exception as error:

                print(error)

    cursor.close()

    connection.close()


if __name__ == "__main__":

    save_embeddings()