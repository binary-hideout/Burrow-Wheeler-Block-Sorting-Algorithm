#from itertools import combinations, permutations
import sys
import math

"""
? param char: La string de la que se sacaran las permutaciones ciclicas, 
?  a->b, b->c, c->d, d->a, por n veces, n=len(char)
? Referencia: https://solitaryroad.com/c302.html
"""
def all_string_permutations(char:str):
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")
    return [char[i:] + char[:i] for i in range(len(char))]


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

    cyclic_permutations = all_string_permutations(char)
    #print(f'permutaciones de la string "{char}":')
    #print(cyclic_permutations, '\n')
    cyclic_permutations.sort()
    #print(f'permutaciones de la string "{char}" ordenadas alfabeticamente:')
    #print(cyclic_permutations)

    combination = ''
    for perm in cyclic_permutations:
        combination += perm[-1]
    original_word_index = cyclic_permutations.index(char)

    return combination, original_word_index

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
    print(alphabet)
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

    return indexes


def gamma(i):
    repeat = "0" * math.floor(math.log2(i + 1))
    binary = format((i+1),'b')
    return (str(repeat) + str(binary))

def delta(i):
    N = math.floor(math.log2(i+1))
    L = math.floor(math.log2(N+1))
    binary = format((i+1),'b')
    repeat = "0" * L
    return (repeat + str(format((N+1),'b')) + binary[1:])

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
def MTF_Encoding():
    print('Actual mtf encoding')

"""
* Inicio del programa
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
print(move_to_front(bws[0]))
#print(f'Resultado de la segunda transformación: "{resultado}"')