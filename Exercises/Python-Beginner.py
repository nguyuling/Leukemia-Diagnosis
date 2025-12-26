import sys

#! I. Exercise programs on basic control structures & loops
print("I. CONTROL STRUCTURES & LOOPS")

# a) Check if number is even or odd
print("\nI.a) Check if number is Even or Odd")
print("-" * 70)
def check_even_odd(num):
    if num % 2 == 0:
        return f"{num} is Even"
    else:
        return f"{num} is Odd"

test_numbers = [10, 15, 42, 7]
for num in test_numbers:
    print(check_even_odd(num))

# b) Print decimal equivalents of 1/2, 1/3, 1/4, ..., 1/10
print("\nI.b) Decimal Equivalents of 1/2 to 1/10")
print("-" * 70)
for denominator in range(2, 11):
    decimal_value = 1 / denominator
    print(f"1/{denominator} -> {decimal_value:.6f}")

# c) Display reversal of a number
print("\nI.c) Reversal of a Number")
print("-" * 70)
def reverse_number(num):
    return int(str(abs(num))[::-1]) * (-1 if num < 0 else 1)

test_nums = [12345, 9876, 100, -5432]
for num in test_nums:
    print(f"{num:6d} -> {reverse_number(num):6d}")

# d) Find biggest number among 3 numbers
print("\nI.d) Find Biggest Number Among 3 Numbers")
print("-" * 70)
def find_biggest(a, b, c):
    return max(a, b, c)

test_triples = [(10, 20, 15), (50, 30, 70), (5, 5, 5)]
for triple in test_triples:
    biggest = find_biggest(triple[0], triple[1], triple[2])
    print(f"{triple} -> Biggest: {biggest}")

# e) Countdown from user number to zero using while loop
print("\nI.e) Countdown from N to 0 (using while loop)")
print("-" * 70)
def countdown(n):
    count = n
    countdown_list = []
    while count >= 0:
        countdown_list.append(count)
        count -= 1
    return countdown_list

test_countdown = countdown(5)
print(f"Countdown from 5 to 0: {' -> '.join(map(str, test_countdown))}")


#! II. Exercise programs on operators & I/O operations
print("\n\nII. OPERATORS & I/O OPERATIONS")

# a) Sum of 2 numbers (command line arguments)
print("\nII.a) Sum of 2 Command Line Arguments")
print("-" * 70)
if len(sys.argv) > 2:
    try:
        num1 = int(sys.argv[1])
        num2 = int(sys.argv[2])
        print(f"Input: {num1} and {num2}")
        print(f"Sum: {num1} + {num2} = {num1 + num2}")
    except ValueError:
        print("Please provide valid integers as command line arguments")
else:
    # Demo with sample numbers
    num1, num2 = 25, 35
    print(f"Input: {num1} and {num2}")
    print(f"Sum: {num1} + {num2} = {num1 + num2}")

# b) Usage of various operators
print("\nII.b) Usage of Various Operators in Python")
print("-" * 70)
a, b = 15, 4
print(f"a = {a}, b = {b}")
print(f"Arithmetic Operators:")
print(f"  a + b = {a + b} (Addition)")
print(f"  a - b = {a - b} (Subtraction)")
print(f"  a * b = {a * b} (Multiplication)")
print(f"  a / b = {a / b:.2f} (Division)")
print(f"  a // b = {a // b} (Floor Division)")
print(f"  a % b = {a % b} (Modulus)")
print(f"  a ** b = {a ** b} (Exponentiation)")
print(f"Comparison Operators:")
print(f"  a > b: {a > b}, a < b: {a < b}, a == b: {a == b}")
print(f"  a >= b: {a >= b}, a <= b: {a <= b}, a != b: {a != b}")
print(f"Logical Operators:")
print(f"  (a > 10) and (b < 10): {(a > 10) and (b < 10)}")
print(f"  (a > 10) or (b > 10): {(a > 10) or (b > 10)}")
print(f"  not (a == b): {not (a == b)}")
print(f"Bitwise Operators:")
print(f"  a & b (AND): {a & b}, a | b (OR): {a | b}, a ^ b (XOR): {a ^ b}")

# c) Check voting eligibility based on age
print("\nII.c) Check Voting Eligibility Based on Age")
print("-" * 70)
def check_voting_eligibility(age):
    if age >= 18:
        return f"Age {age}: Eligible for voting"
    else:
        return f"Age {age}: Not eligible for voting"

test_ages = [16, 18, 21, 17, 25]
for age in test_ages:
    print(check_voting_eligibility(age))

# d) Check if year is leap year
print("\nII.d) Check if Year is Leap Year")
print("-" * 70)
def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False

test_years = [2020, 2021, 2024, 1900, 2000]
for year in test_years:
    result = "Leap Year" if is_leap_year(year) else "Not a Leap Year"
    print(f"{year}: {result}")


#! III.	Exercise programs on Python Script
print("\n\nIII. PYTHON SCRIPTS")

# a) Generate first N natural numbers
print("\nIII.a) Generate First N Natural Numbers")
print("-" * 70)
def first_n_natural_numbers(n):
    return list(range(1, n + 1))

n = 10
result = first_n_natural_numbers(n)
print(f"First {n} natural numbers: {result}")

# b) Check if number is palindrome
print("\nIII.b) Check if Number is Palindrome")
print("-" * 70)
def is_palindrome(num):
    str_num = str(abs(num))
    return str_num == str_num[::-1]

test_palindromes = [121, 123, 1001, 999, 12321, 100]
for num in test_palindromes:
    result = "Palindrome" if is_palindrome(num) else "Not a Palindrome"
    print(f"{num}: {result}")

# c) Print factorial of a number
print("\nIII.c) Factorial of a Number")
print("-" * 70)
def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

test_factorials = [0, 1, 5, 10]
for num in test_factorials:
    fact = factorial(num)
    print(f"  {num}! = {fact}")

# d) Sum of N natural numbers
print("\nIII.d) Sum of N Natural Numbers")
print("-" * 70)
def sum_n_natural_numbers(n):
    # Method 1: Using formula
    formula_result = n * (n + 1) // 2
    # Method 2: Using loop
    loop_result = sum(range(1, n + 1))
    return formula_result, loop_result

test_n_values = [1, 5, 10, 20, 100]
for n in test_n_values:
    formula, loop = sum_n_natural_numbers(n)
    print(f"Sum of first {n:3d} natural numbers: {formula:6d} (Formula: n*(n+1)/2)")