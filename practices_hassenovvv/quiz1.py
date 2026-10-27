"""
### Task 1

Given a range from **A** to **B** and a number **K**, count how many numbers in the range are divisible by **K**. Read **A**, **B**, and **K** on one line. Write a function to solve this task.

### Task 2

The first input is the number of values. The second input contains all the values on one line. Find their sum and average, then count how many values are greater than the average.

"""
# splitlines for what is used
n = int(input())
x = list(map(int,input().split()))
average = sum(x) / n
count = 0
for i in x:
    if i > average:
        count+=1

print(count)

def count(a,b,k):
    count = 0
    for i in range(a,b):
        if i % k == 0:
            count +=1
    print(count)

a,b,k = count(map(int, input().split))
