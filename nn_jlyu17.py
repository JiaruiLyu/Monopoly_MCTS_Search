import numpy 
import scipy.special
import torch
import torch.nn as nn
import pandas as pd
import csv

class Net(nn.Module):
  
    def __init__(self, features):
        super(Net, self).__init__()
        
        self.linear_relu1 = nn.Linear(features, 250)
        self.linear_relu2 = nn.Linear(250, 500)
        self.linear_relu3 = nn.Linear(500, 500)
        self.linear_relu4 = nn.Linear(500, 500)
        self.linear5 = nn.Linear(500, 1)

    def forward(self, x):
        
        y_pred = self.linear_relu1(x)
        y_pred = nn.functional.relu(y_pred)

        y_pred = self.linear_relu2(y_pred)
        y_pred = nn.functional.relu(y_pred)

        y_pred = self.linear_relu3(y_pred)
        y_pred = nn.functional.relu(y_pred)

        y_pred = self.linear_relu4(y_pred)
        y_pred = nn.functional.relu(y_pred)

        y_pred = self.linear5(y_pred)
        return y_pred

# read from the data generated (check data_generation.py for more info) 
if __name__ == "__main__":

    train_data = numpy.genfromtxt('train_data.csv', delimiter=',')
    test_data = numpy.genfromtxt('test_data.csv', delimiter=',')
    train_data = numpy.delete(train_data,118,axis=1)
    test_data = numpy.delete(test_data,118,axis=1)

    ####### Start of updating dataset
    # land_price_rent_rate_train is a 16*500 array
    # e.g. land_price_rent_rate_train[14][499] represent the 15th grid's last data's ratio of land price / land rent
    land_price_rent_rate_train = []
    land_price_rent_rate_test = []
    for i in range (0, 16):
        temp_train_col = numpy.around(train_data[:,64+i] / train_data[:,80+i], 4)
        temp_test_col = numpy.around(test_data[:,64+i] / test_data[:,80+i], 4)
        land_price_rent_rate_train.append(temp_train_col)
        land_price_rent_rate_test.append(temp_test_col)
    
    p_train = pd.DataFrame(land_price_rent_rate_train).T 
    full_train = numpy.insert(numpy.array(p_train), 16, values=numpy.array(train_data[:, 117]), axis=1)
    pd.DataFrame(full_train).to_csv('train.csv', header=False, index=False)
    
    p_test = pd.DataFrame(land_price_rent_rate_test).T 
    full_test = numpy.insert(numpy.array(p_test), 16, values=numpy.array(test_data[:, 117]), axis=1)
    pd.DataFrame(full_test).to_csv('test.csv', header=False, index=False)
    
    ftrain_data = numpy.genfromtxt('train.csv', delimiter=',')
    ftest_data = numpy.genfromtxt('test.csv', delimiter=',')
    ####### End of updating dataset

    target = ftrain_data[:, 16]
    train_labels = torch.tensor(target, dtype=torch.float).view(-1, 1) # train_labels.shape: torch.Size([500, 1])
    train_features = torch.tensor(ftrain_data[:ftrain_data.shape[0]], dtype=torch.float)  # train_features.shape: torch.Size([500, 118])
    test_features = torch.tensor(ftest_data[:ftest_data.shape[0]], dtype=torch.float) # test_features.shape: torch.Size([500, 118])

    model = Net(features=train_features.shape[1])

    # Loss
    criterion = nn.MSELoss(reduction='mean')

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    losses = []

    # Train 500 rounds
    for t in range(500):
        y_pred = model(train_features)
        
        loss = criterion(y_pred, train_labels)
        # print(t, loss.item())
        losses.append(loss.item())
        
        if torch.isnan(loss):
            break
        
        optimizer.zero_grad()
        
        loss.backward()

        optimizer.step()
        
    ###Test
    predictions = model(test_features).detach().numpy()
    newp = []
    for i in range(len(predictions)):
        if predictions[i] <= 0:
            newp.append(0)
        else:
            newp.append(1)
    pd.DataFrame(predictions).to_csv('predict.csv', header=False, index=False)
    pd.DataFrame(newp).to_csv('newpredict.csv', header=False, index=False)
    # with open('e.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
        
    #     writer.writerow(predictions)


