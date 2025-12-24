# use type() to check the data type
str = "Hi mom"
print(str, type(str))
num_int = 7
print(num_int, type(num_int))
num_float = 7.0
print(num_float, type(num_float))
boolean = True
print(boolean, type(boolean))


# find a letter
river = "Mississippi"
target = input("Input a character to find: ")
for index in range(len(river)):
    if river[index] == target:
        print("Letter found at index: ", index)
        break
else:
    print("Letter", target, "not found in", river)
    
    
# find with enumerate
river = "Mississippi"
target = input("Input a character to find: ")
for index, letter in enumerate(river):
    if letter == target:
        print("Letter found at index: ", index)
        break
else:
    print("Letter", letter, "not found in", river)