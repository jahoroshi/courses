n, m = [int(i) for i in "3 5".split()]
mt = [[0] * m for _ in range(n)]
[print(*i) for i in mt]
print()
nm = 1
i, j = 0, 0
flag = True
flag_end = True


while flag_end:
    mt[i][j] = nm
    nm +=1
    j += 1
    
    if j == m - 1 or mt[i][j] != 0:
        while flag:
            mt[i][j] = nm
            nm += 1
            i += 1
            
            if i == n - 1 or mt[i][j] != 0:
                while flag:
                    mt[i][j] = nm
                    nm += 1
                    j -= 1
                    
                    if j == 0 or mt[i][j] != 0:
                        while flag:
                            mt[i][j] = nm
                            nm += 1
                            i -= 1
                            if mt[i][j] != 0:
                                flag = False
                                
                            if nm == n*m:
                                flag_end = False
    
                
[print(*i) for i in mt]