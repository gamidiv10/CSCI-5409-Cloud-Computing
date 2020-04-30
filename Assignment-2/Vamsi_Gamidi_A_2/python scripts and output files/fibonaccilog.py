import sys
import csv
from timeit import Timer
import numpy as np
import matplotlib.pyplot as plt
sys.setrecursionlimit(150000)

with open("C:/Users/vamsi/Desktop/Assign-2/input.txt", 'w+') as outFile:
    for i in range(100):
        outFile.write(str(np.random.randint(1, 100))+'\n')

def fibonacci(num): 
    if num == 1: 
        return 0
    elif num == 2: 
        return 1
    else: 
        return fibonacci(num - 1) + fibonacci(num - 2) 

with open('C:/Users/vamsi/Desktop/Assign-2/fibonacci_log.csv', 'w', newline='') as outputFile:
    writer = csv.writer(outputFile)
    with open("C:/Users/vamsi/Desktop/Assign-2/input.txt", 'r') as inputFile:
        for line in inputFile:
            timeTaken = Timer(lambda: fibonacci(int(line)))
            writer.writerow([line.strip(), timeTaken.timeit(number=1)])


