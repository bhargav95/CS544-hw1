import json
from math import log
from time import time
import sys

smooth = -8


def gettok(x):
    k = x.rfind('/')
    return [x[:k], x[k + 1:]]


def doTheViterbi(sentence, tags, x):
    words = sentence.split(" ")

    viterbi = dict()
    backtrace = list()

    # initial prob
    backtrace.append(dict())

    tp = x["transition_prob"]["START"]
    tag = x["tag_prob"]
    # tp_sum = sum(tp.values())

    w = words[0]

    ep = x["emission_prob"]

    if w in ep:
        mytags = ep[w].keys()
    else:
        mytags = tags

    for i in mytags:

        # ep_sum = sum(ep.values())

        viterbi[i] = 0
        if i in tp:
            viterbi[i] += log(tp[i])  # - log(tp_sum)
        else:
            viterbi[i] += smooth
            # viterbi[i] += -float("inf")
            # viterbi[i] += log(1) - log(tp_sum)

        if w in ep:
            viterbi[i] += log(ep[w][i])  # - log(ep_sum)
        else:
            viterbi[i] += log(tag[i])
            # viterbi[i] += smooth

        backtrace[0][i] = "START"

    # for i in sorted(viterbi,key=viterbi.get,reverse=True):
    #     print i, viterbi[i], backtrace[0][i]

    # rest of the words
    for n in xrange(1, len(words)):
        w = words[n]

        backtrace.append(dict())

        newviterbi = dict()

        if w not in x["emission_prob"]:
            mytags = tags
        else:
            mytags = x["emission_prob"][w].keys()

        for cur in mytags:
            newviterbi[cur] = -float("inf")

            ep = x["emission_prob"]

            for prev in viterbi.keys():
                # print viterbi
                temp = viterbi[prev]

                if prev not in x["transition_prob"]:
                    temp += smooth
                else:
                    tp = x["transition_prob"][prev]
                    # tp_sum = sum(tp.values())

                    if cur in tp:
                        temp += log(tp[cur])  # - log(tp_sum)
                    else:
                        temp += smooth
                        # temp += log(tag[cur])

                if w in ep:
                    temp += log(ep[w][cur])  # - log(ep_sum)
                else:
                    # temp += smooth
                    temp += log(tag[cur])

                if temp > newviterbi[cur]:
                    newviterbi[cur] = temp
                    backtrace[n][cur] = prev

        viterbi = newviterbi

    finalstate = max(viterbi, key=viterbi.get)

    endtags = not True
    if endtags:

        ends = x["end_tag"]

        endmax = -float("inf")
        for i in viterbi:
            if i in ends:
                endtran = log(ends[i])
            else:
                endtran = smooth
            if endmax < viterbi[i] + endtran:
                endmax = viterbi[i] + endtran
                finalstate = i
    else:
        finalstate = max(viterbi, key=viterbi.get)

    # Backtrack
    state = finalstate
    n = len(words) - 1

    finaltags = []

    while state != "START":
        finaltags.insert(0, state)

        try:
            state = backtrace[n][state]
        except KeyError:
            print len(backtrace)
            print len(words)
            print backtrace, "\n"

        n -= 1

    return finaltags


with open("hmmmodel.txt") as f, open(sys.argv[1])as ip, open("hmmoutput.txt", 'w') as out:
    ss = time()

    x = json.loads(f.read())
    tags = x["transition_prob"].keys()
    tags.remove("START")

    y = ip.read().decode('utf-8').split('\n')

    count = 0
    correct = 0

    for index, val in enumerate(y):
        pred = doTheViterbi(y[index], tags, x)
        # print index
        # print pred

        # print y[index]
        # print y[index].decode('UTF-8').split(" ")
        bob = ' '.join(['/'.join([xa, ya]) for xa, ya in zip(y[index].split(" "), pred)])
        # print bob
        out.writelines(bob.encode('utf-8') + "\n")

    end = time()

    print "Time:", str(end - ss)
