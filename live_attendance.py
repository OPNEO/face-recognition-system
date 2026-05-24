import av
import cv2
import numpy as np

from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity

from recognize import load_faces
from attendance import mark_attendance
import winsound
recent_faces={}


def video_frame_callback(
        frame
):

    img=frame.to_ndarray(
        format="bgr24"
    )


    detector=cv2.CascadeClassifier(

        "haarcascade_frontalface_default.xml"

    )


    gray=cv2.cvtColor(

        img,

        cv2.COLOR_BGR2GRAY

    )


    faces=detector.detectMultiScale(

        gray,

        scaleFactor=1.1,

        minNeighbors=5

    )


    known_faces=load_faces()


    for (x,y,w,h) in faces:

        face=img[
            y:y+h,
            x:x+w
        ]

        try:

            embedding=DeepFace.represent(

                img_path=face,

                model_name="Facenet",

                enforce_detection=False

            )

            current=np.array(

                embedding[0][
                    "embedding"
                ]

            ).reshape(
                1,
                -1
            )

            best_name="Unknown"

            best_score=0

            best_emp="N/A"


            for (

                    name,
                    emp,
                    dept,
                    email,
                    vector

            ) in known_faces:


                score=cosine_similarity(

                    current,

                    vector.reshape(
                        1,
                        -1
                    )

                )[0][0]


                if score>best_score:

                    best_score=score

                    best_name=name

                    best_emp=emp


            if best_score<0.60:

                best_name="Unknown"


            cv2.rectangle(

                img,

                (x,y),

                (x+w,y+h),

                (0,255,0),

                2

            )


            cv2.putText(

                img,

                best_name,

                (x,y-10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0,255,0),

                2

            )


            if best_name!="Unknown":

                event=mark_attendance(

                    best_emp,

                    best_name

                )


                if event:

                    winsound.PlaySound(

                        "sounds\\success.wav",

                        winsound.SND_ASYNC

                    )


                    cv2.rectangle(

                        img,

                        (0,0),

                        (600,60),

                        (0,255,0),

                        -1

                    )


                    cv2.putText(

                        img,

                        f"{best_name} : {event}",

                        (20,40),

                        cv2.FONT_HERSHEY_SIMPLEX,

                        1,

                        (255,255,255),

                        2

                    )

        except:

            pass


    return av.VideoFrame.from_ndarray(

        img,

        format="bgr24"

    )