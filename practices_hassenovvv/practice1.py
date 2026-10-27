# создать файл и написать в нем лист продуктов потом добавить в конец списка еще новые и прочитать
with open("products.txt", "w") as f:
    f.write("Melon \n" "Apple \n" "Banana \n")

with open("products.txt", "a") as f:
    f.write("Cherry \n" "Strawberry")

with open("products.txt", "r") as f:
    content = f.read()
    print(content)


x = sorted(content.splitlines(), reverse = True)
print(x)

# import datetime

# x = datetime.date.now()
# print(x)