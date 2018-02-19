import re
import sys
import json

def gettok(x):
    k = x.rfind('/')
    return [x[:k], x[k + 1:]]



with open(sys.argv[1]) as f:
    words = set()
    tags = set()

    ep = dict()
    tp = dict()

    starttag = "START"
    endtag = "END"

    pairs = []
    i = f.readline().rstrip()
    line = 0
    while i:
        line += 1

        pairs = re.split(r' ', i)

        i = f.readline().rstrip()

        # for i in pairs:
        #     print re.split(r'/',i)

        allpairs = map(gettok, pairs)

        # print allpairs

        prevtag = starttag
        for j in allpairs:
            # j[0] is word
            # j[1] is tag

            w = j[0]
            t = j[1]

            if t in ep:
                if w in ep[t]:
                    ep[t][w] += 1
                else:
                    ep[t][w] = 1
            else:
                ep[t] = dict()
                ep[t][w] = 1

            if prevtag in tp:
                if t in tp[prevtag]:
                    tp[prevtag][t] += 1
                else:
                    tp[prevtag][t] = 1
            else:
                tp[prevtag] = dict()
                tp[prevtag][t] = 1

            words.add(w)
            tags.add(t)

            prevtag = t

        if prevtag in tp:
            if endtag in tp[prevtag]:
                tp[prevtag][endtag] += 1
            else:
                tp[prevtag][endtag] = 1
        else:
            tp[prevtag] = dict()
            tp[prevtag][endtag] = 1

    print "Tag Set :", len(tags)
    print "Word Set:", len(words)

    c = 0
    for i in tp:
        for j in tp[i]:
            c += tp[i][j]

    print "Total transition count:", c

    c = 0

    for i in ep:
        for j in ep[i]:
            c += ep[i][j]

    print "Word Count: ", c
    print "Sentence Count: ", line

    data = {"emission_prob": ep, "transition_prob": tp}

    with open('hmmmodel.txt', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True,separators=(',', ':'))
