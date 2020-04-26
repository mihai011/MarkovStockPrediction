import random
import numpy as np


def choose(index, chance):

    if chance > index:
        return 'W'
    return 'B'

def main():

    chance_WW = 0.1
    chance_WB = 0.9

    chance_BW = 0.9
    chance_BB = 0.1

    counts = 10000
    s = 'B'
    
    for i in range(counts):
        
        chance = random.uniform(0,1)
        if s[-1] == 'W':
            s+= choose(chance, chance_WW)
            continue

        if s[-1] == 'B':
            s+= choose(chance, chance_BW)
            continue
        

    print(s[1:].count('W'))
    print(s.count('B'))
    print(s[1:].count('W')/s.count("B"))

    counts_WW = 0
    counts_WB = 0
    counts_BW = 0
    counts_BB = 0

    for i in range(1,len(s)-1):
        
        if s[i] == 'W' and s[i+1] == 'W':
            counts_WW += 1
        if s[i] == 'W' and s[i+1] == 'B':
            counts_WB += 1
        if s[i] == 'B' and s[i+1] == 'W':
            counts_BW += 1
        if s[i] == 'B' and s[i+1] == 'B':
            counts_BB += 1

    print('WW %f' % float(counts_WW/(counts_WW+counts_WB)))
    print('WB %f' % float(counts_WB/(counts_WW+counts_WB)))
    print('BW %f' % float(counts_BW/(counts_BB+counts_BW)))
    print('BB %f' % float(counts_BB/(counts_BB+counts_BW)))

    WW = counts_WW/(counts_WW+counts_WB)
    WB = counts_WB/(counts_WW+counts_WB)
    BW = counts_BW/(counts_BB+counts_BW)
    BB = counts_BB/(counts_BB+counts_BW)

    init = np.matrix([0.1,0.9])
    stoch_mat = np.matrix([[WW, WB],[BW, BB]])

    for _ in range(2000):
        init = init.dot(stoch_mat)
        print(init)
    



if __name__ == "__main__":
    main()