# Функция для обрезки строк и добавления многоточия.
def cut_str(str):
    if len(str) > 48:
        return str[:48] + '...\n'
    return str + '\n'

a = '11111111111111111111'
b = '1111111111111111111111111111111111111111111111111'

c = truncate_str(a)
d = truncate_str(b)

print(c,d)

