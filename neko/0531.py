def testK(k: int):
    for m in range(1,10000):
        if '1' in f'{k*m}':
            # print(i, m*i, )
            pass
        else:
            return False
    return True
for k in range(1,100000000000000000000000000):
    if testK(k):
        print(k)
    