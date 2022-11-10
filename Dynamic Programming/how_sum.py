def how_sum(target_sum, numbers, memo=None):
    if memo == None:
        memo = {}
    if target_sum in memo:
        return memo[target_sum]
    
    if target_sum == 0:
        return []
    if target_sum < 0:
        return None
    
    for num in numbers:
        remainder = target_sum - num
        remainder_result = how_sum(remainder, numbers, memo)
        if remainder_result != None:
            memo[target_sum] = remainder_result + [num]
            return memo[target_sum]

    memo[target_sum] = None
    return None

# m = target sum
# n = numbers.length

# Brute Force
# time: O(n^m * m)
# space O(m)

# Memoized
# time: O(n*m*m) -> O(n*m^2)
# space: O(m*m) -> O(m^2)
print(how_sum(7, [2,3]))
print(how_sum(7, [5,3,4,7]))
print(how_sum(7, [2,4]))
print(how_sum(8, [2,3,5]))
print(how_sum(300, [7, 14]))