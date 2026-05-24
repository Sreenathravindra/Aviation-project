def fl_list(a):
    flated =[]
    for items in a:
        if type(items) is list:
            flated.extend(fl_list(items))
        else:
            flated.append(items)
    return flated

if __name__ == '__main__':
    a = [[0],[1, 2], [3, 4, 5], [6], 7, [8, 9], [10,[11,[12]]]]

    print(fl_list(a))