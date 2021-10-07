def magic_func(num):
    rem = num % 2
    if rem == 0:
        return 1 + 4
    else:
        return 0.1


for sel_a in range(10):
    a = magic_func(sel_a)
    if a >= 1:
        print('res: ', sel_a)
    else:
        print('res: ', sel_a * 10.5)