#from itertools import combinations, permutations

def all_string_permutations(char:str):
    """
    ? :param char: La string de la que se sacaran las permutaciones ciclicas, 
    ?  a->b, b->c, c->d, d->a, por n veces, n=len(char)
    ? https://solitaryroad.com/c302.html
    """
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")
    return [char[i:] + char[:i] for i in range(len(char))]


def block_sorting_forward(char:str):
    """
    ? :param char: La string con la que se hará la matriz y se obtendrá el resultado para después aplicar
    ? 'block-sorting-reverse-transformation
    ? :return: tupla con la combinación del último caracter de cada fila y el indice de la string original
    """
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")

    cyclic_permutations = all_string_permutations(char)
    print(f'permutaciones de la string "{char}":')
    print(cyclic_permutations, '\n')
    cyclic_permutations.sort()
    print(f'permutaciones de la string "{char}" ordenadas alfabeticamente:')
    print(cyclic_permutations)

    combination = ''
    for perm in cyclic_permutations:
        combination += perm[-1]
    original_word_index = cyclic_permutations.index(char)

    return combination, original_word_index


def block_sorting_reverse_transformation(char:str, index:int):
    """
    ? :param char: La string resultante de bs-forward
    ? :param index: El indíce de la string original
    """
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")


print(block_sorting_forward('hello!'))