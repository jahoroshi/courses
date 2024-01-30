def encrypt(n, text):
    encrypted_text = ""

    for i in text:
        
        let_first = let_1 if i.islower() else let_3
        let_last = let_2 if i.islower() else let_4
        
        if i.isalpha():
            if ord(i) + n > ord(let_last):
                encrypted_text += chr(ord(let_first) + ((ord(i) + n) - ord(let_last)) - 1)
            else:
                encrypted_text += chr(ord(i) + n)
            
        else:
            encrypted_text += i
            
    return encrypted_text

text = list('To be, or not to be, that is the question')
word = ""
res = ""
language = 0
let_1 = ["a", "а"][language]
let_2 = ["z", "я"][language]
let_3 = ["A", "А"][language]
let_4 = ["Z", "Я"][language]
        
for i in text:
    if i.isalpha():
        word += i
    elif not i.isalpha():
        res += encrypt(len(word), word) + i
        word = ""
else:
    res += encrypt(len(word), word)
    
print(res)






