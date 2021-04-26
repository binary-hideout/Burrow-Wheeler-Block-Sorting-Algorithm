import sys
import os

from BWBS import *

# get PATH
cwd = os.getcwd()
path = cwd + '/CalgaryCorpus/'

all_files = os.listdir(path)
#print(all_files)
txt_files = list(filter(lambda x: x[-4:] == '.txt', all_files))
print(txt_files)

def file_to_strings(file):
    strings = []
    with open(path + file, 'rt') as fd:
        for line in fd:
            line = line.rstrip()
            strings.append(line)
    return strings
"""
for f in txt_files:
    print(file_to_strings(f))
"""
def encode(option:int):
    strings = file_to_strings(txt_files[option - 1])
    with open(path + 'encoded.txt', 'w') as enc:
        for s in strings:
            
            if s == '':
                print('espacio')
            
            else:
                bwt = block_sorting_forward(s)
                index = bwt[1]
                print(bwt)
        
            #mtf = MTF_Encoding(bwt[0])
            #binary = mtf[0]
            #alphabet = mtf[1]

            #enc.write(binary + ' ' + index + ' ' + alphabet + '\n')
            




print('Ingresa el número de archivo que quieres codificar')
for i in range(len(txt_files)):
    print(f'{i + 1}.- {txt_files[i]}')

try:
    option = int(input('Selección: '))
    encode(option)
except:
    print('Opción no aceptada')
    sys.exit()
