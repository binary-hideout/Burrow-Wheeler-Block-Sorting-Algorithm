'''

'''
import BWBS
import os, io 
import sys
from os import listdir
from os.path import isfile, join
import threading
from threading import Thread
import binascii

path = os.getcwd()
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


def open_file(test):
    test_compressed = open('compress_' + test, 'w', buffering=2000000)
    with open(path + '\\' + test, 'r', buffering=2000000) as file:

        txt = file.read()
        bw_list = txt.split('Ä')
        bw_list.pop()

        final_text = ''
        for transform in bw_list:

            transform = transform.split(' ')
            data = transform[0]
            index = transform[1]

            # asscii = list(chunkstring(data, 3))

            # for binary in asscii:
            #     c = int(binary,2)
            #     final_text += str(c)

            c = int(data,2)
            h = hex(c).split('x')[-1]
            final_text += str(h)

            final_text += ' ' + index + 'Ä'   

        file.close()

    test_compressed.write(final_text)

    test_compressed.close()

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


get_file()