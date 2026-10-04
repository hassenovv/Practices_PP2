import re
import os

def match_pattern(text):
    pattern = r'а.*б*'
    if re.search(pattern, text):
        return True
    else:
        return False

# Получаем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем полный путь к файлу JSON
file_path = os.path.join(current_dir, 'row.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if match_pattern(line):
            print(line)

