""" enterapot nie działa"""
def all_construct_tab(target, word_bank):
    import numpy as np
    
    table = np.empty(len(target) + 1, dtype=object)
    table.fill([])
    table[0] = [[]]
    # print(table)
    for i in range(len(target)):
        for word in word_bank:
            if target[slice(i, i + len(word))] == word:
                # print(table)
                # if table[i] != [[]]:
                #     new_combinations = table[i] + [word]
                # else:
                #     new_combinations = [word]
                if table[i] != [[]]:
                    # new_combinations = table[i]
                    new_combinations = table[i].copy()
                    if len(new_combinations) > 1:
                        try:
                            for j in range(len(new_combinations)):
                                new_combinations[j].append(word)
                        except:
                            new_combinations.append(word)
                    elif len(new_combinations) == 0:
                        new_combinations.append(word)
                    else:
                        new_combinations[0].append(word)
                    # new_combinations[0].append(word)
                    # print('lennnnnn', len(new_combinations), new_combinations)
                else:
                    # new_combinations = [word]
                    if i == 0:
                        new_combinations = [[word]]
                    else:
                        new_combinations = [word]

                # new_combinations = table[i] + [word]
                
                if table[i + len(word)] == []:
                    table[i + len(word)] = new_combinations
                else:
                    # table[i + len(word)].append(new_combinations)
                    table[i + len(word)] = table[i + len(word)] + new_combinations
                # print('i:', i, '; table', table, '\n')
    
    return table[len(target)]

print(all_construct_tab('purple', ['purp', 'p', 'ur', 'le', 'purpl']))

print(all_construct_tab('abcdef', ['ab', 'abc', 'cd', 'def', 'abcd']))
print(all_construct_tab('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']))
print(all_construct_tab('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't']))
print(all_construct_tab('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee']))