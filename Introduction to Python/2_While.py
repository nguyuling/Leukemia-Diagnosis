# Repetition: while

# example 1
x_int = 0
while x_int < 10:
    print(x_int, end=' ')
    x_int += 1

print("\nFinal value of x_int: ", x_int)


# example 2
carrot_supply = False
carrot_needed = int(input("How many carrots does Pinkie Bunnie need today: "))

while carrot_supply==False:
    print("Go farm carrot!")
    carrot_farmed = int(input("How many carrot(s) has Derfie Boo farmed today: "))
    if carrot_farmed >= carrot_needed:
        carrot_supply = True

print("Pinkie: Yayyy it's carrot time! I love my Derfie Boo <3")


# example 3
number = 7
guess_str = input("Guess a number: ")
guess = int(guess_str)

while 0 <= guess <= 100:
    if guess > number:
        print("Guessed too high.")
    elif guess < number:
        print("Guessed too low.")
    else:
        print("You guessed it. The number was:", number)
        break
    guess_str = input("Guess a number: ")
    guess = int(guess_str)  
else:
    print("You quit early, the number was:", number)


# example 4
number_str = input("Number: ")
the_sum = 0

while number_str != "." :
    number   