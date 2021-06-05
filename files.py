'''

'''
import BWBS
from run_encoding import *
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
    with open(path + test, buffering=2000000) as infile:
        txt = infile.read()


        txt_list = list()

        # ? Entre más bajo sea este valor, más rápido será el prorgama
        letras_por_transformada = 100 # Aproximadamente 1 GB de memoria

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
        rle = False
        print('Aplicar RLE puede mejorar el nivel de compresión y acelerar el proceso')
        opc = input('Usar RLE? (s/n): ')

        if opc == 's':
            rle = True
        elif opc == 'n':
            rle = False
        else:
            print('Ingrese una opcion valida')

        for txt in txt_list:
            if(rle):
                run_l_encoded = encode(txt)
                x = BWBS.bwbs(run_l_encoded)
                modified_line = convertTuple(x[0])
                index = x[1]
            else:
                x = BWBS.bwbs(txt)
                modified_line = convertTuple(x[0])
                index = x[1]

        
            mtf = BWBS.MTF_Encoding(modified_line)
            binary = mtf[0]
            alphabet = mtf[1]
            alphabet_list.append(alphabet)

            test_modified.write(binary + ' ' + str(index) + 'Ä')

    test_modified.close()

    opc = input('Decodificar el archivo? (s/n): ')

    if opc == 's':
        decode_file(test, alphabet_list, rle)
    elif opc == 'n':
        sys.exit()
    else:
        print('Ingrese una opcion valida')

def decode_file(test, alphabet, rle):
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

            if(rle):
                final_text += decode(BWBS.block_sorting_reverse_transformation(x, int(index)))
            else:
                final_text += BWBS.block_sorting_reverse_transformation(x, int(index))
                

            # ? Final_text: MTF
            # final_text += x

            a+=1
            
        
        file.close()


    test_decoded.write(final_text)

    test_decoded.close()

get_file()