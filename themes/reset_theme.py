import sys

with open(sys.path[0] + "/current.txt", "w") as currentfile:
    currentfile.write("None")
