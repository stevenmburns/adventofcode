class Leaf:
    def __init__(self,c):
        self.c = c
    def __repr__(self):
        return self.c

def isvalid( tbl, state, seq):

    print(state,seq)

    def inner( lst, cursor):
        print( 'inner:', lst, cursor)
        new_cursor = cursor
        valid = True
        for term in lst:
            new_valid, new_cursor = outer( term, new_cursor) 
            if not new_valid:
                valid = False
        return valid, new_cursor

    def outer( lst_of_lst, cursor):
        if type(lst_of_lst[0][0]) == Leaf:
            yield lst_of_lst[0][0].c == seq[cursor], cursor+1
        else:
            for terms in lst_of_lst:
                yield inner( terms, cursor):

    valid, new_cursor = outer( tbl[state], 0)
    return valid and new_cursor == len(seq)

def tokenize(line):
    return line.split(" ")

def main():
    rules = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

bababa
abbbab
aaabbb
aaaabbb
"""



    messages_now = False
    messages = []

    tbl = {}
    for line in rules.split('\n'):
        state = None
        expr = []
        term = []
        for token in tokenize(line):
            if messages_now:
                if len(token) == 0:
                    pass
                else:
                    messages.append(token)
            else:
                if len(token) == 0:
                    messages_now = True
                elif token[-1] == ':':
                    state = int(token[:-1])
                elif token == '|':
                    expr.append(term)
                    term = []
                elif token[0] == '"':
                    term.append(Leaf(token[1]))
                else:
                    term.append(int(token))
        if not messages_now:
            expr.append(term)
            tbl[state] = expr
    print(tbl,messages)

    count = 0
    for message in messages:
        if isvalid( tbl, 0, message):
            count += 1

    print(f"count: {count}")
    
def test_A():
    main()
