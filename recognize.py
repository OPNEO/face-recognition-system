import cv2
import psycopg2
import numpy as np

from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
from attendance import mark_attendance

"""
Description:
    Connect to PostgreSQL database.

Args:
    None

Returns:
    PostgreSQL connection object
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
    Load all stored embeddings
    from PostgreSQL.

Args:
    None

Returns:
    list
"""


def load_faces():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
        name,
        employee_id,
        department,
        email,
        embedding
        FROM people_master
        """
    )

    records = cursor.fetchall()

    cursor.close()

    connection.close()

    face_data = []

    for name, employee_id, department, email, embedding in records:

        """
        Description:
            PostgreSQL JSONB already returns
            Python list objects.

        Args:
            embedding (list)

        Returns:
            numpy vector
        """

        vector = np.array(
            embedding
        )

        face_data.append(

        (
            name,
            employee_id,
            department,
            email,
            vector
        )

    )

    return face_data


"""
Description:
    Start recognition webcam.

Args:
    None

Returns:
    None
"""


def recognize_face():

    known_faces = load_faces()

    print(
        f"Loaded "
        f"{len(known_faces)} "
        f"embeddings"
    )

    camera = cv2.VideoCapture(0)
    last_detected_name = None

    detector = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml"
    )

    while True:

        success, frame = camera.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            face = frame[
                y:y+h,
                x:x+w
            ]

            try:

                embedding = DeepFace.represent(

                    img_path=face,

                    model_name="Facenet",

                    enforce_detection=False

                )

                current_vector = np.array(

                    embedding[0][
                        "embedding"
                    ]

                ).reshape(1,-1)

                best_name = "Unknown"
                best_score = 0
                best_emp = "N/A"
                best_dept = "Unknown"
                best_email = "N/A"

                for (
                        name,
                        employee_id,
                        department,
                        email,
                        stored_vector
                ) in known_faces:

                    score = cosine_similarity(

                        current_vector,

                        stored_vector.reshape(
                            1,
                            -1
                        )

                    )[0][0]

                    if score > best_score:

                        best_score = score
                        best_name = name
                        best_emp = employee_id
                        best_dept = department
                        best_email = email
                

                if best_score < 0.60:

                    best_name = "Unknown"
                    best_emp = "N/A"
                    best_dept = "Unknown"
                    best_email = "N/A"
                
                if (
                        best_name != "Unknown"
                        and best_name != last_detected_name
                ):

                    mark_attendance(
                        best_emp,
                        best_name
                    )

                    last_detected_name = best_name


                label1 = f"{best_name}"
                label2 = f"{best_emp}"
                label3 = f"{best_dept}"

                cv2.rectangle(

                    frame,

                    (x,y),

                    (x+w,y+h),

                    (0,255,0),

                    2
                )

                cv2.putText(
                    frame,
                    label1,
                    (x, y-30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    label2,
                    (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,255),
                    2
                )

                cv2.putText(
                    frame,
                    label3,
                    (x, y+20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,255),
                    2
                )
                

            except Exception:

                pass

        cv2.imshow(
            "Recognition",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    recognize_face()