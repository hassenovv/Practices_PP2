# Practice 6 - map, filter, reduce + len/sum/min/max/sorted
from functools import reduce

nums = [1, 2, 3, 4, 5, 6]
print("len:", len(nums), "sum:", sum(nums), "min:", min(nums), "max:", max(nums))
print("map (x2):      ", list(map(lambda x: x * 2, nums)))
print("filter (even): ", list(filter(lambda x: x % 2 == 0, nums)))
print("reduce (product):", reduce(lambda a, b: a * b, nums))
print("sorted (desc): ", sorted([5, 2, 9, 1], reverse=True))
