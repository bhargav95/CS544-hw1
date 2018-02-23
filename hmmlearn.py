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

    ends = dict()

    tagcounter = dict()

    starttag = "START"

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

            # add to counters

            if t in tagcounter:
                tagcounter[t] += 1
            else:
                tagcounter[t] = 1

            if w in ep:
                if t in ep[w]:
                    ep[w][t] += 1
                else:
                    ep[w][t] = 1
            else:
                ep[w] = dict()
                ep[w][t] = 1

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

        if j[0] in ends:
            ends[j[0]] += 1
        else:
            ends[j[0]] = 1.0

    tagcounter["START"] = line

    print "Tag Set :", len(tags)
    print "Word Set:", len(words)

    c = 0
    for i in tp:
        for j in tp[i]:
            c += tp[i][j]

    print "Total transition count:", c

    c = 0

    for tag1 in tp:
        for tag2 in tp[tag1]:
            tp[tag1][tag2] /= float(tagcounter[tag1])

    for word in ep:
        for tag in ep[word]:
            ep[word][tag] /= float(tagcounter[tag])

    for i in ends:
        ends[i] /= line

    for i in ep:
        for j in ep[i]:
            c += ep[i][j]

    print "Word Count: ", c
    print "Sentence Count: ", line

    stag = sum(tagcounter.values())
    for i in tagcounter:
        tagcounter[i] /= float(stag)

    data = {"emission_prob": ep, "transition_prob": tp, "end_tag": ends, "tag_prob": tagcounter}

    with open('hmmmodel.txt', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, separators=(',', ':'), indent=0)
