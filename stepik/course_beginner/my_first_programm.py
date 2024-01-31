import random

user_num = 0
count = 0
num = 0

def header():
    global user_num
    global count
    print('Вы можете сами указать максимальное загаданное число или просто нажмите Enter')
    user_num = input()
    count = 0
    
def random_value():
    global user_num
    global num
    if user_num and user_num != '0':
        num = random.randint(1, int(user_num))
    else:
        num = random.randint(1, 100)
        user_num = '100'
    print(num, '!!')


def is_valid(n):
    global user_num
    if n.isdigit():
        n = int(n)
        if user_num:
            return 1 <= n <= int(user_num)
        else:
            return 1 <= n <= 100
    else:
        return False

def artificial_guess():
    val = [int(i) for i in range(1, int(user_num) + 1)]
    up_limit = len(val) // 2
    low_limit = 0
    count = 0
    
    while not num == up_limit:
        if num in val[low_limit:up_limit]:
            up_limit = (up_limit - low_limit) // 2 + low_limit
            # print('1. ', "low:", low_limit, 'up:', up_limit)

        elif num in val[up_limit:]:
            low_limit = up_limit
            up_limit = (up_limit - up_limit // 2) + up_limit
            # print('2.       ', "low:", low_limit, 'up:', up_limit)
        count += 1
        
    return count

    
    
print('Добро пожаловать в числовую угадайку')
header()
random_value()

    
while True:
    n = input()
    if is_valid(n):
        count += 1
        n = int(n)
        if n < num:
            print('Ваше число меньше загаданного, попробуйте еще разок')
        if n > num:
            print('Ваше число больше загаданного, попробуйте еще разок')
        if n == num:
            print(f'Вы угадали, поздравляем! Количество попыток: {count}')
            print(f'Количество итераций у искусственного угадайки: {artificial_guess()}')
            print('Хотите поиграть еще раз?')
            repeat = input('Да/нет: ')
            
            if repeat.lower() == 'да' or not repeat:
                header()
                random_value()
                count = 0
                print('!', num)
                continue
            elif repeat.lower() == "нет":
                print('Спасибо, что играли в числовую угадайку. Еще увидимся...')
                break
            else:
                while True:
                    repeat = input('Введите Да или Нет: ')
                    if repeat.lower() in ("да", "нет"):
                        header()
                        random_value()
                        break
    else:
        print(f'А может быть все-таки введем целое число от 1 до {user_num if user_num else 100}?')