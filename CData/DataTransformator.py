from CSupport.ConfigHandler import ConfigHandler
import pandas as pd

class DataTransformator(ConfigHandler):
    
    def __init__(self, config):
        """
        :param config: None or configparser. If None, default configparser 
                       "config.ini" is read from parent directory.
        """
        super(DataTransformator, self).__init__(config)

    ####################################################################################################
    # SCALING TRANSFORMATOR ############################################################################
    ####################################################################################################
    # (x)/sigma
    # correction

    def setScaleTr(self, columns):
        """
        Set scaling transformator.

        :param columns: None or list - columns of X to use for one-hot encoding. If None, config is used.
        """
        if columns is None:
            columns = self.config.get("columns", "X_for_scale").split(",")

        self.scaling_tr = {}
        for col in columns:
            self.scaling_tr[col] = {"mean": 0.0, "std": 0.0, "idx": 0}

    def fitScaleTr(self, X):
        """
        Fit scaling transformator due to data X and return transformed X.

        :param X: data frame

        :returns: transformed data frame
        """

        for key in self.scaling_tr.keys():
            self.scaling_tr[key]["mean"] = X[key].mean()
            self.scaling_tr[key]["std"] = X[key].std()
            self.scaling_tr[key]["idx"] = X.columns.get_loc(key)

            if self.scaling_tr[key]["std"] > 0:
                X[key] = [(val - self.scaling_tr[key]["mean"]) /
                          self.scaling_tr[key]["std"] for val in X[key]]

        return X

    def trScale(self, X):
        """
        Transform X due to scaling.

        :param X: list or data frame

        :returns: list or data frame
        """
        if type(X) == list:
            for key in self.scaling_tr.keys():
                if self.scaling_tr[key]["std"] > 0:
                    X[self.scaling_tr[key]["idx"]] = \
                        (X[self.scaling_tr[key]["idx"]] - self.scaling_tr[key]["mean"]) / self.scaling_tr[key]["std"]
                else:
                    X[self.scaling_tr[key]["idx"]] = 0
            return X
        elif type(X) == pd.core.frame.DataFrame:
            for key in self.scaling_tr.keys():
                if self.scaling_tr[key]["std"] > 0:
                    X[key] = [(val - self.scaling_tr[key]["mean"]) /
                              self.scaling_tr[key]["std"] for val in X[key]]
                else:
                    X[key] = [0 for val in X[key]]
            return X