def t(x, l):
    return pow(x,l,20201227)

if __name__ == "__main__":
    with open("input.txt") as f:
        data_lines = [int(line.rstrip()) for line in f]
    

    pk_c = data_lines[0]
    pk_d = data_lines[1]

    l_c = 0
    while t(7, l_c) != pk_c:
        l_c += 1
    
    l_d = 0
    while t(7, l_d) != pk_d:
        l_d += 1
    
    encryption_1 = t(pk_c, l_d)
    encryption_2 = t(pk_d, l_c)
    print(f'Solution: {encryption_1}')