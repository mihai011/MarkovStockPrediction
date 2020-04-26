import matplotlib.pyplot as plt
import pandas as pd

def plot_column(path,column):

    stock = pd.read_csv(path)
    stock.plot(x='Date',y=column)

    plt.show()

def get_column(path, column):

    stock = pd.read_csv(path)
    return stock[column].to_numpy()

def stock_made_discrete(array, steps):

    diff = array.max() - array.min()
    distance = diff/steps 

    interval_points = [i for i in range(int(array.min()), int(array.max()), int(distance))]
    states = {}
    
    for i in range(len(interval_points)-1):

        states[i] = (interval_points[i], interval_points[i+1])

    sequence = []

    for v in array:
        for s in states.keys():
            if v > states[s][0] and v < states[s][1]:
                sequence.append(str(s))
                break

    return sequence



if __name__ == "__main__":

    plot_column("Stocks/googl.us.txt","Close")
    arr = get_column("Stocks/googl.us.txt","Close")
    seq = stock_made_discrete(arr,1000)
    print(seq)