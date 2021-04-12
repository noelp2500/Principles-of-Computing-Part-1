# 2048 (Merge Function)
# Author - Noel Pereira
# Submission - http://www.codeskulptor.org/#user47_9GeGpJhMUe_0.py

####################################################################

"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    
    new_line = [value for value in line if value] + [0]*line.count(0)
    if len(new_line) < 2:
        return line
    if new_line[0] == new_line[1]:
        return [2*new_line[0]] + merge(new_line[2:]) + [0]
    else:
        return [new_line[0]] + merge(new_line[1:])
    
print merge([8, 16, 16, 8])