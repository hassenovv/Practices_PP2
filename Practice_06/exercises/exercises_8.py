# Practice 6 - the 8 directory + file exercises
import os
import shutil
import string
from pathlib import Path

work = Path(__file__).parent / "ex_work"
work.mkdir(exist_ok=True)
(work / "sub").mkdir(exist_ok=True)
(work / "hello.txt").write_text("line1\nline2\nline3\n")

# 1. List only directories, only files, and everything
def list_path(path):
    items = os.listdir(path)
    dirs = [i for i in items if os.path.isdir(os.path.join(path, i))]
    files = [i for i in items if os.path.isfile(os.path.join(path, i))]
    return dirs, files, items
print("1.", list_path(work))

# 2. Check access to a path
def check_access(path):
    return {"exists": os.path.exists(path), "readable": os.access(path, os.R_OK),
            "writable": os.access(path, os.W_OK), "executable": os.access(path, os.X_OK)}
print("2.", check_access(work / "hello.txt"))

# 3. Does the path exist? Then show filename and directory
def path_parts(path):
    if os.path.exists(path):
        return os.path.basename(path), os.path.dirname(path)
    return "Path does not exist"
print("3.", path_parts(work / "hello.txt"))

# 4. Count lines in a file
with open(work / "hello.txt") as f:
    print("4. lines:", sum(1 for _ in f))

# 5. Write a list to a file
fruits = ["apple", "banana", "cherry"]
with open(work / "list.txt", "w") as f:
    f.write("\n".join(fruits) + "\n")
print("5.", (work / "list.txt").read_text().split())

# 6. Make A.txt ... Z.txt
letters = work / "letters"
letters.mkdir(exist_ok=True)
for ch in string.ascii_uppercase:
    (letters / f"{ch}.txt").write_text("")
print("6.", len(os.listdir(letters)), "files made")

# 7. Copy contents of one file to another
with open(work / "hello.txt") as src, open(work / "hello_copy.txt", "w") as dst:
    dst.write(src.read())
print("7. same content:", (work / "hello_copy.txt").read_text() == (work / "hello.txt").read_text())

# 8. Delete a file only after checking it exists and we have access
def safe_delete(path):
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)
        return "deleted"
    return "cannot delete (missing or no permission)"
print("8.", safe_delete(work / "hello_copy.txt"), "|", safe_delete(work / "nope.txt"))

shutil.rmtree(work)  # tidy up
