import sys
import os

from BWBS import *

path = 'D:/FIME_8VO/TeoriaInfo/CalgaryCorpus/'

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