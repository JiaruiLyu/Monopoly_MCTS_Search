import numpy

# read from the data generated (check data_generation.py for more info) 
if __name__ == "__main__":
    data = numpy.genfromtxt('train_data.csv', delimiter=',')
    print(data.shape)
    print(data[0][115])