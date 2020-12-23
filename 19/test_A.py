class Leaf:
    def __init__(self,c):
        self.c = c
    def __repr__(self):
        return self.c

from logging import debug

def isvalid( tbl, state, seq):

    debug("="*80)
    debug(f"isvalid: {state} {seq}")

    def aux( lst_of_lst, *, level):
        nonlocal cursor
        debug( f"{' '*(3*level)}aux: {lst_of_lst} {cursor}")
        save_cursor = cursor
        for terms in lst_of_lst:
            debug(f"{' '*(3*level)}setting cursor to {save_cursor}")
            cursor = save_cursor
            failed = False
            for term in terms:
                if failed: continue
                debug( f"{' '*(3*level)}term {term} cursor {cursor}")
                if type(term) == Leaf:
                    debug( f"{' '*(3*level)}Leaf {cursor} {seq} {term.c}")
                    if cursor < len(seq) and term.c == seq[cursor]:
                        debug( f"{' '*(3*level)}Match {cursor} {seq} {term.c} {seq[cursor]}")
                        cursor += 1
                    else:
                        failed = True
                else:
                    debug( f"{' '*(3*level)}non-Leaf: {term} {cursor}")
                    if not aux( tbl[term], level=level+1):
                        failed = True
                debug( f"{' '*(3*level)}end of terms loop: {cursor}")

            debug( f"{' '*(3*level)}end of lol loop: {failed} {level} {cursor}")
            if not failed and level > 0:
                return True
            if not failed and level == 0 and cursor == len(seq):
                debug( f"{' '*(3*level)}Found")
                return True

        return False

    cursor = 0
    return aux( tbl[state], level=0)

def main(txt):

    messages_now = False
    messages = []

    tbl = {}
    for line in txt.split('\n'):
        state = None
        expr = []
        term = []
        for token in line.split(" "):
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
    debug(tbl,messages)

    count = 0
    for message in messages:
        if isvalid( tbl, 0, message):
            count += 1

    print(f"count: {count}")
    return count
    
def test_A():
    txt = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

    assert main(txt) == 2

def test_AA():
    txt = """0: 4 5 | 4 0 5
4: "a"
5: "b"

a
b
ab
aabb
aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbb
aabbb
"""
    assert main(txt) == 3

def test_AAA():
    txt = """0: 2
2: "a" 2 "a" | "a" "a"

aaaa
aa
"""
    assert main(txt) == 1


def test_B():
    txt = """0: 1 2
1: "a"
2: "b"

ab
aba
ba
a
b
"""

    assert main(txt) == 1


def test_C():


    txt = """60: 117 7 | 89 13
38: 7 45 | 13 32
77: 7 51 | 13 48
23: 72 13 | 27 7
61: 105 7 | 7 13
103: 7 121 | 13 112
76: 88 13 | 124 7
28: 61 13 | 27 7
24: 7 17 | 13 33
115: 128 13 | 126 7
82: 13 73 | 7 64
107: 130 13 | 1 7
49: 59 7 | 100 13
131: 86 7 | 87 13
53: 7 105 | 13 13
27: 105 105
21: 7 13 | 13 7
84: 7 26 | 13 32
62: 90 13 | 94 7
18: 93 13
65: 75 13 | 40 7
39: 13 93 | 7 95
6: 7 38 | 13 25
64: 99 7
73: 7 93 | 13 32
101: 13 81 | 7 19
116: 13 39 | 7 122
55: 13 32 | 7 53
48: 13 91 | 7 61
93: 13 13
108: 7 7 | 13 105
94: 13 91 | 7 32
118: 13 79 | 7 57
41: 7 21 | 13 32
113: 7 61 | 13 26
74: 7 53 | 13 93
52: 55 13 | 70 7
5: 108 13 | 27 7
30: 14 7 | 50 13
7: "a"
50: 13 23 | 7 111
32: 13 7 | 13 13
92: 114 13 | 125 7
89: 108 7 | 72 13
9: 7 28 | 13 127
35: 7 131 | 13 47
86: 26 13 | 108 7
67: 7 44 | 13 69
44: 7 80 | 13 22
46: 7 67 | 13 35
111: 32 7 | 72 13
11: 42 31
112: 13 91 | 7 2
99: 7 7
81: 72 7 | 26 13
123: 37 13 | 20 7
45: 7 13 | 13 13
56: 119 13 | 112 7
63: 13 61 | 7 95
57: 7 9 | 13 83
3: 13 106 | 7 43
97: 84 13 | 73 7
85: 13 93 | 7 108
117: 7 53 | 13 21
47: 16 7 | 54 13
71: 129 7 | 63 13
95: 13 13 | 7 7
37: 26 13
2: 7 13 | 13 105
72: 7 13 | 7 7
43: 85 13 | 16 7
4: 130 7 | 25 13
69: 7 22 | 13 80
68: 93 7 | 32 13
22: 45 13 | 53 7
78: 13 2 | 7 27
14: 28 13 | 119 7
17: 13 60 | 7 6
129: 91 7 | 32 13
87: 26 7
79: 58 7 | 107 13
130: 13 72 | 7 91
90: 7 45 | 13 2
8: 42
114: 13 30 | 7 34
66: 61 7 | 93 13
128: 7 108 | 13 72
31: 13 36 | 7 15
127: 13 108 | 7 32
110: 73 13 | 29 7
58: 7 113 | 13 48
120: 7 56 | 13 97
19: 13 53 | 7 2
83: 13 78 | 7 74
34: 7 110 | 13 4
75: 7 102 | 13 52
25: 13 72 | 7 95
16: 7 72 | 13 21
100: 13 82 | 7 116
42: 13 92 | 7 10
119: 13 2 | 7 95
88: 71 13 | 101 7
126: 13 72 | 7 61
33: 96 13 | 123 7
1: 61 7 | 53 13
96: 55 7 | 41 13
102: 7 104 | 13 87
98: 91 13 | 91 7
104: 26 13 | 32 7
51: 7 95 | 13 26
125: 13 120 | 7 3
91: 13 7
13: "b"
10: 65 7 | 46 13
105: 13 | 7
59: 13 115 | 7 77
106: 5 13 | 66 7
80: 72 13 | 53 7
20: 93 7 | 61 13
15: 118 7 | 76 13
70: 91 13 | 93 7
29: 13 26 | 7 21
122: 7 26 | 13 72
124: 12 13 | 109 7
26: 7 13
121: 91 7
36: 13 49 | 7 24
12: 68 13 | 98 7
109: 18 7 | 23 13
54: 13 108 | 7 61
0: 8 11
40: 7 103 | 13 62

abbabbaabaaaabbaabaabbbbabaaaabb
abbababaabbbbbbaababaaababaabbbb
bbabbbabbabbaaaaaaabbbbbaabaababbbababbaaabbabaa
abaabbaaabbbbabbbabbaaaabbaababb
bbaaaaabbbbbbaabbabbbabaaabaabba
bababaabbaabbbbbbbabbbaa
abbababbababbaabbababababbbbbaaababaaaaaabababaa
abbbaabbabbbabbabbabbaabaabbaaaa
abbaaaabbbbabbaaaabababb
babbaaabaababbababbbbbaaaababbaaababbbaabbbaaaba
abbbabbbabbbaaaaaabababababbbbaabaaaabbbbabbabbabaaabaaaabababba
aababbaaabbaabbbaababbbbaabbbabaaaaababb
aaaaababaababbabbbaabbbaaabaabbabbbaaaaa
baabaababababbabaabbbbbaabbabaaabbaaaabaaaababbbbabaabbb
bbaaaaabbababaaaabaaabbabbabbabbbaaabaabbabaabab
bbbbbabaaaaabbbabbaaaabb
bbbaaabbabbabbaaaababaab
bbaaabbbbbbabbababaaaaaa
abaabbabbbbbbbbabbabbbbabbaaaabaaaaababa
bbababbaabaaaaabbbaabbaabbabaabbbbbbbbbabbabbbaaabaaaabb
bbabbbbbbbabbbbbbbaaaaaa
aabbaabbbaaaaabaabbbbbaabaabbabbaabababb
bbabbabbaababbabababbbbababbbabaababbbbbabbabbbbbaababba
bababaabbabbbbaaabbabbab
bbbbaaabbbbbbabbbbbbbbbabbabbabaabbabbaaabaabaab
bbabbaabababbaaabaabaaab
abaaaaaababbabaabaabbbaa
aabaabaabaaabaabbbabbaaabbbabbbbbabaababbabbbbbb
bbabaabbbbbbbabababbbababaaababaaababbabbaabbaabbabaabab
abbbbbaababababaabbaabbbaabbababbbbaaaaa
bababbbbbbbaabbabbbbbbbaabaaabaaaabbaaba
babaaababbaaaaabbbaaaaabaaababababbabbbb
baaabbbbbabaaabbaaabaabababbabbaaaabaaaabbaabababababbaa
baabbaaababbaaabbabbaaabbbaaaabaabaaaaaa
bbbabbaabbaabbababbaaaabbbbabbbabbaabaab
aababaaaabaabbababbaaabbbaababbaabbbbaaa
baaaabaabbaabbbaaaababbbaaaaabaabbbaaaba
abbbaabababbbbbabbabbabaababbbba
babaabbabbabbaabaaababbbaabbbbababbbabbbaabbbbaabbaabaab
aabaabaaabbababaabbaabbbbaabbbaaabbabbbb
bbaabbababbaaabbabbbaaaaabaaaaabbbabbbbababaababbaaababb
baaaaaabaabaabbaabbbbabbaabbabbbaabaaaabababbaaaaaabaaab
babbaaaaaaabaaabbbaabbabababbaba
aaaabbabbbbabbaabbaabbab
aababaaababbababaabbbbabbbabaaaababbbbab
abbaaaabaaabaaaaaabaaaaa
aaabaaabaababbbbaabababb
aabbbaaabababbbbabbaaabbaabaaaabbbaababa
babaaababbabaaababbabaabbabbaaaa
bbabbabbbbbbbabbbbabaaab
bbabbbabaababbabababbaabaaabaaabaabaaaba
aaabaaababbababaabaaabbababbbbab
abbbababbbabbbabbbbaabbbababbbaaabbabbbbabbaaaaa
abbaababbbbaabbbaabbaaaa
bbabbaabbaabbbbbaabaabba
abbaabbbaabbbaaababaabbabaaabbbbbabaaaaaaabbbbbb
bbabbbbaaabbaaaabbbaaaabaaaaaaaabbbbaaaa
babaabbababbaabbabbbbabbbabbbabaabbaababbababbbbabbbaaab
babbbbaaabbbbbbbabbabbab
babababababbaababaabaaaa
bbabababbababaaaaaabaabb
aaabaaaabbbbbabbaabbaaaa
abbbabaabbabbbbaabaaaaba
aaabaaabaaaabbababababaa
bbabbaababbbababbbababaa
aaabaaabbabababaabaababbaababababaababbbabbabbbabababbaa
bbbaabbbabbbbbbbaaabaabb
abaabbaabbbbbaaaaaaaaabbbbbaaaabaaababaa
bbbabbbbaababaaabaabbaab
aababababaabbabbbbbabababbbabbba
bbbaabbbbaaaaaaaabaabbbabbaaabbbabbaabbabbbabbbababbbbab
aaaaaababbaaaaaababbaabb
bbbabbbbbbbaabbbbbaaaaabbaababbabbabaaab
abbabaabaababbababaabbbabbababbaaabbaabaaabbbbbbbbababaabaaaabbb
aabaabbaabbabbbabbaaaabbababaaba
bababaaabaabababbaabababbaaabaabbbbbbaaaabaabaabbaaaabbbabbbaaab
aababbbbbabbaabbbaabbaab
bbaabbbabaaaabaaaabbabbbbbaabbbbababaabbaabaabbaabababba
abbbaaaaabaabbabbbabaabbabaabbab
bbaaaaababaaaaabbbbaaaab
babbaaaabbaaabbbaabababbabbaabbbbbbaaaaaaaabbaaabaababbaaabaabaabbaaaaabaabaabba
babaaabaabbbabbabbbbbbbabbbbbbab
abaababbbbaaabababbaaaabbabaabbaaaabbbba
babababababaaababbbbbababbbabbabaaabbbbbaaabaaaaabbabaaa
bbaaaaabbbbaababbbabbaabbbaababa
babababaabbbbbbabbabaaaa
ababaaaaababbbaaabbbaababbababaa
aaaabbbaaabbbaaaabbbbbbabaaaaababaaababb
abbbababbbaaaaabbbbbbaaababaaaaabaaaababbaababbb
aaaababbbaaabaaabbbbaaba
bbbaabababbbabbabaaaaababbaabbbbaababbbbabbaabaaabbaabaabaaaabba
abbbbbbbbbbaaaaabaabaaaabababbababababab
babbbbbaabbbaabbabbbbbbaaabaababaaabaaaabbbaababaaaaaababbabaaba
babbabbbbbaaabbbbbbabbabbbaaaaaa
aababbaaaaaaababbbabbabaaababbaa
babbaababbbbbabaaaaaaaababaaabbabbabbbbb
bbbbbaaabbbabbababaaabbaaabbbaaaabaabaaaaaaababa
aaaaabbbbbaaaaababbbbbaabbaabbabbbbaaaaaaaababbabaaababbabaaabab
bbbababbaabaaaabbbaabbbababbaaabababbbabbbbbabbaabaaabbb
bbabbaaabaaababababaaabbbbaaaaabbbbbaabbababbbbbabaabaab
aabaababaababbaaabaaaaababaabbaaaabbbbbb
babbbababbbabaabbaaaabba
bbababbabbbababbababaaaabaaaaababaabababbbbbabbabababbba
babbbbaabaaabaabbbaaaaba
baaabaabbbbaabbbabaaabab
abbaaabbbbbabbbbbababbba
abbaaaabaaababbbabbbbbbbaababaaaaaaabaab
baaaababbbbabaabbbabbaabbbaabbabbabaabbb
abbabbaabbbaaabbaababaaabbbbbabbbabaaaaaaabaaaaa
aabbbaaabbbbbbaabbababbaabbabaabbbaaaabb
aaabaaaaaaabaaaaaabbbaab
abbabbaaaabbabababaabbaabbbbababababbbab
aaabaababbbbbbaaabbbaabaabbabaaababbbbab
abbababbbbaaabbbaabbbbba
bbababbaababaaaabbbbaaabbbabbababbbaabaa
bbabaaaabbbbaaaabbbbabaa
abaabbaababbbbbaabbbabaaababbbaaababaabb
abbabaabaababbbaaabbbabbabbbababbbbbaabb
bbbababbabbababababbbaaa
baaaabaaabbbbabababaababbabbabba
babbababbaaabaabbaaaabaaabbbaaaabbaababbabbabbabbbbabaaa
ababbbaababaabbabbabbababbbbbaaabaabbbbaaababaababababaababbbaab
aabaaaabaabbababaababbaaabababaaaaabbaaa
abbbbbbabbabbabbababbbab
babbaaaabbbbbabbbabbababaaaabbaa
bbbbbbaaaabaabbbbaaaabba
ababbbbbabbabaabbabababaaabaaababaabbbbbbbbabbaaabaaaabb
aaaabbabbaabbabbaababaaaaaabbaaa
abbabbbbbaabbaabababbaaa
abaababbaabaaaabababbbbb
baaabababbaabaaaaababaaaababaaba
aabaabababbbbbaaaabababb
aabaabaaaaabbbbbbabaaaaaabbaabbbaaaababaaabababb
bbbbbabbabbbabaaababbaaaaaabbaaaaaabbbba
bbaaaaababaabbbaabbaabbbabbbabbb
abaaaaabbabbaababbbaabbaaaaaabbaabbbbaaa
bbaabbaaabbbababbabbbaaa
abaabaaaababbbaabbbbbaaaabbbbbbaabbbbbaabbabbaaa
bbbbbbbaababaabbbabbbbbaaaababbbbbbbbabbabbabbbbaabbbbbb
bbaabbbaabaababbaaaaabba
abbaababbbaabbabbbbaabaaabbbbbabaaaabbaabaababbb
baabbbabaababbbaaababbabbabbbbaaaabbaaaabaaabbabbabbabbabaaabaaabbababbb
bbbabaabbabbbbaababbbbaaaabaaabb
bbabbaabbabbababbbbabbaaaaaaaabbaabaaaaaaabbbbba
bbbbbaabbabbaaaababbaaaaabbbbabbbbabaaba
baaababbbabaababbbbaabbbababbaab
baabbbbababaaaaaabababaa
abaabbbabbaabbbbabaabbbabbaaababbbbbabaa
bbbbbbbaabaabbbaababbbab
bbaaaaabbaabababbaaaaaaabababbbababbbbab
aabbaabbbbabbabaababbbab
babbabbaaabbbbababbbbbaabbaaabaabbbbabba
bbabbabaaabbaaabababbbbabaababbb
ababbbbabbbbbaabbbbabbbbaabbbabbbabbbbab
bbaabaaababbbabaaabbabaa
abbaaabbbbaabbbbabbababaabbbabbbaaaababa
bbbabbabbbbbababaaabbbba
aabbababbaaaababbbbababbbababaabbaaaaaaababbabaaababbbabaabbbbbb
aaabaaababaabbbabaaaababbababbaa
bbbaaabbabaabbaabababaabaaabaabb
aabbbaaaaaabbabbbbaaabbaaaababaaaabbbaaa
bbbaabbabbabbaaababbbbba
bbabababbbababaababaaaababaaaaabaaabbbbbbabbbabbabbabbab
aabaababbbbbbbbabbabbabaaababaaabaaaaababaaaaabbbaabbaba
aaababbbabbabaaaabaabaabbbbbbbbbaaaaabababaaaabaaabbbbbaabbbbbabbabaaaaa
baaaabaababbaaabbabaaabbabbaabba
abbbbabbbbbbbabbbaabbbab
bbbbbabbbbbbbabbbaabbbbbbbbbbbbabaabbabaaaaaaaaa
bbabaabbaabbbbabbabbaabaabaaaaab
bbabaabbbbbbbababbbbbbbb
bbabbaaababbabbaaaabaababbabababbaaabaabaabaabbabbaaaaababbbabaaabbbabbbabbaabaa
abbbabbabbbbbabaaaabababaabababaaabaababbaabbbbbbaaabaaa
baaaabaabbbaaabbabbaaaab
bababbaabbbabaaaabbaabaabaaabbbbabaaaaabbbaaabbb
bbbabaabbbaaabaabbabababaabbabababbaaaaabbbbabbabaabbaba
abaaaabbbabbbabaaababbababbbbaabbaabbbbbbbbabbba
bbabbabaabbbbbbaabaaabbabaabbbbbbbaababaaabaabbaababbabb
baaabbbbbabaaabaaaaaababbaaabbbabaabbababaaabaaabaabbaab
abbbbbaabbbbbbbaaabbbbabaabaabba
aaabbbabbabbbabaaaaabaab
bbababbabaabbabbbbaaaababbbbbabbababbaba
bbabababaabaabaaaabaabaaaababbbabbabaaaa
bbaaaabbbabbabbbbabbaaaaaabbbbbaabbaaaabbaaaaabb
bbbbbbbabaaaaaaabbbaaababbabbbaaaaaaaaabababbbbabbabbaaaababbbbabbaabbba
bbbaaabbabbababbbbaaaabababaabaa
abaaaaabbaaaababbbaaaaababbbaaab
abaabbaaabbaaabbbbbabbaababbbbabbbbaaaaa
bababaaabbbbababbbabbaab
babbabbabaabababbabbaabbaaaababa
abbbbbbbaaabaaabaaabbbabbabbaababbbbababbabaabbabaabbaab
bbbbaabbbaaaabaababaaabaaaaabbbaabababbbbaaabaaa
abbbaabbabaaabbaabbaabbbabbabbbbbabbbbabbabbbaababbaaaba
abaabbabbaabbbaaabbbaababaaabaababbaabababababbaabbaaaaaabbabbaababbabaababababbaaaabbab
ababbbaaabaaabbaaabbbaaaaababbbaabbabbba
bbbbbabbbaabbbbbaaabaaaaaabaabaabaaabbbbaaabbbbaabbbbaba
baaaabaaabbbbbbbaababaab
aaabababbaaababababbbaab
abbbabbaaabaabaaaabaabbbbbbabaababaaabbbaaabbaaa
aaabbabbaababaaaaabaabbbbbababaaabaaaabaabbbbbbb
bababaabbaabaaaaabaabaaa
baababaabbaaabababaaaaaaabbabbbbbabbbaab
bbaabbaabbabbababaabbabbbbabbabbabbbbabaaaaabbaa
bbaabbbabbaaabbbaabbaaababbbbbbababbaaabbbbaaaaabaabaaabaaaaaababaaabbab
aaababbaabaabbbabbbaaaaaababbbaabaabbaba
ababbbbaaaabbbababbbbbaababbbababaabbbbbbaabbabbbbabaaabbaaaabbabbbaabaabbbababababbbbbb
bbbaaabbabaabbbabbabbbbb
abaabbababaabbababaabbabaaaaaabbaababaabbbabaaab
bbbabbaaabbbaababaaaabaabbaabaaaaabbbbaaaaaabaaa
aababaaaaaabbbbbabbbbaabbbaababababaaaab
bbbababbaabbaabbabbaabbbbabbabbbaababbbaaabbbbbabbbbaaba
aabbabbbbaaaaaaaabbbbabbaabaababbaaabababbbabbba
abaababbabaaaaababababba
bbaabbaabaabababbaabaabb
babbabababbbbbbabbbbbbbb
babbabababbbbabbaabbbbaa
bbbaababbaaaabaaaaaabbbb
bbabbbababbaaabbbaaaabba
abaaaaabbbabbababbbbabbb
bbabaaaaaababbaabbbbbabbaaabaabbbaababbaabaaaaababaaaaaaababbabbbbbbbabaababbaab
aababbabbabaaabbabbababbabbaabba
aaabaaabbaaabababababababbaaaababbaabaab
abbbbaabaaabbababbbababbaaabaabb
bbaaabbbbbabbbabaabbbaba
abbbbbbababbabababbbbbaabbbaabbbabbbaabb
aaaabbabbbaaababbaababaaaaaaaaababababababbbbbab
baaabbabbbabbaabbbaabababbbababbaaaabaabbbbaaabbbabbabab
abbbbbaabbbaabababbaaabbababbbabaaabbabb
baaabbbababbababbbbbaabbaaaaaabbabbabbba
bbababbbaabbbbaababbbaab
babaaaaaabbababbbabababb
bababbbbbbaabbbaaabbbbabbabaaababbaaabbbabbbbbbaabababba
babbbababbaaababbbbbbaaabaabaabbaaaaabba
aabbababbbbaaabbbabaabab
aababaaabaaababaaababbabaaabbbbabbaababb
aaaaabbbaabbaaabbbbaabbabbbbabaa
baaaabaabaaabaabaabbaaababaaaaaa
ababbbaaaabababaabbabbaababaaabaabbbbaba
bbbabbaaabaaaaabbbbbbbbb
bbababbabbaaaababbbbbbaaabaaababbaababba
abaabbabbbbbbaaaaaabbababaaaabaababbabaaaababbba
baaababaabbbbbaaabbaaabbaabbaaaaabababaa
baaaaaaaaabababaaaabaababaabbbbbaababbaababbabaa
bbbababbaababbababaababbaaabaaabaabaaaaa
baabbbbabbabbaabbaabbbaa
bbbabaaaaaabbaaaaabaaaaaaabaaabb
aababbbbbaabbaabaaabbaaabbababbbbbbabaaa
bbbbbbbabbabbaaaabbaababbaabbbbbbabaaaaabbbbbbbbbabaaaababaaaaba
abbbbbbabbbbababaaaaaaabaaabbaabbaabaaaa
bbabbbabbbbabaababbabbaabbbabaaaaaaaabba
aaabbbababaabbaababbaabbbaabaaabbbbbaaba
bababaababaabbaabbbabbbbbaabbbbabbbaaaaa
aaaaabbbbbbbaaabbaaabbbaaabbbbbbababbaba
aababbabaababbabbabaaabbbaaaabaaaaaaabbaababbbab
aabaaaababbbabaabbbbababaabaaaba
baaaaabaabbbababbbabbabaaabaaaaa
bababbbbbbbabbabbaabbbbabbabababbbbbaaaa
aaababbbaaaaabbbbbabbbabbbabababaaabaaaabbbbaaabbaaabbaabaabbbaa
abbbbbbbaabbabaaaabaabaaabbbaaaabbbaaaaababababbaabbaaabaaaaaabaaaabbbabbbbbbaaababaaabbbbbaaabb
bababbbbbabbaababbabaabbbabbaabbabbabbbb
abbbaaaabbabababbbbabbababbaabaa
baabababbbbbbaaaaaaaaaaa
bbbaabbaaaaaabbbbbaabbaababbbaab
aabaaaabaaabaaaaaababbbbbbbaaaba
abbbaababaabababbbabbabbaaaaaaabaaaaaaaabbabbbaa
abbbbaaabbabaaababababbb
abbaababbbbbaabbbabaaaab
babbaaaabbaaabbbbbbbaaabbabaabaabaaaabbb
bbbbbaababaababbaabaaaba
baaabbbabaaabbbababbbabb
aababaaabbbaababbababaabbbbbabbabaabaabb
bbbaaabbabbabbaabaabaaba
babaaabbbabbaabbbabaaabababababbabababbb
bbabbabbbabababababaabbb
baabababbabbbabbaaaabaabaabbbbba
abaababbaaababababaababbbbbaaaab
bbbababbaabbababaabaaaab
abaaabbabbbbaabbabbbbaba
baabbaaabababaabaababbababaaaabbbabbabaa
baaabaaaaaabbbaaabaababaaaaabaab
bbbbbbaabbaaabaaaabaababaabaaaabbabbaabbbaaabaaa
aabababababaaabbabaabbabbbaabbbbbbbbabbaabbbaaab
babbbbbaabaabbbabbabbabbaabaababbaaabaabbabaabaaabaaabbbabababbb
babbbbbbbbbbabaaaaabbaabbaabaaababbbabbb
bbabaabbaabaabababaabbaaabbabbaababbbabb
aababbbbaaabaaaabaaabbab
bbababbabbbbaabbbaaababb
aaaaaabbbbbaabbaabaaaaabbabaaabaaababbabababbaaabbaababb
ababaaababbbbbaaabaaabaa
bababaababaabbaabbababbaaabaabbaabababaa
baaaababbabbaabbbabbbbaabaabbaba
bbbabbabababaaaabaaaabba
bbabaabbababbaaaaababbba
baaaababaaabaaaababaaaaabababbba
bbbababbabbbabbaaaababababbaaabaabaaaaba
bbaaabaababababaaabbaaabbaabaabb
babbbbbaabbaaabbbbbaababbabbbaaaaabbaaaa
ababbaaabaaaabaaaaaabbbaabaaabbb
aaabbababbbabbaabaaaababbbaaaaabbabbaaaaaabbabbbabbabaabbaaaaaabbbbbbbbb
aaabbbabbabbaaaabbabbaaaabaabaaa
bababaabaababaaabaabbaab
bbabbbabaaabababbbbbbaaabbbbabaa
bbbaaabbbbaabaaabbbabbabababbaababbaabaa
bbbbabbabaaaaabbbbabbbbaaabaabbbabbbbaaaabbaababbbbaabbabbaaabbb
aaaabbababbbbbaaabbaabbbabbbbaaa
aaababbbabbaabbbaaabaabaaabbbbba
abaababbbaaabbbabaaaabbabbaabbaabaaaabbbbbbbaaababbaaababbbaabaabbbbabbabbbbbbbbbabbbaab
abbbbbbbabbbabbaabbabbab
abbbaabbaaabaabaaabbabbbaabbaabbbaabaaaaabbabaabababaaba
bbbbbabbbaabbabbbbbbbbbabaabbaba
abbabbaabababbbbbbbbaaba
baaaabaababbaaabbbbaaaaa
bbaabbababaaabbaabbaababbbbaabbbbababbababaabaaa
babaabbabbabbbabbbaaaaabbbbbaabababbbbab
aabbbbababbaababbabbaaaaaabbbaaababaaababaaabbbaabbabbab
babbababbaaabababbbbbaaabbabaabaaaabbaaa
aabbaaabaabbaaabaabbababbaaabbaababaabaa
aaaaaaabbbbbbaabababaabb
baaabbbbaabaaaabbbaabbabababaaba
bababaaabbbbaaababbabbaaabaababaaaabbaab
baaababaababaaaaaabbabaa
bbbabbabbabbabbbaaaaaaba
baaabaabaaaaaabbababaaaaababababbaabbbaa
abaabbaababbabbbaabaabaaaaabaabbbbbabbba
bbabbbbabaabababbbababaa
ababbaaaabaaabbabbababbababbabababbbbaababbabaabaababbbabbabbbaabaaaabbb
babbbbaabbbabbaabaaaabbbbbbbaaaaabbbbbab
aaaaaabbbababbbbbabbbaabababbbababaababb
baaabbbbaabaababababbabbabbbaaabaaaabababbbaaabaabbabababaabaabaababbbbaaabaaabbabbbbaaa
bbabbaababbababbbbaaaaababbabbbb
abbbbaabbbaabbbbabbbabbabaaababababbaabbbbbbaaaaaaaababa
aabbabbbbbabbaabaabbbaaaababaaaaabaabbbaaaabbaaabaababba
abbababaabbbabbaabbbaaab
abbababababbababaabaaabb
aaabbabaaaaaaabbaabbbbbbbabbbabb
aabbbbbaaaaabbbbabbbbaaaabbaabaaabaabbbaaaabaaaabbbbbbab
abaabbabbbaabbaababbbababbaaabaabbbbaabbbaabaabbaaaabbaaaabaaaba
aabbaabbaaaaaaabaaaabaab
abaabbaabbbababbabbbbaabaaaabbbaabbbabaaabbbbbab
baabbbbabbabbbbaaaaaaabbbabbaaaaaabaabba
baabababaaabbbbbbababaaaabbbabbaaabbbbbbabaabbbb
abaababbbbbbbaaaabbababbaabbbbbb
ababaaaaaaabbabaabbbbbbabbbabbaaaaabbbbbbababbba
abbbaabbaaaaaaababaabaaa
bbbabbabbabaaabaababbbbaaabbbbbbabaabbbb
bbabbabbbabbbbbabbbaabbaaaababbbabbaaaba
bababbbaababaabaababaabbbaaabababbbbaaaaaaaaaaaaaaabaabbabbbabbababbbbab
aababaaaaabbaabbaabaaabb
bababaabbaaaaaaaaaaaababbabaaaab
baabbbbbaabaabaaaabaabbbbbabbaabbaabaaaa
bbbaababaabbaaabbbbbabaa
aababbbbabbaaaababababbababaabbbaabbbbbaaaabbaabbabbabab
aaaaabbbbbabbaabababbbbabbabaaba
aababaaaabaaabbaaabbbaab
baabbaaabbabbaaaaababbabbaaaabaabbbabbbbaabbbbbabababbab
baaababababaabbaaaaabbaa
aababbaabbaaaababbaaabaaaabbbaab
abbababbbababbbbbabaabbb
bbbabbbbbabbbbbaaaabbbbbaabbaababaaaabbb
aabaabbbaaaaababbababbab
abaaaaabbabbaabbababaaabbaaaaababbaaaabb
bbabbaaababbaaaaabababababbbbaaaabababaabaabbaab
aaabbabaabbbaabbbaaabbbababaaaabaaabbaaa
baabababbabbababbabbbababaaaaaabaaaababa
bbabaababaaaaaabbbbaaaaabbbaaaaaabbbbaababaababa
bbaaaababaaabbbbaababaaaabbbababaaaabbbaababababbabbbbbbbabbbbbb
bbbbbababbabbabbbbbaaabbbabbabbbbabaabab
babbbbbababaabbabbbbbaaabbabbaabbbbbabababbbbbbbbababbaabaaabbab
aabbbbaabaaaabbbbbaababbbababbaabbaababb
abbababaaaaaaabbaababaaaabaaabaa
abbbbaabaababbbbaabaaaababbbaabbbaabababbbbaaaab
abbbbbbabababaababaabbbabaaabaaa
ababaaabbabaabbaaababbbbbbabaaaa
bbbbaabbaaaaabbbbaabbaba
babababaaababbabbbabbabaaabababb
ababbbbabababbbbabbabbab
abaabbabaabbaaababbaabbbbbbbbaab
ababaaabaaabaaaaaaabbaaa
ababbaaaaabbaaabbabaabab
bbbabbabbbbbaabbaaaaababbbaababbabaaabab
ababaabaababbabbbbbbabbbabbbaabaaaaaaaabbaabbbab
aabbbbabbaabbbbbaabaaaababbababaaaabbabbaabaaaaa
bbabababbabaaabaaabbabba
bbbbaaabbbbaabbbabbabbaabbbbabbbbaaabbab
aaaabbabbbbabbbbbbbbabbb
ababbbbabbabababaababaaaabaabbbaabbaaaaa
bbabbbbababbaabbbaabbabbbabbbabaaabababb
babbbbbabbbbaaabaabbabba
ababbaaabaaabaabababaabb
aaaaaabbaabbabababbbaabaababaabb
abbabababbaabbabbbaaaaaa
abbbaababababaaabbabaaaa
aaaabbbabababababaaaabaaaabaabaaaabbbabb
bbaaaaabbbbababbbaabbbbbaababbaaaaaaaabaaabbbaba
aaababbbabbaaabbbbbbabaa
bbaaabbbbabbaabbabababaa
abbababbabbbbaababbbbbbaabbbaabaaaabaabaababaaaaaaaaabba
baaaabaaabbbbbbaabaabbbb
bbaabaaaaabaababababbaabaaaabbaaabaabaab
babbbbbababaaababbaababb
aaaaababbbbababbabbbbbab
bbabbaaabbbbbaaabbabaabbabbbaabbaabbbaaa
abbbbbbabaabbabbaababbaabaaabbaa
aababaaaaabaabaabababaaabbabababbbbabbaaabbaaababbbbbbbb
baaabbbbbaabababbbbbbaaabbbbbaab
bbabbababaabbbbbbaaaaaaaabbbbaabaaaabbabbabbbababbaaabba
bbbaaabbabaababbaababbaababaaaab
abbbbbabbaabbbaababbbbaababaabbbababaabaaaaaaaab
bbbabaabaaaaababbbbbabbb
bababaaabaaaaababbaaabbaaabbabbbbbbaabaaabbababbbaabaaaabbababba
baabababbbaaabbbbbbbbbab
bababaaabaaababaabaaaaaaaaaaabbaaabbaabb
abbbaaaabbababbaabbabaaa
abaababbaabbabbbbbabbabaaabbaabbbaaaaabaabababab
bababaaabbaaabaaaaaabbbbaaababbabbabbababbbbabaaabbabbaaabbabbaaabbaaaababbbaabb
abaaaaababaababbbaaabbbabaaaaaaabbaabbbbbaabbaba
aababbbbababaaabbbabbbbb
abbbbbaaabbbaababbabaaaa
aaabbbbbaaaaabbbbbaaaaabaaabbabaaabababb
bbaabbaabbaabbaabababaaa
baaababababbababbaabbaba
bbbabbabababbbaaaaaabaaa
baabbbbbbbbbbaabbbabbbbaaabbaabbabbbababaaabbaaa
baabbaaabbabbbabbbbbbababbbbabaa
bbbbaabbabbbaaabbbabaaabaabaaaaa
babbabbbaaabaaabbaaaabababaaabbb
babbbabaaababaababaababbbabaaaabbaaababaaabbaababbaaaabbbaababbb
aabbababaabbababababbbbabaabaabb
"""
    main(txt)



def test_D():
    txt = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""
    assert main(txt) == 3

def test_DD():
    txt = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""
    assert main(txt) == 3

def test_E():
    txt = """9: "b" 27 | "a" 26
10: 23 "b" | 28 "a"
11: 9 "b" 31 | 10 "a" 31 | 9 "b" 11 31 | 10 "a" 11 31
5: "a" "b" | 15 "a"
19: "b" "a" | "b" "b"
12: 24 "b" | 19 "a"
16: 15 "a" | "b" "b"
31: "b" 17 | "a" 13
6: "b" "b" | "a" "b"
2: "a" 24 | "b" "a" "a"
0: 8 11
13: "b" 3 | "a" 12
15: "a" | "b"
17: "b" 2 | "a" 7
23: 25 "a" | 22 "b"
28: 16 "a"
20: "b" "b" | "a" 15
3: 5 "b" | 16 "a"
27: "a" 6 | "b" 18
21: "b" "a" | "a" "b"
25: "a" "a" | "a" "b"
22: "b" "b"
8: 9 "b" | 10 "a" | 9 "b" 8 | 10 "a" 8
26: "b" 22 | "a" 20
18: 15 15
7: "b" 5 | "a" 21
24: "b" "a"

bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""

    extra = """
"""

    assert main(txt) == 12

def test_F():

    txt = """60: 117 7 | 89 13
38: 7 45 | 13 32
77: 7 51 | 13 48
23: 72 13 | 27 7
61: 105 7 | 7 13
103: 7 121 | 13 112
76: 88 13 | 124 7
28: 61 13 | 27 7
24: 7 17 | 13 33
115: 128 13 | 126 7
82: 13 73 | 7 64
107: 130 13 | 1 7
49: 59 7 | 100 13
131: 86 7 | 87 13
53: 7 105 | 13 13
27: 105 105
21: 7 13 | 13 7
84: 7 26 | 13 32
62: 90 13 | 94 7
18: 93 13
65: 75 13 | 40 7
39: 13 93 | 7 95
6: 7 38 | 13 25
64: 99 7
73: 7 93 | 13 32
101: 13 81 | 7 19
116: 13 39 | 7 122
55: 13 32 | 7 53
48: 13 91 | 7 61
93: 13 13
108: 7 7 | 13 105
94: 13 91 | 7 32
118: 13 79 | 7 57
41: 7 21 | 13 32
113: 7 61 | 13 26
74: 7 53 | 13 93
52: 55 13 | 70 7
5: 108 13 | 27 7
30: 14 7 | 50 13
7: "a"
50: 13 23 | 7 111
32: 13 7 | 13 13
92: 114 13 | 125 7
89: 108 7 | 72 13
9: 7 28 | 13 127
35: 7 131 | 13 47
86: 26 13 | 108 7
67: 7 44 | 13 69
44: 7 80 | 13 22
46: 7 67 | 13 35
111: 32 7 | 72 13
11: 42 31 | 42 11 31
112: 13 91 | 7 2
99: 7 7
81: 72 7 | 26 13
123: 37 13 | 20 7
45: 7 13 | 13 13
56: 119 13 | 112 7
63: 13 61 | 7 95
57: 7 9 | 13 83
3: 13 106 | 7 43
97: 84 13 | 73 7
85: 13 93 | 7 108
117: 7 53 | 13 21
47: 16 7 | 54 13
71: 129 7 | 63 13
95: 13 13 | 7 7
37: 26 13
2: 7 13 | 13 105
72: 7 13 | 7 7
43: 85 13 | 16 7
4: 130 7 | 25 13
69: 7 22 | 13 80
68: 93 7 | 32 13
22: 45 13 | 53 7
78: 13 2 | 7 27
14: 28 13 | 119 7
17: 13 60 | 7 6
129: 91 7 | 32 13
87: 26 7
79: 58 7 | 107 13
130: 13 72 | 7 91
90: 7 45 | 13 2
8: 42 | 42 8
114: 13 30 | 7 34
66: 61 7 | 93 13
128: 7 108 | 13 72
31: 13 36 | 7 15
127: 13 108 | 7 32
110: 73 13 | 29 7
58: 7 113 | 13 48
120: 7 56 | 13 97
19: 13 53 | 7 2
83: 13 78 | 7 74
34: 7 110 | 13 4
75: 7 102 | 13 52
25: 13 72 | 7 95
16: 7 72 | 13 21
100: 13 82 | 7 116
42: 13 92 | 7 10
119: 13 2 | 7 95
88: 71 13 | 101 7
126: 13 72 | 7 61
33: 96 13 | 123 7
1: 61 7 | 53 13
96: 55 7 | 41 13
102: 7 104 | 13 87
98: 91 13 | 91 7
104: 26 13 | 32 7
51: 7 95 | 13 26
125: 13 120 | 7 3
91: 13 7
13: "b"
10: 65 7 | 46 13
105: 13 | 7
59: 13 115 | 7 77
106: 5 13 | 66 7
80: 72 13 | 53 7
20: 93 7 | 61 13
15: 118 7 | 76 13
70: 91 13 | 93 7
29: 13 26 | 7 21
122: 7 26 | 13 72
124: 12 13 | 109 7
26: 7 13
121: 91 7
36: 13 49 | 7 24
12: 68 13 | 98 7
109: 18 7 | 23 13
54: 13 108 | 7 61
0: 8 11
40: 7 103 | 13 62

abbabbaabaaaabbaabaabbbbabaaaabb
abbababaabbbbbbaababaaababaabbbb
bbabbbabbabbaaaaaaabbbbbaabaababbbababbaaabbabaa
abaabbaaabbbbabbbabbaaaabbaababb
bbaaaaabbbbbbaabbabbbabaaabaabba
bababaabbaabbbbbbbabbbaa
abbababbababbaabbababababbbbbaaababaaaaaabababaa
abbbaabbabbbabbabbabbaabaabbaaaa
abbaaaabbbbabbaaaabababb
babbaaabaababbababbbbbaaaababbaaababbbaabbbaaaba
abbbabbbabbbaaaaaabababababbbbaabaaaabbbbabbabbabaaabaaaabababba
aababbaaabbaabbbaababbbbaabbbabaaaaababb
aaaaababaababbabbbaabbbaaabaabbabbbaaaaa
baabaababababbabaabbbbbaabbabaaabbaaaabaaaababbbbabaabbb
bbaaaaabbababaaaabaaabbabbabbabbbaaabaabbabaabab
bbbbbabaaaaabbbabbaaaabb
bbbaaabbabbabbaaaababaab
bbaaabbbbbbabbababaaaaaa
abaabbabbbbbbbbabbabbbbabbaaaabaaaaababa
bbababbaabaaaaabbbaabbaabbabaabbbbbbbbbabbabbbaaabaaaabb
bbabbbbbbbabbbbbbbaaaaaa
aabbaabbbaaaaabaabbbbbaabaabbabbaabababb
bbabbabbaababbabababbbbababbbabaababbbbbabbabbbbbaababba
bababaabbabbbbaaabbabbab
bbbbaaabbbbbbabbbbbbbbbabbabbabaabbabbaaabaabaab
bbabbaabababbaaabaabaaab
abaaaaaababbabaabaabbbaa
aabaabaabaaabaabbbabbaaabbbabbbbbabaababbabbbbbb
bbabaabbbbbbbabababbbababaaababaaababbabbaabbaabbabaabab
abbbbbaababababaabbaabbbaabbababbbbaaaaa
bababbbbbbbaabbabbbbbbbaabaaabaaaabbaaba
babaaababbaaaaabbbaaaaabaaababababbabbbb
baaabbbbbabaaabbaaabaabababbabbaaaabaaaabbaabababababbaa
baabbaaababbaaabbabbaaabbbaaaabaabaaaaaa
bbbabbaabbaabbababbaaaabbbbabbbabbaabaab
aababaaaabaabbababbaaabbbaababbaabbbbaaa
baaaabaabbaabbbaaaababbbaaaaabaabbbaaaba
abbbaabababbbbbabbabbabaababbbba
babaabbabbabbaabaaababbbaabbbbababbbabbbaabbbbaabbaabaab
aabaabaaabbababaabbaabbbbaabbbaaabbabbbb
bbaabbababbaaabbabbbaaaaabaaaaabbbabbbbababaababbaaababb
baaaaaabaabaabbaabbbbabbaabbabbbaabaaaabababbaaaaaabaaab
babbaaaaaaabaaabbbaabbabababbaba
aaaabbabbbbabbaabbaabbab
aababaaababbababaabbbbabbbabaaaababbbbab
abbaaaabaaabaaaaaabaaaaa
aaabaaabaababbbbaabababb
aabbbaaabababbbbabbaaabbaabaaaabbbaababa
babaaababbabaaababbabaabbabbaaaa
bbabbabbbbbbbabbbbabaaab
bbabbbabaababbabababbaabaaabaaabaabaaaba
aaabaaababbababaabaaabbababbbbab
abbbababbbabbbabbbbaabbbababbbaaabbabbbbabbaaaaa
abbaababbbbaabbbaabbaaaa
bbabbaabbaabbbbbaabaabba
abbaabbbaabbbaaababaabbabaaabbbbbabaaaaaaabbbbbb
bbabbbbaaabbaaaabbbaaaabaaaaaaaabbbbaaaa
babaabbababbaabbabbbbabbbabbbabaabbaababbababbbbabbbaaab
babbbbaaabbbbbbbabbabbab
babababababbaababaabaaaa
bbabababbababaaaaaabaabb
aaabaaaabbbbbabbaabbaaaa
abbbabaabbabbbbaabaaaaba
aaabaaabaaaabbababababaa
bbabbaababbbababbbababaa
aaabaaabbabababaabaababbaababababaababbbabbabbbabababbaa
bbbaabbbabbbbbbbaaabaabb
abaabbaabbbbbaaaaaaaaabbbbbaaaabaaababaa
bbbabbbbaababaaabaabbaab
aababababaabbabbbbbabababbbabbba
bbbaabbbbaaaaaaaabaabbbabbaaabbbabbaabbabbbabbbababbbbab
aaaaaababbaaaaaababbaabb
bbbabbbbbbbaabbbbbaaaaabbaababbabbabaaab
abbabaabaababbababaabbbabbababbaaabbaabaaabbbbbbbbababaabaaaabbb
aabaabbaabbabbbabbaaaabbababaaba
bababaaabaabababbaabababbaaabaabbbbbbaaaabaabaabbaaaabbbabbbaaab
aababbbbbabbaabbbaabbaab
bbaabbbabaaaabaaaabbabbbbbaabbbbababaabbaabaabbaabababba
abbbaaaaabaabbabbbabaabbabaabbab
bbaaaaababaaaaabbbbaaaab
babbaaaabbaaabbbaabababbabbaabbbbbbaaaaaaaabbaaabaababbaaabaabaabbaaaaabaabaabba
babaaabaabbbabbabbbbbbbabbbbbbab
abaababbbbaaabababbaaaabbabaabbaaaabbbba
babababababaaababbbbbababbbabbabaaabbbbbaaabaaaaabbabaaa
bbaaaaabbbbaababbbabbaabbbaababa
babababaabbbbbbabbabaaaa
ababaaaaababbbaaabbbaababbababaa
aaaabbbaaabbbaaaabbbbbbabaaaaababaaababb
abbbababbbaaaaabbbbbbaaababaaaaabaaaababbaababbb
aaaababbbaaabaaabbbbaaba
bbbaabababbbabbabaaaaababbaabbbbaababbbbabbaabaaabbaabaabaaaabba
abbbbbbbbbbaaaaabaabaaaabababbababababab
babbbbbaabbbaabbabbbbbbaaabaababaaabaaaabbbaababaaaaaababbabaaba
babbabbbbbaaabbbbbbabbabbbaaaaaa
aababbaaaaaaababbbabbabaaababbaa
babbaababbbbbabaaaaaaaababaaabbabbabbbbb
bbbbbaaabbbabbababaaabbaaabbbaaaabaabaaaaaaababa
aaaaabbbbbaaaaababbbbbaabbaabbabbbbaaaaaaaababbabaaababbabaaabab
bbbababbaabaaaabbbaabbbababbaaabababbbabbbbbabbaabaaabbb
bbabbaaabaaababababaaabbbbaaaaabbbbbaabbababbbbbabaabaab
aabaababaababbaaabaaaaababaabbaaaabbbbbb
babbbababbbabaabbaaaabba
bbababbabbbababbababaaaabaaaaababaabababbbbbabbabababbba
babbbbaabaaabaabbbaaaaba
baaabaabbbbaabbbabaaabab
abbaaabbbbbabbbbbababbba
abbaaaabaaababbbabbbbbbbaababaaaaaaabaab
baaaababbbbabaabbbabbaabbbaabbabbabaabbb
abbabbaabbbaaabbaababaaabbbbbabbbabaaaaaaabaaaaa
aabbbaaabbbbbbaabbababbaabbabaabbbaaaabb
aaabaaaaaaabaaaaaabbbaab
abbabbaaaabbabababaabbaabbbbababababbbab
aaabaababbbbbbaaabbbaabaabbabaaababbbbab
abbababbbbaaabbbaabbbbba
bbababbaababaaaabbbbaaabbbabbababbbaabaa
bbabaaaabbbbaaaabbbbabaa
abaabbaababbbbbaabbbabaaababbbaaababaabb
abbabaabaababbbaaabbbabbabbbababbbbbaabb
bbbababbabbababababbbaaa
baaaabaaabbbbabababaababbabbabba
babbababbaaabaabbaaaabaaabbbaaaabbaababbabbabbabbbbabaaa
ababbbaababaabbabbabbababbbbbaaabaabbbbaaababaababababaababbbaab
aabaaaabaabbababaababbaaabababaaaaabbaaa
abbbbbbabbabbabbababbbab
babbaaaabbbbbabbbabbababaaaabbaa
bbbbbbaaaabaabbbbaaaabba
ababbbbbabbabaabbabababaaabaaababaabbbbbbbbabbaaabaaaabb
aaaabbabbaabbabbaababaaaaaabbaaa
abbabbbbbaabbaabababbaaa
abaababbaabaaaabababbbbb
baaabababbaabaaaaababaaaababaaba
aabaabababbbbbaaaabababb
aabaabaaaaabbbbbbabaaaaaabbaabbbaaaababaaabababb
bbbbbabbabbbabaaababbaaaaaabbaaaaaabbbba
bbaaaaababaabbbaabbaabbbabbbabbb
abaaaaabbabbaababbbaabbaaaaaabbaabbbbaaa
bbaabbaaabbbababbabbbaaa
abaabaaaababbbaabbbbbaaaabbbbbbaabbbbbaabbabbaaa
bbbbbbbaababaabbbabbbbbaaaababbbbbbbbabbabbabbbbaabbbbbb
bbaabbbaabaababbaaaaabba
abbaababbbaabbabbbbaabaaabbbbbabaaaabbaabaababbb
baabbbabaababbbaaababbabbabbbbaaaabbaaaabaaabbabbabbabbabaaabaaabbababbb
bbbabaabbabbbbaababbbbaaaabaaabb
bbabbaabbabbababbbbabbaaaaaaaabbaabaaaaaaabbbbba
bbbbbaabbabbaaaababbaaaaabbbbabbbbabaaba
baaababbbabaababbbbaabbbababbaab
baabbbbababaaaaaabababaa
abaabbbabbaabbbbabaabbbabbaaababbbbbabaa
bbbbbbbaabaabbbaababbbab
bbaaaaabbaabababbaaaaaaabababbbababbbbab
aabbaabbbbabbabaababbbab
babbabbaaabbbbababbbbbaabbaaabaabbbbabba
bbabbabaaabbaaabababbbbabaababbb
ababbbbabbbbbaabbbbabbbbaabbbabbbabbbbab
bbaabaaababbbabaaabbabaa
abbaaabbbbaabbbbabbababaabbbabbbaaaababa
bbbabbabbbbbababaaabbbba
aabbababbaaaababbbbababbbababaabbaaaaaaababbabaaababbbabaabbbbbb
aaabaaababaabbbabaaaababbababbaa
bbbaaabbabaabbaabababaabaaabaabb
aabbbaaaaaabbabbbbaaabbaaaababaaaabbbaaa
bbbaabbabbabbaaababbbbba
bbabababbbababaababaaaababaaaaabaaabbbbbbabbbabbabbabbab
aabaababbbbbbbbabbabbabaaababaaabaaaaababaaaaabbbaabbaba
aaababbbabbabaaaabaabaabbbbbbbbbaaaaabababaaaabaaabbbbbaabbbbbabbabaaaaa
baaaabaababbaaabbabaaabbabbaabba
abbbbabbbbbbbabbbaabbbab
bbbbbabbbbbbbabbbaabbbbbbbbbbbbabaabbabaaaaaaaaa
bbabaabbaabbbbabbabbaabaabaaaaab
bbabaabbbbbbbababbbbbbbb
bbabbaaababbabbaaaabaababbabababbaaabaabaabaabbabbaaaaababbbabaaabbbabbbabbaabaa
abbbabbabbbbbabaaaabababaabababaaabaababbaabbbbbbaaabaaa
baaaabaabbbaaabbabbaaaab
bababbaabbbabaaaabbaabaabaaabbbbabaaaaabbbaaabbb
bbbabaabbbaaabaabbabababaabbabababbaaaaabbbbabbabaabbaba
abaaaabbbabbbabaaababbababbbbaabbaabbbbbbbbabbba
bbabbabaabbbbbbaabaaabbabaabbbbbbbaababaaabaabbaababbabb
baaabbbbbabaaabaaaaaababbaaabbbabaabbababaaabaaabaabbaab
abbbbbaabbbbbbbaaabbbbabaabaabba
aaabbbabbabbbabaaaaabaab
bbababbabaabbabbbbaaaababbbbbabbababbaba
bbabababaabaabaaaabaabaaaababbbabbabaaaa
bbaaaabbbabbabbbbabbaaaaaabbbbbaabbaaaabbaaaaabb
bbbbbbbabaaaaaaabbbaaababbabbbaaaaaaaaabababbbbabbabbaaaababbbbabbaabbba
bbbaaabbabbababbbbaaaabababaabaa
abaaaaabbaaaababbbaaaaababbbaaab
abaabbaaabbaaabbbbbabbaababbbbabbbbaaaaa
bababaaabbbbababbbabbaab
babbabbabaabababbabbaabbaaaababa
abbbbbbbaaabaaabaaabbbabbabbaababbbbababbabaabbabaabbaab
bbbbaabbbaaaabaababaaabaaaaabbbaabababbbbaaabaaa
abbbaabbabaaabbaabbaabbbabbabbbbbabbbbabbabbbaababbaaaba
abaabbabbaabbbaaabbbaababaaabaababbaabababababbaabbaaaaaabbabbaababbabaababababbaaaabbab
ababbbaaabaaabbaaabbbaaaaababbbaabbabbba
bbbbbabbbaabbbbbaaabaaaaaabaabaabaaabbbbaaabbbbaabbbbaba
baaaabaaabbbbbbbaababaab
aaabababbaaababababbbaab
abbbabbaaabaabaaaabaabbbbbbabaababaaabbbaaabbaaa
aaabbabbaababaaaaabaabbbbbababaaabaaaabaabbbbbbb
bababaabbaabaaaaabaabaaa
baababaabbaaabababaaaaaaabbabbbbbabbbaab
bbaabbaabbabbababaabbabbbbabbabbabbbbabaaaaabbaa
bbaabbbabbaaabbbaabbaaababbbbbbababbaaabbbbaaaaabaabaaabaaaaaababaaabbab
aaababbaabaabbbabbbaaaaaababbbaabaabbaba
ababbbbaaaabbbababbbbbaababbbababaabbbbbbaabbabbbbabaaabbaaaabbabbbaabaabbbababababbbbbb
bbbaaabbabaabbbabbabbbbb
abaabbababaabbababaabbabaaaaaabbaababaabbbabaaab
bbbabbaaabbbaababaaaabaabbaabaaaaabbbbaaaaaabaaa
aababaaaaaabbbbbabbbbaabbbaababababaaaab
bbbababbaabbaabbabbaabbbbabbabbbaababbbaaabbbbbabbbbaaba
aabbabbbbaaaaaaaabbbbabbaabaababbaaabababbbabbba
abaababbabaaaaababababba
bbaabbaabaabababbaabaabb
babbabababbbbbbabbbbbbbb
babbabababbbbabbaabbbbaa
bbbaababbaaaabaaaaaabbbb
bbabbbababbaaabbbaaaabba
abaaaaabbbabbababbbbabbb
bbabaaaaaababbaabbbbbabbaaabaabbbaababbaabaaaaababaaaaaaababbabbbbbbbabaababbaab
aababbabbabaaabbabbababbabbaabba
aaabaaabbaaabababababababbaaaababbaabaab
abbbbaabaaabbababbbababbaaabaabb
bbaaabbbbbabbbabaabbbaba
abbbbbbababbabababbbbbaabbbaabbbabbbaabb
aaaabbabbbaaababbaababaaaaaaaaababababababbbbbab
baaabbabbbabbaabbbaabababbbababbaaaabaabbbbaaabbbabbabab
abbbbbaabbbaabababbaaabbababbbabaaabbabb
baaabbbababbababbbbbaabbaaaaaabbabbabbba
bbababbbaabbbbaababbbaab
babaaaaaabbababbbabababb
bababbbbbbaabbbaaabbbbabbabaaababbaaabbbabbbbbbaabababba
babbbababbaaababbbbbbaaabaabaabbaaaaabba
aabbababbbbaaabbbabaabab
aababaaabaaababaaababbabaaabbbbabbaababb
aaaaabbbaabbaaabbbbaabbabbbbabaa
baaaabaabaaabaabaabbaaababaaaaaa
ababbbaaaabababaabbabbaababaaabaabbbbaba
bbbabbaaabaaaaabbbbbbbbb
bbababbabbaaaababbbbbbaaabaaababbaababba
abaabbabbbbbbaaaaaabbababaaaabaababbabaaaababbba
baaababaabbbbbaaabbaaabbaabbaaaaabababaa
baaaaaaaaabababaaaabaababaabbbbbaababbaababbabaa
bbbababbaababbababaababbaaabaaabaabaaaaa
baabbbbabbabbaabbaabbbaa
bbbabaaaaaabbaaaaabaaaaaaabaaabb
aababbbbbaabbaabaaabbaaabbababbbbbbabaaa
bbbbbbbabbabbaaaabbaababbaabbbbbbabaaaaabbbbbbbbbabaaaababaaaaba
abbbbbbabbbbababaaaaaaabaaabbaabbaabaaaa
bbabbbabbbbabaababbabbaabbbabaaaaaaaabba
aaabbbababaabbaababbaabbbaabaaabbbbbaaba
bababaababaabbaabbbabbbbbaabbbbabbbaaaaa
aaaaabbbbbbbaaabbaaabbbaaabbbbbbababbaba
aababbabaababbabbabaaabbbaaaabaaaaaaabbaababbbab
aabaaaababbbabaabbbbababaabaaaba
baaaaabaabbbababbbabbabaaabaaaaa
bababbbbbbbabbabbaabbbbabbabababbbbbaaaa
aaababbbaaaaabbbbbabbbabbbabababaaabaaaabbbbaaabbaaabbaabaabbbaa
abbbbbbbaabbabaaaabaabaaabbbaaaabbbaaaaababababbaabbaaabaaaaaabaaaabbbabbbbbbaaababaaabbbbbaaabb
bababbbbbabbaababbabaabbbabbaabbabbabbbb
abbbaaaabbabababbbbabbababbaabaa
baabababbbbbbaaaaaaaaaaa
bbbaabbaaaaaabbbbbaabbaababbbaab
aabaaaabaaabaaaaaababbbbbbbaaaba
abbbaababaabababbbabbabbaaaaaaabaaaaaaaabbabbbaa
abbbbaaabbabaaababababbb
abbaababbbbbaabbbabaaaab
babbaaaabbaaabbbbbbbaaabbabaabaabaaaabbb
bbbbbaababaababbaabaaaba
baaabbbabaaabbbababbbabb
aababaaabbbaababbababaabbbbbabbabaabaabb
bbbaaabbabbabbaabaabaaba
babaaabbbabbaabbbabaaabababababbabababbb
bbabbabbbabababababaabbb
baabababbabbbabbaaaabaabaabbbbba
abaababbaaababababaababbbbbaaaab
bbbababbaabbababaabaaaab
abaaabbabbbbaabbabbbbaba
baabbaaabababaabaababbababaaaabbbabbabaa
baaabaaaaaabbbaaabaababaaaaabaab
bbbbbbaabbaaabaaaabaababaabaaaabbabbaabbbaaabaaa
aabababababaaabbabaabbabbbaabbbbbbbbabbaabbbaaab
babbbbbaabaabbbabbabbabbaabaababbaaabaabbabaabaaabaaabbbabababbb
babbbbbbbbbbabaaaaabbaabbaabaaababbbabbb
bbabaabbaabaabababaabbaaabbabbaababbbabb
aababbbbaaabaaaabaaabbab
bbababbabbbbaabbbaaababb
aaaaaabbbbbaabbaabaaaaabbabaaabaaababbabababbaaabbaababb
ababaaababbbbbaaabaaabaa
bababaababaabbaabbababbaaabaabbaabababaa
baaaababbabbaabbbabbbbaabaabbaba
bbbabbabababaaaabaaaabba
bbabaabbababbaaaaababbba
baaaababaaabaaaababaaaaabababbba
bbbababbabbbabbaaaababababbaaabaabaaaaba
bbaaabaababababaaabbaaabbaabaabb
babbbbbaabbaaabbbbbaababbabbbaaaaabbaaaa
ababbaaabaaaabaaaaaabbbaabaaabbb
aaabbababbbabbaabaaaababbbaaaaabbabbaaaaaabbabbbabbabaabbaaaaaabbbbbbbbb
aaabbbabbabbaaaabbabbaaaabaabaaa
bababaabaababaaabaabbaab
bbabbbabaaabababbbbbbaaabbbbabaa
bbbaaabbbbaabaaabbbabbabababbaababbaabaa
bbbbabbabaaaaabbbbabbbbaaabaabbbabbbbaaaabbaababbbbaabbabbaaabbb
aaaabbababbbbbaaabbaabbbabbbbaaa
aaababbbabbaabbbaaabaabaaabbbbba
abaababbbaaabbbabaaaabbabbaabbaabaaaabbbbbbbaaababbaaababbbaabaabbbbabbabbbbbbbbbabbbaab
abbbbbbbabbbabbaabbabbab
abbbaabbaaabaabaaabbabbbaabbaabbbaabaaaaabbabaabababaaba
bbbbbabbbaabbabbbbbbbbbabaabbaba
abbabbaabababbbbbbbbaaba
baaaabaababbaaabbbbaaaaa
bbaabbababaaabbaabbaababbbbaabbbbababbababaabaaa
babaabbabbabbbabbbaaaaabbbbbaabababbbbab
aabbbbababbaababbabbaaaaaabbbaaababaaababaaabbbaabbabbab
babbababbaaabababbbbbaaabbabaabaaaabbaaa
aabbaaabaabbaaabaabbababbaaabbaababaabaa
aaaaaaabbbbbbaabababaabb
baaabbbbaabaaaabbbaabbabababaaba
bababaaabbbbaaababbabbaaabaababaaaabbaab
baaababaababaaaaaabbabaa
bbbabbabbabbabbbaaaaaaba
baaabaabaaaaaabbababaaaaababababbaabbbaa
abaabbaababbabbbaabaabaaaaabaabbbbbabbba
bbabbbbabaabababbbababaa
ababbaaaabaaabbabbababbababbabababbbbaababbabaabaababbbabbabbbaabaaaabbb
babbbbaabbbabbaabaaaabbbbbbbaaaaabbbbbab
aaaaaabbbababbbbbabbbaabababbbababaababb
baaabbbbaabaababababbabbabbbaaabaaaabababbbaaabaabbabababaabaabaababbbbaaabaaabbabbbbaaa
bbabbaababbababbbbaaaaababbabbbb
abbbbaabbbaabbbbabbbabbabaaababababbaabbbbbbaaaaaaaababa
aabbabbbbbabbaabaabbbaaaababaaaaabaabbbaaaabbaaabaababba
abbababaabbbabbaabbbaaab
abbababababbababaabaaabb
aaabbabaaaaaaabbaabbbbbbbabbbabb
aabbbbbaaaaabbbbabbbbaaaabbaabaaabaabbbaaaabaaaabbbbbbab
abaabbabbbaabbaababbbababbaaabaabbbbaabbbaabaabbaaaabbaaaabaaaba
aabbaabbaaaaaaabaaaabaab
abaabbaabbbababbabbbbaabaaaabbbaabbbabaaabbbbbab
baabbbbabbabbbbaaaaaaabbbabbaaaaaabaabba
baabababaaabbbbbbababaaaabbbabbaaabbbbbbabaabbbb
abaababbbbbbbaaaabbababbaabbbbbb
ababaaaaaaabbabaabbbbbbabbbabbaaaaabbbbbbababbba
abbbaabbaaaaaaababaabaaa
bbbabbabbabaaabaababbbbaaabbbbbbabaabbbb
bbabbabbbabbbbbabbbaabbaaaababbbabbaaaba
bababbbaababaabaababaabbbaaabababbbbaaaaaaaaaaaaaaabaabbabbbabbababbbbab
aababaaaaabbaabbaabaaabb
bababaabbaaaaaaaaaaaababbabaaaab
baabbbbbaabaabaaaabaabbbbbabbaabbaabaaaa
bbbaababaabbaaabbbbbabaa
aababbbbabbaaaababababbababaabbbaabbbbbaaaabbaabbabbabab
aaaaabbbbbabbaabababbbbabbabaaba
aababaaaabaaabbaaabbbaab
baabbaaabbabbaaaaababbabbaaaabaabbbabbbbaabbbbbabababbab
baaababababaabbaaaaabbaa
aababbaabbaaaababbaaabaaaabbbaab
abbababbbababbbbbabaabbb
bbbabbbbbabbbbbaaaabbbbbaabbaababaaaabbb
aabaabbbaaaaababbababbab
abaaaaabbabbaabbababaaabbaaaaababbaaaabb
bbabbaaababbaaaaabababababbbbaaaabababaabaabbaab
aaabbabaabbbaabbbaaabbbababaaaabaaabbaaa
baabababbabbababbabbbababaaaaaabaaaababa
bbabaababaaaaaabbbbaaaaabbbaaaaaabbbbaababaababa
bbaaaababaaabbbbaababaaaabbbababaaaabbbaababababbabbbbbbbabbbbbb
bbbbbababbabbabbbbbaaabbbabbabbbbabaabab
babbbbbababaabbabbbbbaaabbabbaabbbbbabababbbbbbbbababbaabaaabbab
aabbbbaabaaaabbbbbaababbbababbaabbaababb
abbababaaaaaaabbaababaaaabaaabaa
abbbbaabaababbbbaabaaaababbbaabbbaabababbbbaaaab
abbbbbbabababaababaabbbabaaabaaa
ababaaabbabaabbaaababbbbbbabaaaa
bbbbaabbaaaaabbbbaabbaba
babababaaababbabbbabbabaaabababb
ababbbbabababbbbabbabbab
abaabbabaabbaaababbaabbbbbbbbaab
ababaaabaaabaaaaaaabbaaa
ababbaaaaabbaaabbabaabab
bbbabbabbbbbaabbaaaaababbbaababbabaaabab
ababaabaababbabbbbbbabbbabbbaabaaaaaaaabbaabbbab
aabbbbabbaabbbbbaabaaaababbababaaaabbabbaabaaaaa
bbabababbabaaabaaabbabba
bbbbaaabbbbaabbbabbabbaabbbbabbbbaaabbab
aaaabbabbbbabbbbbbbbabbb
ababbbbabbabababaababaaaabaabbbaabbaaaaa
bbabbbbababbaabbbaabbabbbabbbabaaabababb
babbbbbabbbbaaabaabbabba
ababbaaabaaabaabababaabb
aaaaaabbaabbabababbbaabaababaabb
abbabababbaabbabbbaaaaaa
abbbaababababaaabbabaaaa
aaaabbbabababababaaaabaaaabaabaaaabbbabb
bbaaaaabbbbababbbaabbbbbaababbaaaaaaaabaaabbbaba
aaababbbabbaaabbbbbbabaa
bbaaabbbbabbaabbabababaa
abbababbabbbbaababbbbbbaabbbaabaaaabaabaababaaaaaaaaabba
baaaabaaabbbbbbaabaabbbb
bbaabaaaaabaababababbaabaaaabbaaabaabaab
babbbbbababaaababbaababb
aaaaababbbbababbabbbbbab
bbabbaaabbbbbaaabbabaabbabbbaabbaabbbaaa
abbbbbbabaabbabbaababbaabaaabbaa
aababaaaaabaabaabababaaabbabababbbbabbaaabbaaababbbbbbbb
baaabbbbbaabababbbbbbaaabbbbbaab
bbabbababaabbbbbbaaaaaaaabbbbaabaaaabbabbabbbababbaaabba
bbbaaabbabaababbaababbaababaaaab
abbbbbabbaabbbaababbbbaababaabbbababaabaaaaaaaab
bbbabaabaaaaababbbbbabbb
bababaaabaaaaababbaaabbaaabbabbbbbbaabaaabbababbbaabaaaabbababba
baabababbbaaabbbbbbbbbab
bababaaabaaababaabaaaaaaaaaaabbaaabbaabb
abbbaaaabbababbaabbabaaa
abaababbaabbabbbbbabbabaaabbaabbbaaaaabaabababab
bababaaabbaaabaaaaaabbbbaaababbabbabbababbbbabaaabbabbaaabbabbaaabbaaaababbbaabb
abaaaaababaababbbaaabbbabaaaaaaabbaabbbbbaabbaba
aababbbbababaaabbbabbbbb
abbbbbaaabbbaababbabaaaa
aaabbbbbaaaaabbbbbaaaaabaaabbabaaabababb
bbaabbaabbaabbaabababaaa
baaababababbababbaabbaba
bbbabbabababbbaaaaaabaaa
baabbbbbbbbbbaabbbabbbbaaabbaabbabbbababaaabbaaa
baabbaaabbabbbabbbbbbababbbbabaa
bbbbaabbabbbaaabbbabaaabaabaaaaa
babbabbbaaabaaabbaaaabababaaabbb
babbbabaaababaababaababbbabaaaabbaaababaaabbaababbaaaabbbaababbb
aabbababaabbababababbbbabaabaabb
"""
    main(txt)
