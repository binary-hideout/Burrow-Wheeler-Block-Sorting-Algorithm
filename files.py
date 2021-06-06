'''

'''
import BWBS
from run_encoding import *
import sys
from os import listdir
from os.path import isfile, join
import timeit

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

        rle = False
        print('Aplicar RLE puede mejorar el nivel de compresión y acelerar el proceso')
        opc = input('Usar RLE? (s/n): ')

        if opc == 's':
            rle = True
        elif opc == 'n':
            rle = False
        else:
            print('Ingrese una opcion valida')
        
        rle_time = 'N/A'
        if(rle):
            rle_start = timeit.default_timer()
            run_l_encoded = encode(txt)
            rle_time = timeit.default_timer() - rle_start
            txt = run_l_encoded
        else:
            rle_time = 'N/A'
            pass

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
            #?BWBS
            bwbs_start = timeit.default_timer()
            x = BWBS.bwbs(txt)
            modified_line = convertTuple(x[0])
            index = x[1]
            bwbs_time = timeit.default_timer() - bwbs_start
            #?MTF
            mtf_start = timeit.default_timer()
            mtf = BWBS.MTF_Encoding(modified_line)
            binary = mtf[0]
            alphabet = mtf[1]
            alphabet_list.append(alphabet)
            mtf_time = timeit.default_timer() - mtf_start

            test_modified.write(binary + ' ' + str(index) + 'Ä')

    test_modified.close()

    opc = input('Decodificar el archivo? (s/n): ')

    if opc == 's':
        decoding_start = timeit.default_timer()
        decode_file(test, alphabet_list, rle)
        decoding_time = timeit.default_timer() - decoding_start 
        print('\nTiempos:\n-------------------------------\n')
        print(f'RL encoding: {rle_time}s\nBWT: {bwbs_time/60}min\nMTF encoding: {mtf_time}s\n')
        print(f'Decoding: {decoding_time/60}min\n')
        print('----------------------------')
    elif opc == 'n':
        print('Tiempos:\n')
        print(f'RL encoding: {rle_time}s\nBWT: {bwbs_time/60}min\nMTF encoding: {mtf_time}s\n')
        print('----------------------------')
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