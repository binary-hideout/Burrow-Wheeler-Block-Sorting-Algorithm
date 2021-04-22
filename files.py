'''

'''
import BWBS
import sys
from os import listdir
from os.path import isfile, join

path = 'calgarycorpus/'
calgary_files = [f for f in listdir(path) if isfile(join(path, f))] # Se obtienen todos los documentos dentro de la carpeta 'calgarycorpus'


def get_file():
    x = 0
    try:
        print('--- DOCUMENTO DE PRUEBAS ---')
        for i, item in enumerate(calgary_files, 1):
            if item != '.DS_Store': print(i, '. ' + item, sep = '', end = '\n')

        x = int(input('\nSeleccionar el documento con el que se vaya a trabajar: ')) # El usuario escoge en formato numérico el archivo con el que se trabajará
    except:
        print('Ingrese una opción válida')
        sys.exit()
    
    open_file(calgary_files[x])

def convertTuple(tup):
    str =  ''.join(tup)
    return str


def open_file(test):
    test_modified = open('bw_' + test, 'w')
    with open(path + test) as infile:
        for line in infile:
            x = BWBS.bwbs(line)
            modified_line = convertTuple(x[0])
            test_modified.write(modified_line)
    test_modified.close()

get_file()