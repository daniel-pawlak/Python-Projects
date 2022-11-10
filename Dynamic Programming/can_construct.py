def can_construct(target, word_bank, memo=None):
    if memo == None:
        memo = {}
    if target in memo:
        return memo[target]    
    if target == '':
        return True
    
    for word in word_bank:
        try:
            if target.index(word) == 0:
                suffix = target[slice(len(word), len(target))]
                if can_construct(suffix, word_bank, memo) == True:
                    memo[target] = True
                    return True
        except:
            pass

    memo[target] = False
    return False

print(can_construct('abcdef', ['ab', 'abc', 'cd', 'def', 'abcd']))
print(can_construct('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']))
print(can_construct('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't']))
print(can_construct('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee']))