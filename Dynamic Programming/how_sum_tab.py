def how_sum_tab(target_sum, numbers):
    import numpy as np

    table = np.full(target_sum + 1, None)
    table[0] = []

    for i in range(target_sum):
        if table[i] != None:
            try:
                for num in numbers:
                    table[i + num] = table[i] + [num]
            except:
                pass

    return table[target_sum]
    
print(how_sum_tab(7, [2,3]))    # 3, 2, 2
print(how_sum_tab(7, [5,3,4,7]))    # 3, 4 or 7
print(how_sum_tab(7, [2,4]))    # None
print(how_sum_tab(8, [2,3,5]))  # 2, 2, 2, 2
print(how_sum_tab(300, [7,14])) # None