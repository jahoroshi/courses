import random
global word_list
word_list = ['птица', 'быть', 'человек', 'год', 'время', 'работа', 'день', 'рука', 'жизнь', 'говорить']

def get_word():
    return random.choice(word_list)

def display_hangman(tries):
    stages = [  # финальное состояние: голова, торс, обе руки, обе ноги
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                ''',
                # голова, торс, обе руки, одна нога
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                ''',
                # голова, торс, обе руки
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                ''',
                # голова, торс и одна рука
                '''
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                ''',
                # голова и торс
                '''
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                ''',
                # голова
                '''
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                ''',
                # начальное состояние
                '''
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                '''
    ]
    return stages[tries]

def play(word):
    word_completion = ["_" for _ in range(len(word))]  # строка, содержащая символы _ на каждую букву задуманного слова
    guessed = False                    # сигнальная метка
    guessed_letters = []               # список уже названных букв
    guessed_words = []                 # список уже названных слов
    tries = 6                          # количество попыток
    final_word = []
    
    print("Давайте играть в угадайку слов!\n")

    
    while tries >= 0 and not word.isupper():
        print(display_hangman(tries))
        print("+++>", "".join(word_completion), "\n")
        entering = input("Введите слово или букву: ").lower()
        
        if not entering.isalpha():
            print("Вы ввели некорректный символ.")
            continue
        elif entering in guessed_letters:
            print("Вы уже называли такую букву, назовите новую.")
            continue
        elif entering in guessed_words:
            print("Вы уже называли такое слово, пробуйте ещё!")
            continue
        elif len(entering) > 1:
            if entering == word:
                print(f"Поздравляем! Вы угадали слово {word}!")
                break
            else:
                guessed_words.append(entering)
                print("Вы назвали неверное слово.")
                tries -= 1
                continue
        else:
            guessed_letters.append(entering)
            if entering in word:
                for i in word:
                    if entering == i:
                        word_completion[word.index(i)] = i
                        word = word.replace(i, i.upper(), 1)
                        print("\nПопадание.")
                else:
                    continue
                    
            else:
                print(f"Буквы {entering} нет в слове.")
                guessed_letters.append(entering)
                tries -= 1  
                
        if not tries:
            print(display_hangman(tries))
            print("\n\n:::::Вы проиграли! =((:::::\n\n")
            break
        if tries in [3, 1]:
            tries_count = 2
            if tries_count:
                print()
                clue = input("Хотите подсказку? Да/нет: ")
                print()
                if not clue.lower() == "нет":
                    show_let = input("Сколько букв показать?___: ")
                    if show_let.isdigit():
                        for _ in range(int(show_let)):
                            for i in word:
                                if i.islower():
                                    word_completion[word.index(i)] = i
                                    word = word.replace(i, i.upper(), 1)
                                    tries_count -= 1
                                    break
                                    
                    else:
                        print("Введена не цифра!")
                        continue
        
    else:
        print("\n\n---CONGRATULATIONS!---\n")
        print(f"Поздравляем! Вы угадали слово {word}!\n")

                    
                
while not play(get_word()):
    answer = input("Хотите сыграть еще? Да/нет: ")
    if answer.lower() == "нет":
        break
    else:
        continue

        


                
            