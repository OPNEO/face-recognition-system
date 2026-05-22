import os
from deepface import DeepFace


"""
Description:
    Generate embeddings for all registered
    face images inside dataset folder.

Args:
    None

Returns:
    None
"""


def generate_embeddings():

    dataset_folder = "dataset"

    if not os.path.exists(dataset_folder):

        print("Dataset folder not found")

        return

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
            f"\nProcessing: {person_name}"
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

                print(
                    f"\nImage: {image_name}"
                )

                print(
                    f"Vector length:"
                    f" {len(vector)}"
                )

                print(
                    f"First values:"
                )

                print(
                    vector[:10]
                )

            except Exception as error:

                print(
                    f"\nError: {image_name}"
                )

                print(error)


if __name__ == "__main__":

    generate_embeddings()