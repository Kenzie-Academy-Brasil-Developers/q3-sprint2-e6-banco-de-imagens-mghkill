# Desenvolva sua lógica de manipulação das imagens aqui


import os

from app.kenzie import ENV_GENERATOR


def walk_generator():
    list_dir = []
    list_file = []

    generator = os.walk(ENV_GENERATOR)

    for directory, _, file in list(generator):
        dir_append = directory.split("/")[-1]

        list_dir.append(dir_append)
        list_file.append(file)
    output = (list_dir, list_file)

    return output