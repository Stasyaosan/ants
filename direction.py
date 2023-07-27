right = [1, 0]
right_up = [1, -1]
right_down = [1, 1]
left = [-1, 0]
left_up = [-1, -1]
left_down = [-1, 1]
up = [0, -1]
down = [0, 1]


def filter_by_right(element):
    # print(element)
    if element[0] == 1:
        return False
    return True


def filter_by_left(element):
    # print(element)
    if element[0] == -1:
        return False
    return True


def filter_by_up(element):
    # print(element)
    if element[1] == -1:
        return False
    return True


def filter_by_down(element):
    # print(element)
    if element[1] == 1:
        return False
    return True


