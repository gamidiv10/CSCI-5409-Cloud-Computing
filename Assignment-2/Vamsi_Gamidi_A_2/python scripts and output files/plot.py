import matplotlib.pyplot as plt
values = []
times = []
with open('C:/Users/vamsi/Desktop/Assign-2/factorial_log.csv', 'r', newline='') as outputFile:
    for line in outputFile:
        x = line.split(',')
        print(x)
        values.append(int(x[0]))
        times.append(float(x[1].strip()))

plt.bar(values, times)
plt.show()


with open('C:/Users/vamsi/Desktop/Assign-2/fibonacci_log.csv', 'r', newline='') as outputFile:
    for line in outputFile:
        x = line.split(',')
        print(x)
        values.append(int(x[0]))
        times.append(float(x[1].strip()))

plt.bar(values, times)
plt.show()
