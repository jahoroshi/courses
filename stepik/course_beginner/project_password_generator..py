import random
digits = "0123456789"
lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
punctuation = "!#$%&*+-=?@^"
chars = ""

print("Задайте параметры пароля:\n")
options = (
    [
    input("Введите количество паролей для генерации: "),
    input("Задайте длину пароля: "),
    input("Пароль должен содержать цифры? Да/нет: "),
    input("Пароль должен содержать прописные буквы? Да/нет: "),
    input("Пароль должен содержать строчные буквы? Да/нет: "),
    input("Пароль должен содержать специальные символы? Да/нет: "),
    input("Исключить <il1Lo0O>? Да/нет: ")
     ]
    )

if options[2].lower() != "нет":
    chars += digits
if options[3].lower() != "нет":
    chars += lowercase_letters
if options[4].lower() != "нет":
    chars += uppercase_letters
if options[5].lower() != "нет":
    chars += punctuation
    
for _ in range(int(options[0])):
    print("".join(random.sample(chars, int(options[1]))))