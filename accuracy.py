import sys
import re

def gettok(x):
    k = x.rfind('/')
    return [x[:k], x[k + 1:]]


with open(sys.argv[1]) as f1, open(sys.argv[2]) as f2:

    correct=0
    count=0
    linecount=0
    while True:
        a = f1.readline()

        if not a:
            break

        b = f2.readline()

        if not b:
            break

        a = a.rstrip().split(' ')
        b = b.rstrip().split(' ')


        for x,y in zip(a,b):
            a1 = gettok(x)[1]
            b1 = gettok(y)[1]

            if a1 == b1:
                correct+=1
            else:
            #elif linecount in range (15,100):
                print "Line:",
                print linecount,
                print [x],
                print "should be",
                print [y]
            count+=1

        linecount+=1

    print correct
    print count
    print float(correct)*100/count,
    print "%"