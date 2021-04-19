#from itertools import combinations, permutations
import sys

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
    #const Sigma = new Set<string>()
    #for (let i = 0; i < str.length; ++i)
        #Sigma.add(str[i]);
    #return Array.from(Sigma).sort()
    alphabet = []
    
    for i in range(len(text)):
        alphabet.append(str(text[i]))
    print(alphabet)
    unique_alphabet = list(set(alphabet))
    unique_alphabet.sort()
    return unique_alphabet
"""
? function move_to_front: Agarra el caracter con su indice y lo mueve al frente de la lista
? param index: el indice en la cadena de texto
"""
def move_to_front():
    print('move to front')
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
print(get_alphabet(bws[0]))
#print(f'Resultado de la segunda transformación: "{resultado}"')