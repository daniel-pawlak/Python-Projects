def can_sum_tab(target_sum, numbers):
    import numpy as np

    table = np.full(target_sum + 1, False)
    table[0] = True

    for i in range(target_sum):
        if table[i] == True:
            try:
                for num in numbers:
                    table[i + num] = True
            except:
                pass

    return table[target_sum]

print(can_sum_tab(7, [2,3]))    # true
print(can_sum_tab(7, [5,3,4,7]))    # true
print(can_sum_tab(7, [2,4]))    # false
print(can_sum_tab(8, [2,3,5]))  # true
print(can_sum_tab(300, [7,14])) # false