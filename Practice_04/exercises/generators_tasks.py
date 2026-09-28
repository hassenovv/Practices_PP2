# 1. Squares of numbers up to N
def squares_upto(N):
    for i in range(N + 1):
        yield i ** 2

# 2. Even numbers between 0 and n, comma separated
def evens(n):
    for i in range(0, n + 1, 2):
        yield i

# 3. Numbers divisible by 3 and 4 in range 0..n
def div_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4. squares(a, b): squares of all numbers from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

# 5. Countdown from n to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


if __name__ == "__main__":
    print("1:", list(squares_upto(5)))

    n = int(input("2: enter n: "))
    print(",".join(str(x) for x in evens(n)))

    print("3:", list(div_by_3_and_4(50)))

    print("4:")
    for v in squares(3, 7):
        print(v)

    print("5:", list(countdown(5)))
