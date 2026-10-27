from functools import reduce

nums = [1, 2, 3, 4, 5, 6]

# print("map (x2):      ", list(map(lambda x: x * 2, nums)))
# print("filter (even): ", list(filter(lambda x: x % 2 == 0, nums)))
print("reduce (product):", reduce(lambda a, b: a * b, nums)) # reduce applies a function to the items in nums, carrying the result forward each time.
# print("sorted (desc): ", sorted([5, 2, 9, 1], reverse=True))




# a,b,c = map(int, input().split())
# print(a,b,c)

# doubled = list(map(lambda x : x * 2, nums))
# print(doubled)

# numbers = list(map(int,input().split())) # Read three integers on one line and create a list containing their squares.
# print(list(map(lambda x: x*x,numbers)))

# syntax of map: map(function, iterable) function: what to do with each item, iterable: the collection of items to process, such as a list

# words = ["cat", "elephant", "dog"]
# print(list(map(len, words)))

# numbers = [-4, 0, 3, -1, 7]
# x = list(filter(lambda x: x > 0, numbers)) # only positive
# print(x)

# words = ["apple", "kiwi", "banana", "fig"]
# hmm = list(filter(lambda x: len(x) > 4, words))
# print(hmm)

# 7. From numbers = [1, 2, 3, 4, 5, 6], keep the even numbers, then square them. The result should be [4, 16, 36].
numbers = [1, 2, 3, 4, 5, 6]
output = list(filter(lambda x: x%2==0, numbers))
output2 = list(map(lambda z: z*z, output))
print(output2)