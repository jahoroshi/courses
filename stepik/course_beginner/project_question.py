import random
answers = [
    "Бесспорно",
    "Мне кажется - да",
    "Пока неясно, попробуй снова",
    "Даже не думай",
    "Предрешено",
    "Вероятнее всего",
    "Спроси позже",
    "Мой ответ - нет",
    "Никаких сомнений",
    "Хорошие перспективы",
    "Лучше не рассказывать",
    "По моим данным - нет",
    "Определённо да",
    "Знаки говорят - да",
    "Сейчас нельзя предсказать",
    "Перспективы не очень хорошие",
    "Можешь быть уверен в этом",
    "Да",
    "Сконцентрируйся и спроси опять",
    "Весьма сомнительно"
]

question = True

print("Привет Мир, я магический шар, и я знаю ответ на любой твой вопрос.\n")
print(f'Привет {input("Давай знакомиться, как тебя зовут? ...")}\n')

while True:
    input("Задай свой вопрос: ")
    print("\n>>>>", random.choice(answers))
    print("\nХотите сыграть еще одну игру?")
    if input("Да/нет: ").lower() == 'нет':
        print("\nВозвращайся если возникнут вопросы!")
        break 
    else:
        print("\n-------Давай попробуем еще разок. \n")