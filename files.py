
'''

'''
import BWBS
import os, io 
import sys
from os import listdir
from os.path import isfile, join
from burrowswheeler import transform, inverse

path = 'calgarycorpus/'
calgary_files = [f for f in listdir(path) if isfile(join(path, f))] # Se obtienen todos los documentos dentro de la carpeta 'calgarycorpus'


def get_file():
    x = 0
    try:
        print('--- DOCUMENTO DE PRUEBAS ---')
        for i, item in enumerate(calgary_files, 1):
            if item != '.DS_Store': print(i-1, '. ' + item, sep = '', end = '\n')

        x = int(input('\nSeleccionar el documento con el que se vaya a trabajar: ')) # El usuario escoge en formato numérico el archivo con el que se trabajará
    except:
        print('Ingrese una opción válida')
        sys.exit()
    
    open_file(calgary_files[x])

def convertTuple(tup):
    str =  ''.join(tup)
    return str


def open_file(test):
    test_modified = open('bw_' + test, 'w', buffering=2000000)
    #string = io.open(path + test, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True)
    with open(path + test, buffering=2000000) as infile:
        txt = infile.read()
        data = ''.join(txt) + '$'
        # print(txt)
        x = BWBS.bwbs(data)
       
        test_modified.write(x)
        """
        test_modified.write(binary + ' ' + str(index) + '\n')
        #enc.write(binary + ' ' + index + ' ' + alphabet + '\n')
        """
    test_modified.close()

get_file()