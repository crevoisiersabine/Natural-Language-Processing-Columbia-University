__author__ = 'Sabine'


def readfile(file):
    return open(file, "r")


#Following function adds type RARE to rare words in new file file_write
def replacewords(n, file_count, file_raw, file_write): #n is the number of counts beneath which a word in considered infrequent
    l = readfile(file_count)
    repo = {}
    for line in l:
        segment = line.split(" ")
        if(int(segment[0]) < n) and "WORDTAG" in line:
            for chars in segment[3]:
                if(chars.isdigit()):
                    if segment[3].strip("\n") not in repo:
                        repo[segment[3].strip("\n")] = "Numeric"
            if segment[3].strip("\n").isupper():
                if segment[3].strip("\n") not in repo:
                    repo[segment[3].strip("\n")] = "All Capitals"
            elif segment[3].strip("\n")[len(segment[3].strip("\n")) - 1].isupper():
                if segment[3].strip("\n") not in repo:
                    repo[segment[3].strip("\n")] = "Last Capital"
            else:
                if segment[3].strip("\n") not in repo:
                    repo[segment[3].strip("\n")] = "_RARE_"

    raw_l = readfile(file_raw)
    newfile = open(file_write, "w")
    for row in raw_l:
        pieces = row.split(" ")
        if pieces[0] in repo:
            pieces[0] = repo[pieces[0]]
        newfile.write(" ".join(pieces))

replacewords(5, "gene.counts", "gene.train", "gene_rare_improved.train")