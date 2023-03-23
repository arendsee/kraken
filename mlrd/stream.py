def takeS(i, xs):
    ys = [x for (j, x) in xs if j < i]
    return ys

#  unpackStream py :: unpack => "iterator" a -> [a]
def unpackStream(xs):
    return list(xs)

#  packStream   py :: pack   => [a] -> "iterator" a
def packStream(xs):
    """
    Only needed for compatibility
    """
    for x in xs:
        yield x
