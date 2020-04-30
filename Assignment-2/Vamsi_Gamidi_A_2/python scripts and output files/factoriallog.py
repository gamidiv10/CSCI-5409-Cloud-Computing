import sys
from timeit import Timer
import csv
import numpy as np
from time import time_ns

with open("C:/Users/vamsi/Desktop/Assign-2/input.txt", 'w+') as outFile:
    for i in range(100):
        outFile.write(str(np.random.randint(1,100))+'\n')

def factorial(num):
    if num == 1 or num == 0:
        return 1
    return num*factorial(num-1)

with open('C:/Users/vamsi/Desktop/Assign-2/factorial_log.csv', 'w', newline='') as outputFile:
    writer = csv.writer(outputFile)
    with open("C:/Users/vamsi/Desktop/Assign-2/input.txt", 'r') as inputFile:
        for line in inputFile:
            timeTaken = Timer(lambda: factorial(int(line)))
            writer.writerow([line.strip(), timeTaken.timeit(number=1)])


