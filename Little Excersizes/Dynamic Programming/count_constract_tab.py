def count_construct_tab(target, word_bank):
    import numpy as np
    
    table = np.zeros(len(target) + 1, dtype='int64')
    table[0] = 1

    for i in range(len(target)):
        for word in word_bank:
            if target[slice(i, i + len(word))] == word:
                table[i + len(word)] += table[i]

    return table[len(target)]

print(count_construct_tab('purple', ['purp', 'p', 'ur', 'le', 'purpl']))    # 2
print(count_construct_tab('abcdef', ['ab', 'abc', 'cd', 'def', 'abcd']))    # 1
print(count_construct_tab('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar'])) # 0
print(count_construct_tab('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't'])) # 4
print(count_construct_tab('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee'])) # 0