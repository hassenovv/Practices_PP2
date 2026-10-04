import re 
import os

def change(text):
    x = re.sub("\\s", ":", text)
    x = re.sub("[.,]", ":", x)
    print(x)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'row.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        change(line)