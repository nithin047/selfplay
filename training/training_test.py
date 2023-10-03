import torch
import numpy.random as rn
import numpy as np

from model.define_model import initialize_ml_model

def test_training_pipeline():

    # make the network learn a simple non-linear function

    input_size = 10
    output_size = 5
    dataset_size = 1000

    x = 100 * rn.uniform(size=(dataset_size, input_size))
    A = 10 * rn.uniform(size=(output_size, input_size))

    y = np.zeros((dataset_size, output_size))

    for i in range(dataset_size):
        y[i, :] = np.matmul(A, 3 * x[i, :] ** 4 + 5 * x[i, :] ** 3)


if __name__=="__main__":

    test_training_pipeline()


