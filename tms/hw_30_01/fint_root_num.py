text = "a b c d e f r g b".split()
n = 3
el = 0
res = []

for i in range(-len(text), 0, n):
    res.append(text[i:i + n])
res[-1].append(text[-1])
    
print(res)