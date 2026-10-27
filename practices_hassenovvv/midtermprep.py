#1

# mylist = list(map(int, input().split()))
# for i, num in enumerate(mylist, start = 0):
#     if num > 10:
#         print(i, num)

#2

# names = list(map(str, input().split()))
# grades = list(map(int, input().split()))

# for name, grade in zip(names,grades):
#     print(name, grade)

"""

ЗАДАНИЕ 4 — REDUCE

Напиши генератор, который выдаёт согласные буквы английского слова. Используй yield.

Пример:
Ввод:
Programming

Вывод:
P r g r m m n g

    
"""
def consonant(word):
    vowels = 'aeiouAEIOU'
    for letter in word:
        if letter not in vowels:
            yield letter

word = input()
print(list(consonant(word)))