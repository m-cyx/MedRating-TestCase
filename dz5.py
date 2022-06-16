# Есть список со списками, сделать его плоским list = [1,[1,2,3,[4,[]], 8, [9,[10,11]]]]

from unittest import result


def make_list(lst, result=[]):
    for item in lst:
        if isinstance(item, list):
            make_list(item, result)
        else:
            result.append(item)
    return result


lst = [1, 2, 3, [4, 5, [], [11, [12, 13, [14]]], 6, [7, 8, 9]]]

print(make_list(lst))
