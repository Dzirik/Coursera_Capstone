import numpy as np
import pandas as pd
import CVisualization.Visualization as V


class DFExploration(object):

    def __init__(self):
        self.visu = V.Visualization()

    def print_attr_stats(self, df, min_unique=20):
        """
        Prints df colulmns stats.
        :param df: DataFrame
        """

        for col in df.columns:
            self.print_single_attr_stats(df, col, min_unique)
            # print(col)
            # print(f" Column type: {df[col].dtype}")
            # print(f" Number of Null values: {df[[col]].isnull().sum()[0]}")
            # print(f" Number of unique values is:{len(df[col].value_counts())}")
            # print(f" Percentage of unique values is: {len(df[col].value_counts())/df.shape[0]}")
            # if len(df[col].value_counts()) < min_unique:
            #     pom = df[col].value_counts()
            #     print("\n")
            #     print(pom)
            #     self.visu.bar_plot(pom.index, pom, (5,5))
            # if df[col].dtype == "float64" and df[[col]].isnull().sum()[0] == 0:
            #     self.visu.histogram(df[col])
            # print("\n")

    def print_single_attr_stats(self, df, col_name, min_unique=20):
        print("####################################################################################################")
        print(f"Column Name: {col_name}")
        print(f" Column type: {df[col_name].dtype}")
        print(f" Number of Null values: {df[[col_name]].isnull().sum()[0]}")
        print(f" Number of unique values is:{len(df[col_name].value_counts())}")
        print(f" Percentage of unique values is: {len(df[col_name].value_counts())/df.shape[0]}")
        if len(df[col_name].value_counts()) < min_unique:
            pom = df[col_name].value_counts()
            print("\n")
            print(pom)
            self.visu.bar_plot(pom.index, pom, (5, 5))
        if df[col_name].dtype == "float64" and df[[col_name]].isnull().sum()[0] == 0:
            self.visu.histogram(df[col_name])
        print("\n")

    def attrs_are_equal(self, df, col_1, col_2):
        """

        :param df: DataFrame.
        :param col_1: String.
        :param col_2: String.
        :return: Boolean
        """

        # alternative approach
        """
        c1 = list(df[col_1])
        c2 = list(df[col_2])
        id = [x == y for x,y in zip(t1, t2)]
        if sum(id) == 0:
            return True
        else:
            return False
        """

        c1 = df[col_1]
        c2 = df[col_2]

        return c1.equals(c2)

    def create_deviation_attributes(self, df):
        """
        :param df: DataFrame. data_hluk_stav
        """
        self.create_dev_from_limit_att(df)
        self.create_out_of_limit_att(df)
        self.create_vysledek_0_1_att(df)

    def create_dev_from_limit_att(self, df):
        """
        :param df: DataFrame. data_hluk_stav
        """
        df["Dev_from_Limit"] = df["Limit"] - df["4-Z H1"]

    def create_out_of_limit_att(self, df):
        """
        :param df: DataFrame. data_hluk_stav
        """
        df["Out_of_Limit"] = [1 if x > 1 else 0 for x in df["relativni "]]

    def create_vysledek_0_1_att(self, df):
        """
        :param df: DataFrame. data_hluk_stav
        """
        df["Výsledek_0_1"] = [1 if x != "i.O." else 0 for x in df["Výsledek"]]

    def delete_attribute(self, df, attr_name):
        """

        :param df: DataFrame. data_hluk_stav
        :param attr_name: String. Name of attribute.
        :return:
        """
        df.drop(attr_name, axis=1, inplace=True)