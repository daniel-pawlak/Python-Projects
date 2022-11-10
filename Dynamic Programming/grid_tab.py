def grid_traveler(m, n):
    import numpy as np

    table = np.zeros((m + 1, n + 1), dtype='int64')

    table[1, 1] = 1

    for i in range(m+1):
        for j in range(n+1):
            current = table[i][j]
            if j + 1 <= n:
                table[i][j + 1] += current

            if i + 1 <= m:
                table[i + 1][j] += current

    return table[m][n]

print(grid_traveler(1, 1))
print(grid_traveler(3, 2))
print(grid_traveler(2, 3))
print(grid_traveler(3, 3))
print(grid_traveler(18, 18))