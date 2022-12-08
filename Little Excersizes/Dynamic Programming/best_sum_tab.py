def best_sum_tab(target_sum, numbers):
    import numpy as np

    table = np.full(target_sum + 1, None)
    table[0] = []

    for i in range(target_sum):
        if table[i] != None:
            for num in numbers:
                combination = table[i].copy()
                combination.append(num)
                if i + num < len(table):
                    if table[i + num] != None:
                        if len(combination) < len(table[i + num]):
                            table[i + num] = combination
                    else:
                        table[i + num] = combination
    return table[target_sum]
    
print(best_sum_tab(7, [2,3]))    # 3, 2, 2
print(best_sum_tab(7, [5,3,4,7]))    # 7
print(best_sum_tab(7, [2,4]))    # None
print(best_sum_tab(8, [2,3,5]))  # 3, 5
print(best_sum_tab(8, [2,7,5]))  # 2, 2, 2, 2 
print(best_sum_tab(100, [1,2,5,25])) # 25,25,25,25
print(best_sum_tab(300, [7,14])) # None