def fib(n):
    import numpy as np

    table = np.zeros(n + 1, dtype='int64')

    table[1] = 1

    for i in range(n):
        table[i + 1] += table[i]
        if i != n-1:
            table[i + 2] += table[i]

    return table[n]

print(fib(6))
print(fib(7))
print(fib(8))
print(fib(50))