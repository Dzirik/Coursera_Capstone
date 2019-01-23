from sklearn.datasets import make_classification
from sklearn.datasets import make_regression
import numpy as np

class ToyData(object):
    def __init__(self):
        pass


    def get_toy_data(self):
        X, Y = self.classification(500, 4, 2)
        X_train = X[0:300, :]
        Y_train = Y[0:300]
        Y_train = Y_train.flatten()

        X_test = X[300:400, :]
        Y_test = Y[300:400]
        Y_test = Y_test.flatten()

        X_blind = X[400:500,:]
        X_blind_index = range(100,200)

        return (X_blind, X_blind_index, X_train, Y_train, X_test, Y_test)
    
    def classification(self, n_samples, n_features, n_classes):
        X, Y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_features,
            n_clusters_per_class=1,
            n_redundant=0,
            n_classes=n_classes,
            random_state=9877
        )
        
        Y = Y.reshape(len(Y), 1)
        return X, Y.astype(np.float32)
    
    def regression(self):
        pass