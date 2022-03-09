from flask import Flask, request, jsonify, safe_join, send_file
from app.kenzie import DATABASE_DIRECTORY, ENV_GENERATOR, FILES_DIRECTORY, FILE_MAX_LENGTH, create_directore_database
from http import HTTPStatus
import os

from app.kenzie.image import walk_generator

app = Flask(__name__)

create_directore_database()


@app.post('/upload')
def upload_image():

    file = request.files["file"]
    extension = file.filename.split(".")[-1]
    path_files_upload = os.path.abspath(f"./{DATABASE_DIRECTORY}/{FILES_DIRECTORY}/{extension}")
    file_walk = os.walk(path_files_upload)
    dict_header = int(dict(request.headers)["Content-Length"])


    if not os.path.isdir(path_files_upload):
        return {"error": "unsupported media type"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    if dict_header > int(FILE_MAX_LENGTH):
        return {"error": "max 1.0MB"}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE

    try:
        for *_, file_name in file_walk:
            if file_name[0] == file.filename:
                return {"error": "this image already exists"}, HTTPStatus.CONFLICT
    except IndexError:  
        ...    
    file.save(f"{path_files_upload}/{file.filename}") 

    return {"message": "image created"}, HTTPStatus.CREATED



@app.get('/files')
def list_items():

    tuple_directory = walk_generator()   
        
    output = dict(zip(tuple_directory[0][1:], tuple_directory[1][1:]))
    
    return output, HTTPStatus.OK



@app.get('/files/<dirname>')
def search_item(dirname):

    tuple_directory = walk_generator()
    
    output = dict(zip(tuple_directory[0][1:], tuple_directory[1][1:]))
    
    if dirname in output.keys():
        return {dirname: output[dirname]}, HTTPStatus.OK
    
    return {"error": "extension not found"}, HTTPStatus.NOT_FOUND



@app.get('/download/<filename>')
def download_item(filename):
    

    extension = filename.split(".")[-1]

    path_files_upload = os.path.abspath(f"./{DATABASE_DIRECTORY}/{FILES_DIRECTORY}/{extension}")

    filepath = safe_join(path_files_upload, filename)

    tuple_directory = walk_generator()

    for item in tuple_directory[1]:
        if filename in item:
            return send_file(filepath, as_attachment=True), HTTPStatus.OK
    
    return {"error": "not found"}, HTTPStatus.NOT_FOUND
    