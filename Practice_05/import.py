def generator_vowel():
    vowels = 'aeiou'
    list = []
    for i in list:
        if list[0] in vowels:
            yield list[i]
   
x = generator_vowel("apple")
print(next(x))



