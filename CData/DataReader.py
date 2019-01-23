from CSupport.ConfigHandler import ConfigHandler
import pandas as pd
import numpy as np
import os
import sys

class DataReader(ConfigHandler):
    
    """
    Reads data to the dictionary.
    """
    
    def __init__(self, config):
        """
        :param config: None or configparser. If None, default configparser 
                       "config.ini" is read from parent directory.
        """
        super(DataReader, self).__init__(config)
        
        self.data_dict = {}
    
    
    def read_data(self, only_uc_2=True):
        """
        reads all data set at once
        """
        if only_uc_2:
            self.data_dict["uc2_simplified"] = self.read_df_from_csv(
                self.config.get("data", "uc2_simplified"),
                ","
            )
        else:
            self.data_dict["elektromery"] = self.read_df_from_csv(
                self.config.get("data", "elektromery"),
                ","
            )
            self.data_dict["unikatni_elektromer"] = self.read_df_from_csv(
                self.config.get("data", "unikatni_elektromer"),
                ","
            )
        

    def get_data(self, df_key):
        """
        :param df_key: String. The key of data set.

        :returns: DataSet.
        """
        return self.data_dict[df_key]
        
    def read_df_from_xls(self, xls_name):
       """
       :param xls_name: string
       """
       return pd.read_excel(os.path.join(self.config.get(
            "path", "raw_data"), xls_name))

    def read_df_from_csv(self, csv_name, delimiter=","):
        """
        :param xls_name: string
        """
        return pd.read_csv(os.path.join(self.config.get(
            "path", "raw_data"), csv_name), delimiter=delimiter)

    def save_df_as_pickle(self, df, file_name):
        """

        :param df: DataFrame. DF to save.
        :param file_name: String. File name without .pkl.
        """
        df.to_pickle(os.path.join(self.config.get(
            "path", "final_data"), file_name))

    def save_df_as_csv(self, df, file_name, separator=";"):
        """
        :param df: DataFrame. DF to save.
        :param file_name: String. File name without .csv
        """
        df.to_csv(
            os.path.join(self.config.get("path", "final_data"), file_name+".csv"),
            sep=separator,
            index=False
        )

    def load_file_from_pickle(self, file_name):
        """

        :param file_name: String. File  name without .pkl.
        :return: DataFrame
        """
        return pd.read_pickle(os.path.join(self.config.get(
            "path", "final_data"), file_name))