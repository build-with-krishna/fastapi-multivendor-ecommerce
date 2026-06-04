import os
import uuid

from fastapi import UploadFile


UPLOAD_FOLDER = "app/uploads/products"


def upload_product_image(file: UploadFile):

    # CREATE FOLDER
    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    # UNIQUE FILE NAME
    extension = file.filename.split(".")[-1]

    file_name = f"{uuid.uuid4()}.{extension}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file_name
    )

    # SAVE FILE
    with open(file_path, "wb") as buffer:

        buffer.write(file.file.read())

    return file_name