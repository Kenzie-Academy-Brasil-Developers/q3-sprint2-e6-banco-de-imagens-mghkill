# Desenvolva sua lógica de manipulação das imagens aqui


import os

from app.kenzie import ENV_GENERATOR


def generator_walk(direc, file):
    
    generator = os.walk(ENV_GENERATOR)

    for directory, _, file in list(generator):
        dir_append = directory.split("/")[-1]
        direc.append(dir_append)
        file.append(file)