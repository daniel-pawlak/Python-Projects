def all_construct(target, word_bank, memo=None):
    if memo == None:
        memo = {}
    if target in memo:
        return memo[target]    
    if target == '':
        return [[]]

    table_size = len(target) + 1
    table = []
    for i in range(table_size):
        table.append([])
    table[0] = [[]]
    
    for i in range(table_size):
        # condition
        if table[i] != []:
            for word in word_bank:
                # slice condition
                if target[i : i + len(word)] == word:
                    new_combinations = [[word] + way for way in table[i]]
                    # adds the word to every combination the current position holds
                    # now,push that combination to the table[i+len(word)]
                    table[i + len(word)] += new_combinations

    # combinations are in reverse order so reverse for better output
    for combination in table[len(target)]:
        combination.reverse()

    return table[len(target)]  

def all_construct2(target, word_bank, memo=None):
    from itertools import chain
    from functools import reduce
    if memo == None:
        memo = {}
    if target in memo:
        return memo[target]    
    if target == '':
        return [[]]
    
    result = []
    def flat2gen(alist):
        for item in alist:
            if isinstance(item, list):
                for subitem in item: yield subitem
            else:
                yield item

    for word in word_bank:
        try:
            if target.index(word) == 0:
                # print('ok')
                suffix = target[slice(len(word), len(target))]
                # print(suffix)
                suffix_ways = all_construct2(suffix, word_bank, memo)
                # target_ways = [[word] + suffix_ways[i] for i in range(len(suffix_ways))]
                target_ways = list(flat2gen([[word] + suffix_ways[i] for i in range(len(suffix_ways))]))
                # print('suf', list(flat2gen(target_ways)))
                # target_ways = [[word] + [*suffix_ways[i]] for i in range(len(suffix_ways))]
                # print(target_ways)
                # print(suffix_ways)
                result.append(target_ways)
        except:
            pass

    return result

def all_construct3(target, word_bank, memo=None):
    if memo == None:
        memo = {}
    if target in memo:
        return memo[target]    
    if target == '':
        return [[]]
    
    result = []

    def flat2gen(alist):
        for item in alist:
            if isinstance(item, list):
                for subitem in item: yield subitem
            else:
                yield item

    for word in word_bank:
        try:
            if target.index(word) == 0:
                suffix = target[slice(len(word), len(target))]
                suffix_ways = all_construct2(suffix, word_bank, memo)
                target_ways = list(flat2gen([[word] + suffix_ways[i] for i in range(len(suffix_ways))]))
                result.append(target_ways)
        except:
            pass

    if result[-1] == []:
        result.pop(-1)

    memo[target] = result
    return result

print(all_construct3('purple', ['purp', 'p', 'ur', 'le', 'purpl']))
print(all_construct('abcdef', ['ab', 'abc', 'cd', 'def', 'abcd']))
print(all_construct('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']))
print(all_construct('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't']))
# print(all_construct('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee']))