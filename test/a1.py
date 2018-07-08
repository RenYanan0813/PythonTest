

def a(a, b):
    return  a + b

c = a
import random
# print(str(random.choice(range(10))) for _ in range(9))

print(''.join(str(random.choice(range(10))) for a in range(4)))