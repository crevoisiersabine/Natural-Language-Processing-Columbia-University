__author__ = 'Sabine'

import pprint

def emission(word, tag, file):
    l = readfile(file)
    counter = 0
    counter2 = 0
    for line in l:
        if tag in line and word in line:
            counter += float(line.split(" ")[0])
        if (" " + tag + " ") in line and "WORDTAG" in line:
            counter2 += float(line.split(" ")[0])
    return counter / counter2


def readfile(file):
    return open(file, "r")


def functionQ(y_i, y_i2, y_i1):
    count = readfile("gene_rare.counts")
    numerator = 0
    denominator = 0
    for line in count:
        if "3-GRAM" in line:
            segment = line.split(" ")
            if y_i2 in segment[2] and y_i1 in segment[3] and y_i in segment[4]:
                numerator = float(segment[0])
        if "2-GRAM" in line:
            divide = line.split(" ")
            if y_i2 in divide[2] and y_i1 in divide[3]:
                denominator = float(divide[0])
    return numerator/denominator


def functionViterbi(file):
    l = readfile(file) #This creates an array of arrays where the length is the number of sentences
    sentences = []
    bp_array = []
    for line in l:
        line = line.strip("\n")
        if(line == ""):
            sentences.append([])
            bp_array.append([])

    l = readfile(file)
    count = 0  #This populates the above array of arrays with the words in each centre
    for again in l:
        again = again.strip("\n")
        if(again != ""):
            sentences[count].append(again)
        else:
            count += 1

    index = 0
    for sentence in sentences: #Loop through the sentences in the document
        viterbi(len(sentence), sentence, bp_array[index])
        index += 1

    pprint.pprint(bp_array)


def viterbi(k, word_array, empty_array):
    if k==1:
        a = functionQ("O", "*", "*") * emission(word_array[k-1], "O", "gene_rare.counts")
        b = functionQ("I-GENE", "*", "*") * emission(word_array[k-1], "I-GENE", "gene_rare.counts")
        if a > b:
            empty_array.append("*")
            empty_array.append("*")
            empty_array.append("O")
            return a
        else:
            empty_array.append("*")
            empty_array.append("*")
            empty_array.append("I-GENE")
            return b
    else:
        viter = viterbi(k-1, word_array, empty_array)
        a = viter * functionQ("O", empty_array[len(empty_array)-2], empty_array[len(empty_array)-1])*emission(word_array[k-1], "O", "gene_rare.counts")
        b = viter * functionQ("I-GENE", empty_array[len(empty_array)-2], empty_array[len(empty_array)-1])*emission(word_array[k-1], "I-GENE", "gene_rare.counts")
        if a > b:
            empty_array.append("O")
            return a
        else:
            empty_array.append("I-GENE")
            return b


# array = []
# word_array = ["the", "gene", "is", "deuterium"]
# print viterbi(4, word_array, array)
# print array

functionViterbi("gene.dev")

# functionQ("I-GENE","*", "*")