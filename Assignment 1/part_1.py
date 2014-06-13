__author__ = 'Fraser with the help of Sabine'


def readfile(file):
    return open(file, "r")


def emission(word, tag, file, numy):
    l = readfile(file)
    counter = 0
    for line in l:
        if tag in line and word in line:
            counter += float(line.split(" ")[0])
    return counter / numy


def count(tag, file):
    l = readfile(file)
    counter = 0
    for line in l:
        if (" " + tag + " ") in line and "WORDTAG" in line:
            counter += float(line.split(" ")[0])
    return counter


#Following function adds type RARE to rare words in new file file_write
def replacewords(n, file_count, file_raw, file_write): #n is the number of counts beneath which a word in considered infrequent
    l = readfile(file_count)
    repo = {}
    for line in l:
        segment = line.split(" ")
        if(int(segment[0]) < n) and "WORDTAG" in line:
            if segment[3] not in repo:
                repo[segment[3].strip("\n")] = segment[0] #We have written to a dictionary containing key rare word, value occurrence

    raw_l = readfile(file_raw)
    newfile = open(file_write, "w")
    for row in raw_l:
        pieces = row.split(" ")
        if pieces[0] in repo:
            pieces[0] = "_RARE_"
        newfile.write(" ".join(pieces))


def simpletagger(filetag, filedev, fileout):
    O = count("O", filetag)
    IGENE = count("I-GENE", filetag)
    countfile = readfile(filetag)
    repo = {}

    for row in countfile:
        segmentation = row.split(" ")
        if "1-GRAM" in row and "O" in row:
            countO = float(segmentation[0])
        if "1-GRAM" in row and "I-GENE" in row:
            countIGENE = float(segmentation[0])
        if "WORDTAG" in row:
            segment = row.split(" ")
            amount = segment[0]
            tag = segment[2]
            word = segment[3].strip("\n")
            if word not in repo:
                repo[word] = {}
            if tag not in repo[word]:
                repo[word][tag] = amount


    #This code finds the emission factor for RARE
    if emission("_RARE_", "O", filetag, countO) < emission("_RARE_", "I-GENE", filetag, countIGENE):
        max_tag_rare = "I-GENE"
    else:
        max_tag_rare = "O"

    newfile = open(fileout, "w")
    l = readfile(filedev)
    for line in l:
        if line.strip("\n") not in repo:
            newfile.write("".join(["_RARE_ ", max_tag_rare, "\n"]))
        else:
            newfile.write("".join([line.strip("\n") + " ", maxemission(line.strip("\n"), repo, filetag, countO, countIGENE), "\n"]))


def maxemission(word, repo, filetag, countO, countIGENE):
    if len(repo[word].keys()) == 1:
        return repo[word].keys()[0]
    else:
        if emission(word, "O", filetag, countO) < emission(word, "I-GENE", filetag, countIGENE):
            return "I-GENE"
        else:
            return "O"

def run():
    replacewords(5, "gene.counts", "gene.train", "gene_rare.train")
    simpletagger("gene_rare.counts", "gene.test", "gene_test.p1.out")

run()
