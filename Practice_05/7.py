import os
import re

def makeuppercase(match):
    return match.group(2).upper() + match.group(3)

def camel(text):
    pattern = r'(_)(\w)([а-я]*)'
    if re.search(pattern, text):
        print(re.sub(pattern, makeuppercase, text))

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'row.txt')

with open(file_path, 'r',encoding='utf-8') as file:
    for line in file:
        camel(line)