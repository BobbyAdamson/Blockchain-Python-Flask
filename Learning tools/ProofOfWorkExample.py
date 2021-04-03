from hashlib import sha256

"""
  Example program implementing "proof of work"
  Where y is the proof we're looking for.
  Equation: sha256(x*y) where last character in the encoded hex is 0 i.e. sha256(x*y)[-1] = 0
  
  You solve for Y by brute forcing the product of x and y and hashing it until the last character is 0
"""

x = 5 # Known
y = 0 # The true Y is unknown, so we will brute force by incrementing and running hash again
expectedResult = "0"

while sha256(f'{x*y}'.encode()).hexdigest()[-1] != expectedResult:
  y += 1
  print(y, "     ",  sha256(f'{x*y}'.encode()).hexdigest())

print(f'The solution is y = {y}', "    ", sha256(f'{x*y}'.encode()).hexdigest())

