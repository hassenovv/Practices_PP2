import os
import re

def find_sequences(text):
    pattern = r'\b[А-Я]+[а-я]+\b'
    sequences = re.findall(pattern, text)
    return sequences

# Получаем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем полный путь к файлу JSON
file_path = os.path.join(current_dir, 'row.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        sequences = find_sequences(line)
        for seq in sequences:
            print(seq)