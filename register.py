import os
import cv2


"""
Description:
    Register a person by capturing face images
    from webcam and saving cropped face images.

Args:
    None

Returns:
    None
"""


def register_face():

    """
    Description:
        Ask user name and create
        dataset folder.

    Args:
        None

    Returns:
        person_name (str)
        person_folder (str)
    """

    person_name = input(
        "Enter name to register: "
    ).strip()

    person_folder = os.path.join(
        "dataset",
        person_name
    )

    os.makedirs(
        person_folder,
        exist_ok=True
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print(
            "ERROR: Camera not found"
        )

        return

    face_detector = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml"
    )

    image_count = 0

    MAX_IMAGES = 20

    print("\nRegistration Started...")
    print(
        "Move your face slightly "
        "for different angles"
    )

    while True:

        """
        Description:
            Read webcam frame.

        Args:
            None

        Returns:
            success (bool)
            frame
        """

        success, frame = camera.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100,100)
        )

        for (x, y, w, h) in faces:

            """
            Description:
                Crop only face region.

            Args:
                frame coordinates

            Returns:
                face image
            """

            face = frame[
                y:y+h,
                x:x+w
            ]

            image_count += 1

            filename = os.path.join(
                person_folder,
                f"{person_name}_{image_count}.jpg"
            )

            cv2.imwrite(
                filename,
                face
            )

            cv2.rectangle(
                frame,
                (x,y),
                (x+w,y+h),
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
            "Face Registration",
            frame
        )

        """
        Description:
            Stop after enough images
            or user presses q.

        Args:
            keyboard input

        Returns:
            None
        """

        if image_count >= MAX_IMAGES:

            print(
                "\nRegistration completed"
            )

            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()

    cv2.destroyAllWindows()

    print("\nSaved images:")

    for file in os.listdir(
        person_folder
    ):
        print(file)


if __name__ == "__main__":
    register_face()