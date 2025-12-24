# string slicing
str = "bioinformatics"
slice_str = str[11:14]
reverse_str = slice_str[::-1]
print(reverse_str)

another_str = reverse_str + ' ' + str[5:11]
print(another_str)

new_str = str[:3].upper() + str[3:]
print(new_str)


# modify a string
a_str = 'spam'
new_str = a_str[0:1] + 'l' + a_str[2:4]
print(new_str)