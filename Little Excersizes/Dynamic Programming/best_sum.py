def best_sum(target_sum, numbers, memo=None):
    if memo == None:
        memo = {}
    if target_sum in memo:
        return memo[target_sum]
    
    if target_sum == 0:
        return []
    if target_sum < 0:
        return None

    shortest_combination = None

    for num in numbers:
        remainder = target_sum - num
        remainder_combination = best_sum(remainder, numbers, memo)
        if remainder_combination != None:
            combination = remainder_combination + [num]
            if shortest_combination == None or len(combination) < len(shortest_combination):
                shortest_combination = combination

    memo[target_sum] = shortest_combination
    return shortest_combination

# m = target sum
# n = numbers.length

# Brute Force
# time: O(n^m * m)
# space O(m^2)

# Memoized
# time: O(m*n*m) -> O(n * m^2)
# space: O(m*m) -> O(m^2)

print(best_sum(7, [2,3]))
print(best_sum(7, [5,3,4,7]))
print(best_sum(7, [2,4]))
print(best_sum(8, [2,3,5]))
print(best_sum(300, [7, 14]))
print(best_sum(100, [7, 14, 25]))