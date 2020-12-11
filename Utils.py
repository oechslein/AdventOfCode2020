def multiply(my_list):
    result = 1
    for elem in my_list:
        result *= elem
    return result

def count(my_list):
    result = 0
    for _ in my_list:
        result += 1
    return result
