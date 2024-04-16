def flip(x: str):
    a = list()
    for i in x:
        a.append(i)
    a.reverse()
    b = ""
    for o in range(len(a)-1):
        b += a[o]
    return b
