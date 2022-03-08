from flask import Flask, request, jsonify, safe_join
from app.kenzie import ALLOWED_EXTENSIONS, DATABASE_DIRECTORY, FILES_DIRECTORY, create_directore_database
from http import HTTPStatus
import os
import time

app = Flask(__name__)

create_directore_database()


@app.post('/upload')
def upload_image():

    file = request.files["file"]
    extension = file.filename.split(".")[-1]
    path_files_upload = os.path.abspath(f"./{DATABASE_DIRECTORY}/{FILES_DIRECTORY}/{extension}")
    
    file_walk = os.walk(path_files_upload)
    try:
        for *_, file_name in file_walk:
            if file_name[0] == file.filename:
                return {"error": "this image already exists"}, 409
    except IndexError:

        if not os.path.isdir(path_files_upload):

            return {"error": "unsupported media type", "type file": "jpg, gif, png"},HTTPStatus.UNSUPPORTED_MEDIA_TYPE  

        file.save(f"{path_files_upload}/{file.filename}") 
        return {"message": "image created"}, HTTPStatus.CREATED


@app.get('/')
def teste():
    return ""
