import re
import os

def a_b(text):
    pattern = r'а.*л$' #нет строк заканчивающихся на б поэтому вместо б л для проверки
    if re.search(pattern, text):
        return True
    else:
        return False

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'row.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if a_b(line):
            print(line)