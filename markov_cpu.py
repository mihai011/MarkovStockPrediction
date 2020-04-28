import numpy as np
from numba import jit
from numba import cuda
from tqdm import tqdm

import matplotlib.pyplot as plt
from visualization_stock import *

#@cuda.jit
@jit(nopython=True)
def make_matrix(m):
    for i in range(m.shape[0]):
        m[i] = m[i]/np.sum(m[i])

    return m


class Markov:
    """Class that implements a markov Chain for stock prediction"""

    def __init__(self, path, column, steps):

        arr = get_column(path,column)
        # Making data to discrete steps
        data = stock_made_discrete(arr,steps)

        self.symbols = {}
        self.transitions = np.array([])
        self.stochastic_matrix = None
        counter = -1

        # Reading the chain , counting transitions and symbols  
        for i in tqdm(range(1,len(data)-1,1)):

            if data[i] not in self.symbols.keys():
                counter += 1
                self.symbols[data[i]] = counter
                
                if self.transitions.size == 0:
                    self.transitions = np.array([0.])
                    continue

                r = np.zeros((1,counter), dtype=float)
                c = np.zeros((counter+1,1), dtype=float)
                self.transitions = np.vstack((self.transitions, r))
                self.transitions = np.hstack((self.transitions, c))

            if data[i+1] not in self.symbols.keys():
                counter += 1
                self.symbols[data[i+1]] = counter

                r = np.zeros((1,counter), dtype=int)
                c = np.zeros((counter+1,1), dtype=int)
                self.transitions = np.vstack((self.transitions, r))
                self.transitions = np.hstack((self.transitions, c))

            if self.transitions.size == 1:
                self.transitions[0] = self.transitions[0] + 1
            else:
                self.transitions[self.symbols[data[i]]][self.symbols[data[i+1]]]= \
                    self.transitions[self.symbols[data[i]],self.symbols[data[i+1]]]+1

        print(self.symbols)

    def make_stochastic_matrix(self):
        """create stochastic matrix for predictions"""

        self.stochastic_matrix = cuda.to_device(self.stochastic_matrix)
        self.stochastic_matrix = make_matrix(self.transitions) 

        print(self.stochastic_matrix)      
    
    def predict_chain(self,init, count):
        """make predictions for "count" paces"""

        history = []

        inv_map = {v: k for k, v in self.symbols.items()}

        for _ in range(count):
            init = np.dot(init, self.stochastic_matrix)
            history.append(init)

        for index in range(len(init)):
            line = [h[index] for h in history]
            plt.plot(line,label=inv_map[index])

        plt.legend()
        plt.show()
        plt.show(block=False)


        return init

if __name__ == "__main__":

    #initiate object for Markov chain  
    m = Markov("Stocks/googl.us.txt","Close",10)
    m.make_stochastic_matrix()

    arr = np.arange(len(m.symbols))
    arr = arr/np.sum(arr)
    np.random.shuffle(arr)

    res = m.predict_chain(arr,5)
    


               


                


            