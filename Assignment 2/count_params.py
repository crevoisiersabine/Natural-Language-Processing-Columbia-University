__author__ = 'Sabine & Fraser'

import pprint

# N as the list of non-terminals as a simple array
# set_of_rules as an array of tuples
def grammar_rules(file):
    set_of_rules = []
    Nonterminals = []
    NT = []
    Unary_rules = []
    l = open(file, "r")
    for lines in l:
        segments = lines.split(" ")
        if "BINARYRULE" in lines:
            set_of_rules.append(((segments[2], segments[3], segments[4].strip('\n')), segments[0]))
        if "NONTERMINAL" in lines:
            Nonterminals.append((segments[2].strip('\n'), segments[0]))
            NT.append(segments[2].strip('\n'))
        if "UNARYRULE" in lines:
            Unary_rules.append(((segments[2], segments[3].strip('\n')), segments[0]))
    return set_of_rules, Nonterminals, Unary_rules, NT


#Creating some data structures
set_of_rules, N, unary_rules, NT = grammar_rules("parse_train.counts.out")

#Create dictionaries
unary_rules_dict = dict(unary_rules)
N_dict = dict(N)
set_of_rules_dict = dict(set_of_rules)

# sentences as a nested array of sentences each a simple array of words
def read_sentences(file):
    sentences = []
    l = open(file, "r")
    for line in l:
        sentence = []
        sentences.append(sentence)
        words = line.split(" ")
        for word in words:
            sentence.append(word)
    return sentences

# unary_rule_exists is a method that takes a word and a non terminal and returns a boolean depending on whether rule exists
def unary_rule_exists(word, non_terminal, unary_rules_dict):
    if (non_terminal, word) in unary_rules_dict:
        return True
    return False

# q_1 evaluates the unary count for non terminal going to a given word
def q_1(X, Y):
    return float(unary_rules_dict[(X, Y)]) / float(N_dict[X])

# q_2 evaluates the binary count for X going to Y, Z
def q_2(X, Y, Z):
    return float(set_of_rules_dict[(X, Y, Z)])/float(N_dict[X])


def backtrace(back, bp):
    "Extract the tree from the backpointers."
    if not back: return None
    if len(back) == 6:
        (X, Y, Z, i, s, j) = back
        return [X, backtrace(bp[i, s, Y], bp),
                backtrace(bp[s + 1, j, Z], bp)]
    else:
        (X, Y, i, i) = back
        return [X, Y]


def argmax(ls):
    "Compute the argmax of a list (item, score) pairs."
    if not ls: return None, 0.0
    return max(ls, key = lambda x: x[1])


#NB: This creates the rule for the bottom layer of the tree
def PCFG(N, set_of_rules_dict, sentence):
    pi = {}
    bp = {}
    #Initialisation
    for i in range(1, len(sentence) + 1):
        for X in N:
            if(unary_rule_exists(sentence[i-1], X, unary_rules_dict)): #s[i] is the word at position i of sentence s & unary_rules is array of all unary_rules
                pi[i, i, X] = q_1(X, sentence[i-1])
                bp[i, i, X] = (X, sentence[i-1], i, i)

    #Algorithm
    for l in range(1, len(sentence)):
        for i in range(1, len(sentence) - l + 1):
            j= i + l
            for X_all in N:
                score_array = []
                bs_dict = {}

                #Evaluating the highest probability configuration
                for (X, Y, Z) in set_of_rules_dict:
                    for s in range(i, j):
                        if (X == X_all):
                            if ((i, s, Y) in pi and (s + 1, j, Z) in pi):
                                result = q_2(X_all, Y, Z) * pi[i, s, Y] * pi[s + 1, j, Z]
                                score_array.append(result)
                                bs_dict[result] = (X_all, Y, Z, i, s, j)

                if(len(score_array) != 0):
                    maximum_score = max(score_array)
                    pi[i, j, X_all] = maximum_score
                    bp[i, j, X_all] = bs_dict[maximum_score]

    # Return the tree rooted in SBARQ
    if (1, len(sentence), "SBARQ") in pi:
        tree = backtrace(bp[1, len(sentence), "SBARQ"], bp)
        return tree


def run():
    #TEST
    test_sentence = ["What", "was", "the", "_RARE_", "_RARE_", "of", "the", "_RARE_", "_RARE_", "_RARE_", "in", "_RARE_", "?"]
    print PCFG(NT, set_of_rules_dict, test_sentence)

run()