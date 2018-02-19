import json
from math import log
from time import time
import sys

smooth = -15


def gettok(x):
    k = x.rfind('/')
    return [x[:k], x[k + 1:]]


def doTheViterbi(sentence, tags, x):
    words = sentence.split(" ")

    viterbi = dict()
    backtrace = []

    # initial prob
    backtrace.append(dict())

    tp = x["transition_prob"]["START"]
    tp_sum = sum(tp.values())

    for i in tags:
        ep = x["emission_prob"][i]
        ep_sum = sum(ep.values())

        viterbi[i] = 0
        if i in tp:
            viterbi[i] += log(tp[i]) - log(tp_sum)
        else:
            viterbi[i] += smooth
            # viterbi[i] += -float("inf")
            # viterbi[i] += log(1) - log(tp_sum)

        w = words[0]
        if w in ep:
            viterbi[i] += log(ep[w]) - log(ep_sum)
        else:
            viterbi[i] += smooth
            # viterbi[i] += -float("inf")
            # viterbi[i] += log(1) - log(ep_sum)

        backtrace[0][i] = "START"

    # for i in sorted(viterbi,key=viterbi.get,reverse=True):
    #     print i, viterbi[i], backtrace[0][i]

    # rest of the words
    for n in xrange(1, len(words)):
        w = words[n]

        backtrace.append(dict())

        newviterbi=dict()

        for cur in tags:
            newviterbi[cur] = -float("inf")

            ep = x["emission_prob"][cur]
            ep_sum = sum(ep.values()) + len(tags)

            for prev in tags:
                #print viterbi
                temp = viterbi[prev]

                tp = x["transition_prob"][prev]
                tp_sum = sum(tp.values())

                if cur in tp:
                    temp += log(tp[cur] + 1) - log(tp_sum)
                else:
                    temp += smooth
                    # temp += -float("inf")
                    # temp += log(1) - log(tp_sum)

                if w in ep:
                    temp += log(ep[w] + 1) - log(ep_sum)
                else:
                    temp += smooth
                    # temp += -float("inf")
                    # temp += log(1) - log(ep_sum)

                if temp > newviterbi[cur]:
                    newviterbi[cur] = temp
                    backtrace[n][cur] = prev

        viterbi=newviterbi

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
            print viterbi[10]
            print x["transition_prob"]["VBG"]["NNS"]
            raw_input()
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
