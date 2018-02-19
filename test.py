import json

with open("hmmmodel.txt") as f, open("train/zh_dev_raw.txt") as t:

    mod = json.loads(f.read())

    dev = t.read().split("\n")

    setofmod=set()
    setofdev=set()

    for i in dev:
        words = i.split(" ")

        for w in words:
            setofdev.add(w.decode('utf-8'))

    print len(setofdev)

    ep = mod["emission_prob"]

    for i in ep:

        for j in ep[i]:
            setofmod.add(j)

    print len(setofmod)

    print len(setofdev.intersection(setofmod))