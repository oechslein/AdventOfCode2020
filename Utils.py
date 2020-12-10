def multiply(my_list):
    if not(my_list):
        return 1
    return my_list[0] * multiply(my_list[1:])