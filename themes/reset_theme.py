import sys

'''
    This script resets the theme to 'None'.
'''

# Reset the current theme to 'None'
with open(sys.path[0] + "/current.txt", "w") as currentfile:
    currentfile.write("None")
