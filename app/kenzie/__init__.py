import os
FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")
DATABASE_DIRECTORY = os.getenv("DATABASE_DIRECTORY")
FILE_MAX_LENGTH = os.getenv("FILE_MAX_LENGTH")
ENV_GENERATOR = os.getenv("ENV_GENERATOR")

def create_directore_database():
    path_files_upload = os.path.abspath(f"{DATABASE_DIRECTORY}")
    if not os.path.isdir(path_files_upload):
        os.mkdir(f"./{DATABASE_DIRECTORY}")
        os.mkdir(f"./{DATABASE_DIRECTORY}/{FILES_DIRECTORY}")
    
        for item in ALLOWED_EXTENSIONS.split(","):
            os.mkdir(f"./{DATABASE_DIRECTORY}/{FILES_DIRECTORY}/{item}")
        