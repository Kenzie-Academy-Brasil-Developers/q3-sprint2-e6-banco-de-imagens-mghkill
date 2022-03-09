from flask import Flask, request, jsonify, safe_join, send_file
from app.kenzie import DATABASE_DIRECTORY, ENV_GENERATOR, FILES_DIRECTORY, FILE_MAX_LENGTH, create_directore_database
from http import HTTPStatus
import os
import time

from app.kenzie.image import generator_walk

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
        return {"error": "unsupported extension", "type file": "jpg, gif, png"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

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

    generator_walk = os.walk(ENV_GENERATOR)
    output_list_dir = []
    output_list_file = []
    
    for directory, _, file in list(generator_walk):
        dir_append = directory.split("/")[-1]
        output_list_dir.append(dir_append)
        output_list_file.append(file)
        
    output = dict(zip(output_list_dir[1:], output_list_file[1:]))
    

    
    return output, HTTPStatus.OK

@app.get('/files/<dirname>')
def search_item(dirname):
    output_list_dir = []
    output_list_file = []   
    generator_walk = os.walk(ENV_GENERATOR)
    
    for directory, _, file in list(generator_walk):
        dir_append = directory.split("/")[-1]
        output_list_dir.append(dir_append)
        output_list_file.append(file)

    
    
    output = dict(zip(output_list_dir[1:], output_list_file[1:]))
    
    if dirname in output.keys():
        return {dirname: output[dirname]}, HTTPStatus.OK
    
    return {"error": "extension not found"}, HTTPStatus.NOT_FOUND


@app.get('/download/<filename>')
def download_item(filename):
    extension = filename.split(".")[-1]

    path_files_upload = os.path.abspath(f"./{DATABASE_DIRECTORY}/{FILES_DIRECTORY}/{extension}")

    filepath = safe_join(path_files_upload, filename)
    # 
    output_list_dir = []
    output_list_file = [] 

    # generator_walk(output_list_dir, output_list_file)
    generator = os.walk(ENV_GENERATOR)

    for directory, _, file in list(generator):
        dir_append = directory.split("/")[-1]
        output_list_dir.append(dir_append)
        output_list_file.append(file)

    for item in output_list_file:
        if filename in item:
            return send_file(filepath, as_attachment=True), HTTPStatus.OK
    
    return {"error": "not found"}, HTTPStatus.NOT_FOUND
    