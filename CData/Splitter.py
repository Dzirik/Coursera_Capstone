from CSupport.ConfigHandler import ConfigHandler
import numpy as np
import pandas as pd
import time
from sklearn.model_selection import StratifiedShuffleSplit

class Splitter(ConfigHandler):
    def __init__(self, config):
        super(Splitter, self).__init__(None)
        self.ss_indexes = {}
        
        self.report = {
            "X_train_shape": None,
            "Y_train_shape": None,
            "X_test_shape": None,
            "Y_test_shape": None,
            "X_val_shape": None,
            "Y_val_shape": None
        }
        
    def stratified_train_test_val(self, X, Y, test_size=None):
        X_train, Y_train, X_test, Y_test = self.stratified_train_test(X, Y, test_size)
        X_test, Y_test, X_val, Y_val = self.stratified_train_test(X_test, Y_test, 0.5)
        
        self.report["X_train_shape"] = X_train.shape
        self.report["Y_train_shape"] = Y_train.shape
        self.report["X_test_shape"] = X_test.shape
        self.report["Y_test_shape"] = Y_test.shape
        self.report["X_val_shape"] = X_val.shape
        self.report["Y_val_shape"] = Y_val.shape  
        
        return X_train, Y_train, X_test, Y_test, X_val, Y_val
        
    def stratified_train_test(self, X, Y, train_size=None):
        """
        :param X: Numpy nD array.
        :param Y: Numpy 2D array.
        :param train_size: float. Number between 0 and 1.
        
        :returns: (X_train, Y_train, X_test, Y_test)
        """
        if train_size is None:
            train_size = self.config.getfloat("splitting", "train_size")
        self.stratified(
            X, 
            Y, 
            train_size,
            1, 
            self.config.getint("splitting", "random_state")
        )
        
        idx = self.ss_indexes[0][0]
        id = self.ss_indexes[0][1]
        
        return (X[idx, :], Y[idx, :], X[id, :], Y[id, :])
    
    def stratified(self, X, Y, train_size, n_splits=1, random_state=None):
        """
        :param X: Numpy 2D array.
        :param Y: Numpy 2D array.
        :param test_size: float. Number between 0 and 1.
        :param n_splits: Integer.
        :param random_state: Integer
        """
        start_time = time.time()
        
        self.ss = StratifiedShuffleSplit(
            n_splits=n_splits,
            test_size=1 - train_size,
            random_state=random_state
        )
        self.ss = self.ss.split(X,Y)
        
        self.ss_indexes = {}
        for i in range(n_splits):            
            self.ss_indexes[i] = next(self.ss)
            #print("Y 0/1 ratio: " + str(i) + str(sum(Y[self.ss_indexes[i]])/len(self.ss_indexes[i])))
            
            
    def get_report(self):
        return self.report