def encode(data):
    encoding = ''
    prev_char = ''
    count = 1

    if not data: return ''

    for char in data:
        # Ultimo caracter y actual son diferentes
        if char != prev_char:
            # Suma la cuenta y el caracter
            if prev_char:
                encoding += str(count) + prev_char
            count = 1
            prev_char = char
        else:
            count += 1
    else:
        encoding += str(count) + prev_char
        return encoding

def decode(data):
    decode = ''
    count = ''
    for char in data:
        # Caracter numérico
        if char.isdigit():
            char = char[0]
            count += char
        else:
            # Obtener caracter * cuenta para el decoding
            try:
                c = int(count)
                if(c <= 9):
                    decode += char * int(count)
                    count = ''
            except:
                decode += char
    return decode
