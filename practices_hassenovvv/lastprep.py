# with open("names.txt", "w") as f:
#     f.write("Arman \n")
#     f.write("Nurik \n")
#     f.write("Iliyas \n")
#     f.write("Aidos \n")

# with open("names.txt", "r") as f:
#     content = f.read()
   


# x = list(filter(lambda name: name[0]== "A", content.splitlines()))
# print(x)

# with open("numbers.txt", "w") as f:
#     f.write("5 \n")
#     f.write("10 \n")
#     f.write("15 \n")
#     f.write("20 \n")

# with open("numbers.txt", "r") as f:
#     content = f.read()
   
# x = sum(map(int, content.splitlines()))
# print(x)

def vowel(word):
    vowels = 'aeiou'
    for i in word:
        if i == vowels:
            yield i

word = input()
print(list(vowel(word)))

