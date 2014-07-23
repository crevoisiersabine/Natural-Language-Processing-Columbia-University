__author__ = 'frasercampbell'

import json
import pprint


def read_json(file):
    trees = []
    with open(file, 'r') as input_data:
        for lines in input_data:
            trees.append(json.loads(lines))
    return trees


def readfile(file): #This reads in the count file to identify _RARE_ words
    l = open(file, "r")
    words = []
    non_terminal = []
    for line in l:
        if "UNARYRULE" in line:
            if int(line.split(" ")[0]) < 5:
                words.append(line.split(" ")[3].strip("\n"))
                non_terminal.append(line.split(" ")[2])
    return words, non_terminal
    # pprint.pprint(words)
    # pprint.pprint(non_terminal)


def wrapper_search(words, non_terminal):
    trees = read_json("parse_train.dat")
    l = open("test.txt", "w")
    for tree in trees:
        # print trees
        for i in range(len(words)): #This searches for all words which are rare
            # print i
            search(tree, words[i], non_terminal[i])
        l.write(str(tree) + "\n")
        # pprint.pprint(tree)


def search(tree, key, NT): #This searches the JSON tree struct for the rare words array
    if not (any(isinstance(el, list) for el in tree)) and type(tree) == list:  #base case when reach end of tree and want to check for rare word
        tree[0] = tree[0].encode('ascii', 'ignore')
        tree[1] = tree[1].encode('ascii', 'ignore')
        if tree[1] == key and tree[0] == NT:
            print "I'm here !"
            tree[1] = "_RARE_"
        return True
    elif type(tree) == str:  #base case for start of tree
        return False
    else:
        tree[0] = tree[0].encode('ascii', 'ignore')
        for elements in tree:
            search(elements, key, NT)


words, non_terminal = readfile("cfg.counts")
wrapper_search(words, non_terminal)