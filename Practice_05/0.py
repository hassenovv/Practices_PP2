import re

def match_pattern(text):
    pattern = r'a.*b(?:.*b){1,2}'
    if re.fullmatch(pattern, text):
        return True
    else:
        return False

# Проверка работы функции
test_strings = ["a", "acb", "abb", "abbb", "ac", "abc", "aab", "abcb"]
for string in test_strings:
    if match_pattern(string):
        print(f"Строка '{string}' соответствует шаблону.")
    else:
        print(f"Строка '{string}' не соответствует шаблону.")
