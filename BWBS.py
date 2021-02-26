from itertools import combinations, permutations

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

print(all_string_permutations('hello'))

def block_sorting_forward(char:str):
    """
    ? :param char: La string con la que se hará la matriz y se obtendrá el resultado para después aplicar
    ? 'block-sorting-reverse-transformation
    """
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")

def block_sorting_reverse_transformation(char:str):
    """
    ? :param matrix: El resultado de block-sorting-forward
    """
    if not isinstance(char, str):
        raise TypeError("El parametro debe ser una string")
    if not char:
        raise ValueError("La string no puede estar vacía")