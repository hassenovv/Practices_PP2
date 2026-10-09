# Practice 6 - File handling: create, read, append
from pathlib import Path

folder = Path(__file__).parent
f = folder / "sample.txt"

# 1. Create a file and write data ("w" = write, erases old content)
with open(f, "w") as file:
    file.write("Hello!\nI am learning Python.\n")

# 2. Read the whole file
with open(f, "r") as file:
    print("read():", file.read())

# read one line / all lines as a list
with open(f) as file:
    print("readline():", file.readline().strip())
with open(f) as file:
    print("readlines():", file.readlines())

# 3. Append a new line ("a" = add to the end)
with open(f, "a") as file:
    file.write("This line was appended.\n")

with open(f) as file:
    print("After append:\n" + file.read())

# "x" = create only if it does NOT exist (error if it does)
try:
    with open(f, "x") as file:
        file.write("never happens")
except FileExistsError:
    print("x mode: file already exists, so Python stopped us.")
