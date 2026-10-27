import datetime
start = input()
exam1 = input()
exam2 = input()
exam3 = input()

converted_start = datetime.datetime.strptime(start, "%Y-%m-%d")
converted_exam1 = datetime.datetime.strptime(exam1, "%Y-%m-%d")
converted_exam2 = datetime.datetime.strptime(exam2, "%Y-%m-%d")
converted_exam3 = datetime.datetime.strptime(exam3, "%Y-%m-%d")

difference1 = converted_exam1 - converted_start
difference2 = converted_exam2 - converted_start
difference3 = converted_exam3 - converted_start

print("Exam 1:", difference1.days, "days")
print("Exam 2:", difference2.days, "days")
print("Exam 3:", difference3.days, "days")