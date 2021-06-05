import sys
import os
import math
import time
import LimitMemory
import big_file_sort
from random import choice
from timeit import timeit
from functools import partial

def sort_file():
    # Windows
    #os.system('cmd /c "sort /REC 65535 permutations_list.txt /o sorted_permutations.txt"')
    big_file_sort.sort_file('permutations_list.txt', 'sorted_permutations.txt', temp_file_location='/temp/')

def radix_sort(values, key, step=0):
    if len(values) < 2:
        for value in values:
            yield value
        return

    bins = {}
    for value in values:
        bins.setdefault(key(value, step), []).append(value)

    for k in sorted(bins.keys()):
        for r in radix_sort(bins[k], key, step + 1):
            yield r

def bw_key(text, value, step):
    return text[(value + step) % len(text)]

def burroughs_wheeler_custom(text):
    return ''.join(text[i - 1] for i in radix_sort(range(len(text)), partial(bw_key, text)))

def cyclic_perm_func(a:str):
    n = len(a)
    b = [[a[i - j] for i in range(n)] for j in range(n)]
    return b

def nextperm(lst):
  for i in range(len(lst) - 1, 0, -1):
    if lst[i-1] < lst[i]:
      for j in range(len(lst) - 1, i-1, -1):
        if lst[i-1] < lst[j]:
          return lst[:i-1] + lst[j:j+1] + lst[:j:-1] + lst[i-1:i] + lst[j-1:i-1:-1]

"""
? param char: La string de la que se sacaran las permutaciones ciclicas, 
?  a->b, b->c, c->d, d->a, por n veces, n=len(char)
? Referencia: https://solitaryroad.com/c302.html
"""
def all_string_permutations(char:str):
    """
    memory = int(input('Cantidad de memoria a utilizar en GB: '))

    # Default memory
    if (memory <= 0) or (memory > 12):
        memory = 2

    LimitMemory.set_limit_memory(memory)
    """
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")

    char = char.replace('\n','')

    # print(char)

    buff = 2 * 1000000000 # GB
    with open('permutations_list.txt', 'w') as permutation_file:

        for i in range(len(char)):
            p = char[i:] + char[:i]
            permutation_file.write(p+'\n')
            # print(p)

    permutation_file.close()
    perms = []
    with open('permutations_list.txt', 'r') as permutation_file:

        for l in permutation_file:
            perms.append(l)
    """
    sorted_perms = nextperm(perms)
    perm = ''
    index = 0
    original_index = 0

    # print('\n\n\n\n\n\n\n============= SORTED ===============')

    for line in sorted_perms:
        perm += line[-2]
        # perm.append(line[-2])

        line = line.replace('\n','')

        if line == char:
            original_index = index
        
        index += 1
    """

    """
    sort_file() # sorted_permutations.txt

    perm = ''
    index = 0
    original_index = 0

    # print('\n\n\n\n\n\n\n============= SORTED ===============')
    with open('sorted_permutations.txt', 'r') as f:
        for line in f:
            perm += line[-2]
            # perm.append(line[-2])

            line = line.replace('\n','')

            if line == char:
                original_index = index
            
            index += 1
                

    f.close()
    """
    # print(perm)

    return perms

    # with open('permutations_list.txt', 'r', buffering=buff) as permutation_file:
    #     dataString = permutation_file.read()
    #     dataList = dataString.split('Ä')
    #     dataList.pop()

    #     return dataList
    
    # permutation_file.close()
        

    # return [char[i:] + char[:i] for i in range(len(char))]


"""
? param char: La string con la que se hará la matriz y se obtendrá el resultado para después aplicar
? 'block-sorting-reverse-transformation
? return combination: tupla con la combinación del último caracter de cada fila
? return original_word_index: el indice de la string original
"""
def block_sorting_forward(char:str):
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")

    #cyclic_permutations = all_string_permutations(char)
    # cyclic_permutations = cyclic_perm_func(char)
    
    #print(f'permutaciones de la string "{char}":')
    #print(cyclic_permutations, '\n')

    # cyclic_permutations.sort()

    #print(f'permutaciones de la string "{char}" ordenadas alfabeticamente:')
    #print(cyclic_permutations)

    #combination = ''
    # for perm in cyclic_permutations:
    #     combination += perm[-1]
    # original_word_index = cyclic_permutations.index(char)
    custom = partial(burroughs_wheeler_custom, char)
    #combination += custom.args[0][-2]
    #combination, original_word_index = all_string_permutations(char)

    return custom.args[0]

"""
? function block_sorting_reverse_transformation: 'invierte' el resultado de una transformada de BW
? param char: La string resultante de bs-forward
? param index: El indíce de la string original
"""
def block_sorting_reverse_transformation(char:str, index:int):
    
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")
    if index < 0:
        raise ValueError("El índice no debe ser menor a 0")
    if index >= len(char):
        raise ValueError(
            "El índice no puede ser mayor a la longitud de la string original"
        )
    
    ordered_rotations = [""] * len(char)
    for x in range(len(char)):
        for i in range(len(char)):
            ordered_rotations[i] = char[i] + ordered_rotations[i]
        ordered_rotations.sort()
    return ordered_rotations[index]
"""
? param text: Cadena de texto de la que sacara el alfabeto
? return alphabet: lista con el alfabeto de la cadena
"""
def get_alphabet(text:str):
    alphabet = []

    for i in range(len(text)):
        alphabet.append(str(text[i]))
    #print(alphabet)
    unique_alphabet = list(set(alphabet))
    unique_alphabet.sort()
    return unique_alphabet

"""
? function move_to_front: Aplica el move-to-front
? param text: la cadena de texto a aplicarle el mtf
? return indexes: la string con sus indices correspondientes a partir de su alfabeto.
"""
def move_to_front(text:str):
    if not isinstance(text, str):
        raise TypeError("El parametro debe ser una string")
    if not text:
        raise ValueError("La string no puede estar vacía")

    txt_alphabet = get_alphabet(text)
    indexes = []
    for i in range(len(text)):
        id_alphabet = txt_alphabet.index(text[i])
        indexes.append(id_alphabet)
        #pop that element (text[i]) and put it at the front of the alphabet
        txt_alphabet.pop(id_alphabet)
        txt_alphabet.insert(0, text[i])

    return indexes, get_alphabet(text) #indexes + original alphabet

"""
def gamma(i):
    repeat = "0" * math.floor(math.log2(i + 1))
    binary = format((i+1),'b')
    return (str(repeat) + str(binary))
"""

def delta(i):
    N = math.floor(math.log2(i+1))
    L = math.floor(math.log2(N+1))
    binary = format((i+1),'b')
    repeat = "0" * L
    return (repeat + str(format((N+1),'b')) + binary[1:])

"""
# Robbie test
def inv_gamma(bitstream: str):
    output = []
    try:
        j = bitstream.index("1")
    except Exception as e:
        j=-1
        print("No se encontró el indice")
    while ((j >= 0) and (len(bitstream) > (2*j))):
        output.append(int(bitstream[j:(2 * j + 1)] , 2) - 1)
        bitstream = bitstream[(2*j+1):]
        try:
            j = bitstream.index("1")
        except Exception as e:
            j=-1
            print("No se encontró el indice")
    if len(bitstream) > 0:
        return []
    return output
"""

"""
? param bits: A string of bits consisting of concatenated Elias delta codes.
"""
def inv_delta(bits:str):
    output = []
    try:
        L = bits.index("1")
    except Exception as e:
        L=-1
        #print("No se encontró el indice")

    while L >= 0:
        if ( len(bits) < (2*L+1) ):
            return []
        
        N = int(bits[L:(2 * L + 1)] , 2) - 1

        if ( len(bits) < (2 * L + 1 + N) ):
            return []

        binary = "1" + bits[(2 * L + 1):(2 * L + 1 + N)]
        output.append(int(binary , 2) - 1)
        bits = bits[(2 * L + N + 1):]

        try:
            L = bits.index("1")
        except Exception as e:
            L=-1
            #print("No se encontró el indice")


    if len(bits) > 0:
        return []

    return output
    
    
"""
? function MTF_Encoding: calls delta function to convert the indexes from move to front to bits
? param char: the string to be encoded
? return accumulator: the string converted to bits
"""
def MTF_Encoding(char:str):
    #move_to_front(bws[0]).reduce((accumulator, i) => accumulator + delta(i), "");
    mtf = move_to_front(char)
    indexes = mtf[0]
    alphabet = mtf[1]
    accumulator = ''
    for i in range(len(indexes)):
        accumulator += delta(indexes[i])
    #print(indexes)
    return accumulator, alphabet

"""
? function MTF_Decoding: Decodes and Mtf_encoded string
? param mtf_coded: the string to be decoded
? param alphabet: original alphabet
? return decoded text: the mapped characters from the alphabet
"""
def MTF_Decoding(mtf_coded:str, alphabet:list):
    data = inv_delta(mtf_coded)
    if(data == [] or max(data) >= len(alphabet)):
        return ""
    decoded = []
    for i in range(len(data)):
        j = data[i]
        c = alphabet[j]
        decoded.append(c)
        alphabet.pop(j)
        alphabet.insert(0, c)

    decoded_text = ''
    for word in decoded:
        decoded_text += word
        
    return decoded_text

"""
* Inicio del programa
"""

def bwbs(original_word):
    '''
    try:
        original_word = str(input('Ingresa una cadena de texto para aplicarle el Algoritmo BWSB: '))
    except:
        print('Ingresa una cadena de texto válida')
        sys.exit()
    '''

    bws = block_sorting_forward(original_word) #Block sorting forward con la string
    
    #resultado = block_sorting_reverse_transformation(bws[0], bws[1]) #Block sorting reverse con el resultado de bs forward
    mtf_encoded = MTF_Encoding(bws[0])
    binary = mtf_encoded[0]
    alphabet = mtf_encoded[1]
    '''
    print('\n')
    print(f'La cadena de texto original: "{original_word}"\n')
    print(f'Resultado de la primera transformación: "{bws[0]}" con indice de la original "{bws[1]}"')
    print(move_to_front(bws[0]))
    '''
    #print(f'Resultado de la segunda transformación: "{resultado}"')
    
    return bws

# bwbs()

"""
try:
    original_word = str(input('Ingresa una cadena de texto para aplicarle el Algoritmo BWSB: '))
except:
    print('Ingresa una cadena de texto válida')
    sys.exit()
bws = block_sorting_forward(original_word) #Block sorting forward con la string
#resultado = block_sorting_reverse_transformation(bws[0], bws[1]) #Block sorting reverse con el resultado de bs forward
print('\n')
print(f'La cadena de texto original: "{original_word}"\n')
print(f'Resultado de la primera transformación: "{bws[0]}" con indice de la original "{bws[1]}"')
mtf_encoded = MTF_Encoding(bws[0])
binary = mtf_encoded[0]
alphabet = mtf_encoded[1]
mtf_decoded = MTF_Decoding(binary, alphabet)
print(mtf_decoded)
print(block_sorting_reverse_transformation(mtf_decoded, bws[1]))
#print(f'Resultado de la segunda transformación: "{resultado}"')
"""