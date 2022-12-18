import numpy as np
import torch as tr
import matplotlib.pyplot as plt

# read from the data generated (check data_generation.py for more info) 

class LinNet(tr.nn.Module):
    def __init__(self, input_size=115, hidden_size=32, output_size=1):
        super().__init__()
        self.to_hidden_1 = tr.nn.Linear(input_size, hidden_size)
        self.to_output = tr.nn.Linear(hidden_size, output_size)
        tr.nn.init.xavier_uniform_(self.to_hidden_1.weight)

    def forward(self, x):
        h_1 = tr.relu(self.to_hidden_1(x.reshape(x.shape[0],-1)))
        y = self.to_output(h_1)

        return y

if __name__ == "__main__":
    tmp_data = np.genfromtxt('data_zzhang96/train_data.csv', delimiter=',')
    tmp_testing_data = np.genfromtxt('data_zzhang96/test_data.csv', delimiter=',')
    input_data = tmp_data[:, 0:115].reshape(-1, 115)
    output_data = tmp_data[:, 115].reshape(-1, 1)
    input_test_data = tmp_testing_data[:, 0:115].reshape(-1, 115)
    output_test_data = tmp_testing_data[:, 115].reshape(-1, 1)

    curves = [], []

    print(input_data.shape)
    print(output_data.shape)

    # train the neural network
    my_nn = LinNet()
    loss_fn = tr.nn.MSELoss()
    optimizer = tr.optim.SGD(my_nn.parameters(), lr=0.000001)

    # convert the data to tensor
    tr_input_data = tr.from_numpy(input_data).float()
    tr_output_data = tr.from_numpy(output_data).float()
    tr_test_input_data = tr.from_numpy(input_test_data).float()
    tr_test_output_data = tr.from_numpy(output_test_data).float()

    for i in range(500):
        # forward pass
        y_pred = my_nn(tr_input_data)
        loss = loss_fn(y_pred, tr_output_data)

        # backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # print the loss
        print("epoch: {}, loss: {}".format(i, loss.item()))
        curves[0].append(loss.item())

        # test the model
        y_pred_test = my_nn(tr_test_input_data)
        loss_test = loss_fn(y_pred_test, tr_test_output_data)
        curves[1].append(loss_test.item())

    # plot the loss curve
    plt.plot(curves[0], label='train')
    plt.plot(curves[1], label='test')
    plt.legend()
    plt.show()