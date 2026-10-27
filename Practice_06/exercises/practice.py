
with open("demofile2.txt", "w") as f:
    f.write("Hi")

# Open the file again to read it
with open("demofile2.txt", "r") as f:
    print(f.read())