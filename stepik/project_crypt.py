text = "To be, or not to be, that is the question!"
n = 17
encrypted_text = ""
let_1 = "a"
let_2 = "z"
let_3 = "A"
let_4 = "Z"

for i in text:
    if i.isalpha():
        if ord(i) + n > ord(let_2 if i.islower() else let_4):
            encrypted_text += chr(ord(let_1 if i.islower() else let_3) + ((ord(i) + n) - ord(let_2 if i.islower() else let_4)))
        else:
            encrypted_text += chr(ord(let_1 if i.islower() else let_3) + n)
        
    else:
        encrypted_text += i
        
print("".join(encrypted_text))







