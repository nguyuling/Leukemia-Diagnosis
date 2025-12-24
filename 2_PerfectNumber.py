# Repetition: while

# Check if a number is perfect number
number = int(input("Enter a number: "))
divisor = 1
sum_of_divisors = 0
while divisor < number:
    if number % divisor == 0:
        sum_of_divisors += divisor
    divisor += 1

if number == sum_of_divisors:
    print(number, "is perfect")
else:
    print(number, "is not perfect")
    

# Check if a range of number contain perfect number
top_num = int(input("What is the upper number for the range: "))
number = 2
while number <= top_num:
    divisor = 1
    sum_of_divisors = 0
    while divisor < number:
        if number % divisor == 0:
            sum_of_divisors += divisor
        divisor += 1
    
    if number == sum_of_divisors:
        print(number, "is perfect")
    elif number < sum_of_divisors:
        print(number, "is deficient")
    elif number > sum_of_divisors:
        print(number, "is abundant")
    number += 1