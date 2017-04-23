from random import randint


def coupon_collector(n):
    """
    Coupon collector problem
    :param n:  number of coupons to collect
    :return: number of iterations
    """
    collected = [False] * n
    ite = 0  # iterations
    unique = 0
    while unique < n:
        r = randint(0, n - 1)
        if not collected[r]:
            unique += 1
            collected[r] = True

        ite += 1
    return ite
