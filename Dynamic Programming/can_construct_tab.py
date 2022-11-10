def can_construct_tab(target, word_bank):
    import numpy as np
    
    table = np.full(len(target) + 1, False)
    table[0] = True

    for i in range(len(target)):
        if table[i] == True:
            for word in word_bank:
                if target[slice(i, i + len(word))] == word:
                    table[i + len(word)] = True

    return table[len(target)]

print(can_construct_tab('abcdef', ['ab', 'abc', 'cd', 'def', 'abcd']))  # true
print(can_construct_tab('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']))   # false
print(can_construct_tab('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't'])) # true
print(can_construct_tab('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee']))  # false