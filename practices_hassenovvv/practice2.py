# def generator_vowel(list):
#     vowels = 'aeiou'
#     for i in list:
#         if list[0] in vowels:
#             yield i
   
# list = input("Enter a word:")
# x = generator_vowel(list)
# print(next(x))

import datetime 
x = datetime.datetime.now()
y = datetime.datetime(2020,5,17)
difference = x - y
print(difference.days)