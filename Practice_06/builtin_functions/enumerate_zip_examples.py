# Practice 6 - enumerate, zip, type checking and conversion
names = ["Ann", "Bob", "Cara"]
scores = [90, 75, 88]

for i, name in enumerate(names, start=1):
    print(i, name)

for name, score in zip(names, scores):
    print(name, "->", score)

print(dict(zip(names, scores)))

value = "42"
print(type(value), isinstance(value, str))
print(int(value) + 1, float(value), str(3.5), list("abc"), bool(0), bool("x"))
