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
    cyclic_permutations.sort()

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
        txt_alphabet.pop(id_alphabet)
        txt_alphabet.insert(0, text[i])

    return indexes, get_alphabet(text) #indexes + original alphabet

def delta(i):
    N = math.floor(math.log2(i+1))
    L = math.floor(math.log2(N+1))
    binary = format((i+1),'b')
    repeat = "0" * L
    return (repeat + str(format((N+1),'b')) + binary[1:])


"""
? param bits: Cadena de bits con los codigos "Elias delta"
"""
def inv_delta(bits:str):
    output = []
    try:
        L = bits.index("1")
    except Exception as e:
        L=-1

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


    if len(bits) > 0:
        return []

    return output
    
    
"""
? function MTF_Encoding: calls delta function to convert the indexes from move to front to bits
? param char: the string to be encoded
? return accumulator: the string converted to bits
"""
def MTF_Encoding(char:str):
    mtf = move_to_front(char)
    indexes = mtf[0]
    alphabet = mtf[1]
    accumulator = ''
    for i in range(len(indexes)):
        accumulator += delta(indexes[i])

    return accumulator, alphabet

"""
? function MTF_Decoding: Decodifica la cadena del Mtf
? param mtf_coded: la cadena a decodificar
? param alphabet: alfabeto original
? return decoded text: caracteres del alfabeto ordenados
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

    bws = block_sorting_forward(original_word) #Block sorting forward con la string
    
    return bws