number_str = input("Enter a positive integer: ")
number = int(number_str)
count = 0

print("Starting with number:", number)
print("Sequence is: ", end=' ')

while number > 1:
    if number%2: #odd
        number = number*3 + 1
    else: #even
        number = number/2
    print(number, ",", end=' ')
    count += 1

else:
    print("\nSequence is", count, "numbers long")