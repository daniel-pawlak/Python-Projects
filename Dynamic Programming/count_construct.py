def count_construct(target, word_bank, memo=None):
    if memo == None:
        memo = {}
    if target in memo:
        return memo[target]    
    if target == '':
        return 1
    
    total_count = 0
    for word in word_bank:
        try:
            if target.index(word) == 0:
                suffix = target[slice(len(word), len(target))]
                num_of_ways = count_construct(suffix, word_bank, memo)
                total_count += num_of_ways

        except:
            pass

    memo[target] = total_count
    return total_count

print(count_construct('purple', ['purp', 'p', 'ur', 'le', 'purpl']))
print(count_construct('abcdef', ['ab', 'abc', 'cd', 'def', 'abcd']))
print(count_construct('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']))
print(count_construct('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't']))
print(count_construct('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee']))