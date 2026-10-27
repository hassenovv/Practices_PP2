#classes, data math 

with open("shopping.txt", "w") as f:
    f.write("Banana \n")
    f.write("Apple \n")
    f.write("Kiwi \n")
    f.write("Mango \n")
    f.write("Orange \n")


with open("shopping.txt", "a") as f:
    f.write("Cherry \n") 
    f.write("Grapes \n")
            

with open("shopping.txt", "x") as f:
    content = f.read()
    print(content)

x = sorted(content.splitlines(), reverse = False)
print(x)
