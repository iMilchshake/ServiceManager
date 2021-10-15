import random
import sys

print("Thanks for using TestService.py!")
if random.choice([True, False]):
    print("this script is doing hard work")
elif random.choice([True, False]):
    print("Warning: Something might be going wrong!", file=sys.stderr)
else:
    raise ValueError("script completely failed!")
print("The answer to the universe is 42!")
