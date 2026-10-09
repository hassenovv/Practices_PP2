# Practice 6 - Create nested directories, list, find by extension
import os
from pathlib import Path

base = Path(__file__).parent / "demo"
os.makedirs(base / "a" / "b" / "c", exist_ok=True)   # nested folders
(base / "notes.txt").write_text("hi")
(base / "a" / "data.csv").write_text("1,2,3")
(base / "a" / "b" / "more.txt").write_text("hello")

print("getcwd:", os.getcwd())
print("listdir:", sorted(os.listdir(base)))

print("Only .txt files (everywhere inside):")
for p in base.rglob("*.txt"):
    print("  ", p.relative_to(base))
