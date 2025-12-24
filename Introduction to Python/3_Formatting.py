# string formattng
print("Sorry, is this the {} minute {}?".format(5, 'ARGUMENT'))
print("{:<10s} is {:>10d} years old".format("Bill", 25))
for i in range(5): print("{:10d} {:4d}".format(i, i**2))
import math
print("pi is {:4f}".format(math.pi))
print("pi is {:8.4f}".format(math.pi))


# arg
print("{0} is {2} and {0} is also {1}".format("Bill", 25, "tall"))

print("{0:.>12s} / {1:0=+10d} / {2:->5d}".format("abc", 35, 22))

print("{:#6.0f}".format(3))
print("{:04d}".format(4))
print("{:,d}".format(1234567890))


# table
for n in range(3,11):
    print("{:4}-sides:{:6}{:10.2f}{:10.2f}".format(n, 180*(n-2), 180*(n-2)/n, 360/n))