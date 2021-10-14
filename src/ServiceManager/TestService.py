import sys

print("This could be some debug text!")
print("Warning: This is a Warning! Something is going terribly wrong", file=sys.stderr)
raise ValueError("Okay not a warning, script completely failed D:")
