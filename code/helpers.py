import random
def random_unique(n, start, stop):
    if (stop - start) < n:
        raise ValueError('Not enough number of subsequent classes')
    return random.sample(range(start, stop), n)

def compare_two_lists(a, b):
    return not set(a).isdisjoint(set(b))