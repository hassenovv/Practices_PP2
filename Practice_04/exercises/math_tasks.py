import math

# 1. Degree to radian
deg = float(input("Input degree: "))
print("Output radian:", round(math.radians(deg), 6))

# 2. Area of a trapezoid
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
print("Expected Output:", (b1 + b2) / 2 * h)

# 3. Area of a regular polygon: n * s^2 / (4 * tan(pi / n))
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area = n * s ** 2 / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(area))

# 4. Area of a parallelogram
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
print("Expected Output:", base * height)
