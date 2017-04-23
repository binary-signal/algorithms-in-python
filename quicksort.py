from math import floor


def quicksort(s):
    """
    Quick sort algorithm implementation using recursion 
    :param s: unordered list of elements
    :return: ordered list of elements
    """
    if len(s) == 0 or len(s) == 1:  # trivial case
        return s
    n = len(s)
    m = floor(n / 2)
    x = s[m]  # pivot

    s1 = []  # elements smaller or equal to pivot element
    s2 = []  # elements greater than pivot

    for i in range(0, n):
        if i == m:  # skip comparison with self
            continue
        if s[i] <= x:
            s1.append(s[i])
        else:
            s2.append(s[i])

    s1 = quicksort(s1)  # quick-sort left sub list
    s2 = quicksort(s2)  # quick-sort right sub list

    s1.append(x)    # merge ordered elements
    s1 = s1 + s2
    return s1
