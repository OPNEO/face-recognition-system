import os
import cv2
import numpy as np
import psycopg2

from deepface import DeepFace
from psycopg2.extras import Json
from sklearn.metrics.pairwise import cosine_similarity


"""
Description:
    Connect to PostgreSQL database.

Args:
    None

Returns:
    PostgreSQL connection
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
    Check whether face already exists.

Args:
    new_embedding (numpy array)

Returns:
    tuple:
        (
            exists,
            matched_name
        )
"""


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

        existing_vector = np.array(
            existing_embedding
        )

        score = cosine_similarity(

            new_embedding.reshape(
                1,
                -1
            ),

            existing_vector.reshape(
                1,
                -1
            )

        )[0][0]

        """
        Description:
            Face similarity threshold.

        Args:
            None

        Returns:
            duplicate match
        """

        if score > 0.75:

            return (

                True,

                existing_name

            )

    return (

        False,

        None

    )


"""
Description:
    Register a new user.

Args:
    name (str)
    employee_id (str)
    email (str)
    department (str)

Returns:
    tuple:
        (
            success,
            message
        )
"""


def register_user(

        name,
        employee_id,
        email,
        department
):

    folder = os.path.join(
        "dataset",
        name
    )

    os.makedirs(

        folder,

        exist_ok=True
    )

    camera = cv2.VideoCapture(
        0
    )

    detector = cv2.CascadeClassifier(

        "haarcascade_frontalface_default.xml"

    )

    image_count = 0

    embeddings = []

    MAX_IMAGES = 10

    while image_count < MAX_IMAGES:

        success, frame = camera.read()

        if not success:
            continue

        gray = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2GRAY
        )

        faces = detector.detectMultiScale(

            gray,

            1.1,

            5
        )

        for (

                x,
                y,
                w,
                h

        ) in faces:

            face = frame[

                y:y+h,

                x:x+w

            ]

            filename = os.path.join(

                folder,

                f"{image_count}.jpg"

            )

            cv2.imwrite(

                filename,

                face
            )

            embedding = DeepFace.represent(

                img_path=face,

                model_name="Facenet",

                enforce_detection=False

            )

            vector = np.array(

                embedding[0][
                    "embedding"
                ]

            )

            embeddings.append(
                vector
            )

            image_count += 1

            cv2.rectangle(

                frame,

                (x, y),

                (x+w, y+h),

                (0,255,0),

                2
            )

            cv2.putText(

                frame,

                f"Captured:{image_count}/{MAX_IMAGES}",

                (20,40),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (0,255,0),

                2
            )

        cv2.imshow(

            "Registration",

            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break

    camera.release()

    cv2.destroyAllWindows()

    if len(embeddings) == 0:

        return (

            False,

            "No face detected"

        )

    """
    Description:
        Create average embedding.

    Args:
        embeddings

    Returns:
        average vector
    """

    average = np.mean(

        embeddings,

        axis=0
    )

    exists, matched_person = face_exists(

        average

    )

    if exists:

        return (

            False,

            f"Face already registered as {matched_person}"

        )

    connection = connect_db()

    cursor = connection.cursor()

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