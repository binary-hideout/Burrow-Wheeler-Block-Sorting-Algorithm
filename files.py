'''

'''
import BWBS
import os, io 
import sys
from os import listdir
from os.path import isfile, join
import threading
from threading import Thread

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
        # print(txt)

        txt_list = list()

        # ? Entre más bajo sea este valor, más rápido será el prorgama
        letras_por_transformada = 24688 # Aproximadamente 1 GB de memoria

        if (len(txt) < (letras_por_transformada * 2)):
            txt_list.append(txt)

        else:
            aux = 0
            partes = int(len(txt) / letras_por_transformada)

            for i in range(1,partes+1):
                siguiente = int((len(txt) / partes) * i)

                txt_list.append(txt[aux:siguiente])
                aux = siguiente

        alphabet_list = list()
        for txt in txt_list:
            x = BWBS.bwbs(txt)
            modified_line = convertTuple(x[0])
            index = x[1]
        
            #mtf = BWBS.MTF_Encoding(txt)
            mtf = BWBS.MTF_Encoding(modified_line)
            binary = mtf[0]
            alphabet = mtf[1]
            alphabet_list.append(alphabet)
            #test_modified.write(binary)
            # test_modified.write(binary + ' ' + str(index) + '\n')
            test_modified.write(binary + ' ' + str(index) + 'Ä')

            """
            test_modified.write(binary + ' ' + str(index) + '\n')
            #enc.write(binary + ' ' + index + ' ' + alphabet + '\n')
            """
    test_modified.close()

    opc = input('Decodificar el archivo? (s/n): ')

    if opc == 's':
        decode_file(test, alphabet_list)
    elif opc == 'n':
        sys.exit()
    else:
        print('Ingrese una opcion valida')

def decode_file(test, alphabet):
    test_decoded = open('decode_' + test, 'w', buffering=2000000)
    
    with open('bw_' + test, 'r', buffering=2000000) as file:
        txt = file.read()
        bw_list = txt.split('Ä')
        bw_list.pop()

        final_text = ''
        a = 0
        for encode in bw_list:
            encode = encode.split(' ')
            transform = encode[0]
            index = encode[1]
            x = BWBS.MTF_Decoding(transform, alphabet[a])

            final_text += x

            # final_text += BWBS.block_sorting_reverse_transformation(x, int(index))

            a+=1
            
        
        file.close()


    test_decoded.write(final_text)

    test_decoded.close()

get_file()