glossary = {
    'punishment': ['malum', 'multa'],
    'apple': ['malum', 'pomum', 'popula'],
    'fruit': ['baca', 'bacca', 'popum'],
}

reversed_dict = {}

for key, values in glossary.items():
    for value in values:
        if value in reversed_dict:
            reversed_dict[value].append(key)
        else:
            reversed_dict[value] = [key]

for key, value in sorted(reversed_dict.items()):
    print(key + ' - ' + ', '.join(value))

'''
1) Идём по ключам словаря
2) Идёи по каждому значению ключа словаря
3) Если такое значение есть в новом словаре, то дополняем его ключом 
4) Если нет, то задаём новую пару значение-ключ
5) Проходимся по ключам и значениеям словаря и выводим ключ + джоин значений
'''
# Result:
# baca - fruit
# bacca - fruit
# malum - apple, punishment
# multa - punishment
# pomum - apple
# popula - apple
# popum - fruit

# sorted()
# Методы списков: append(), extend().
# Методы словарей: values(), keys(), items(), get(), update(), setdefault().
