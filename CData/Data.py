import CData.DataReader as DR
import CData.DFExploration as DFE
import CData.Splitter as S
import CData.DataTransformator as T
import numpy as np
import pandas as pd
from GLOBAL_CONSTANTS import *


class Data(object):

    columns_types = {
         "accountid":"Not-used",
         "learning_group":"Not-used",
         "successful_lead":"Not-used",
         "probability_of_success":"Not-used",
         "probability_of_success_channel_call":"Not-used",
         "probability_of_success_channel_email":"Not-used",
         "probability_of_success_channel_mail":"Not-used",
         "probability_of_success_channel_sms":"Not-used",
         "ep_akceptacia":"category",
         "volany_z_lead":"category",
         "ep_kampan":"category",
         "reakcia_l3m":"category",
         "call_l3m":"category",
         "feature_count_interested_response":"category",
         "feature_count_not_interested_response":"category",
         "feature_has_gas":"category",
         "feature_has_ee":"category",
         "feature_odber":"category",
         "feature_has_email":"category",
         "feature_has_telephone":"category",
         "fetaure_customer_has_left":"category",
         "feature_live_customer_flag":"category",
         "feature_client_in_default":"category",
         "feature_normal_client":"category",
         "feature_has_ep_product":"category",
         "feature_has_pracka":"category",
         "feature_has_kotol":"category",
         "feature_has_tr":"category",
         "feature_has_kv":"category",
         "feature_has_led":"category",
         "feature_has_sprcha":"category",
         "feature_has_alarm":"category",
         "feature_has_ohr":"category",
         "feature_has_zasuvka":"category",
         "feature_has_filter":"category",
         "feature_uzemie":"category",
         "feature_okres":"category",
         "feature_mikrosegment_aktual":"category",
         "feature_cisty_potencial":"f8",
         "feature_client_value":"f8",
         "feature_client_value_group":"category",
         "feature_gas_d1":"category",
         "feature_city_1000_plus":"category",
         "feature_ov_sa_rovna_om_adrese":"category",
         "feture_house":"category",
         "feature_odber_no":"category",
         "feature_has_nekom_wo_kv":"category",
         "feature_pocet_om":"category",
         "feature_pocet_kom_om_gas":"category",
         "feature_pocet_kom_om_ee":"category",
         "feature_vek":"f8",
         "feature_pohlavie":"category",
         "feature_count_portfolio_inactive":"category",
         "feature_count_portfolio_active":"category",
         "pocet_nekom_produktov":"category"
    }


    def __init__(self):
        self.dr = DR.DataReader(None)
        self.dfe = DFE.DFExploration()
        self.sp = S.Splitter(None)
        self.tr = T.DataTransformator(None)

        self.train_columns = None

    def pipeline_read_and_prepare_final_data_for_modelling(self, only_uc_2=True):
        self.obtain_data(only_uc_2)
        clean_simplified = self.process_attributes(report=False)
        clean_simplified_final_oh = self.create_one_hot_encoding(clean_simplified, CATEGORICAL_COLUMNS)
        clean_simplified_final_oh = self.scale_continuous_variable(clean_simplified_final_oh, CONTINUOUS_COLUMNS)
        print(clean_simplified_final_oh[CONTINUOUS_COLUMNS].describe())
        (X_blind, X_blind_index, X_train, Y_train, X_test, Y_test) = self.split_data(clean_simplified_final_oh)

        return (X_blind, X_blind_index, X_train, Y_train.flatten(), X_test, Y_test.flatten())

    def obtain_data(self, only_uc_2=True):
        """

        :return:
        """
        # raw data reading
        self.dr.read_data(only_uc_2)

        #converting "," to "." to get texts
        self.dr.data_dict["uc2_simplified"]["feature_cisty_potencial"] = [
            float(x.replace(",", ".")) if type(x) == str else x for x in
            list(self.dr.data_dict["uc2_simplified"]["feature_cisty_potencial"])
        ]

    def process_attributes(self, report=False):

        simplified = self.dr.get_data("uc2_simplified").copy()
        self.clean_age(simplified, "feature_vek")
        for col, cat in self.columns_types.items():
            if cat == "category":
                self.convert_to_categorical(simplified, col, "Undefined")
            elif cat == "f8":
                self.process_continuous_columns(simplified, col)

            if report:
                print(f"Column named \"{col}\" has type: {simplified[col].dtype}")
        print("\n")

        simplified[Y_COLUMN] = simplified[Y_COLUMN].astype(int)

        return simplified

    def create_one_hot_encoding(self, df, columns_for_one_hot):
        print(f"Clean simplified shape is: {df.shape}")
        clean_simplified_final = df[[ID_COLUMN] + [Y_COLUMN] + X_COLUMNS]
        print(f"Clean simplified final shape is: {clean_simplified_final.shape}")
        clean_simplified_final_oh = pd.get_dummies(clean_simplified_final,
                                                   prefix=columns_for_one_hot, columns=columns_for_one_hot)
        print(f"Clean simplified final oh shape is: {clean_simplified_final_oh.shape}")

        return clean_simplified_final_oh

    def split_data(self, clean_simplified_final_oh):
        learn_index = list(self.dr.data_dict["uc2_simplified"][COLUMN_LEARNING] != "target")
        X_blind = clean_simplified_final_oh.loc[
            [not b for b in learn_index],
            clean_simplified_final_oh.columns != Y_COLUMN
        ]
        X_blind_index = X_blind[ID_COLUMN]
        X_blind.drop(labels=ID_COLUMN, axis=1, inplace=True)
        print(f"Column accountid is present in X_blind_drop: {ID_COLUMN in X_blind.columns}")
        print(f"X_blind shape is: {X_blind.shape}")
        X_learn = clean_simplified_final_oh.loc[learn_index, clean_simplified_final_oh.columns != Y_COLUMN]
        X_learn.drop(labels=ID_COLUMN, axis=1, inplace=True)
        self.train_columns = list(X_learn.columns)
        print(f"Length of train_columns is: {len(self.train_columns)}")
        print(f"Column accountid is present in X_blind_drop: {ID_COLUMN in X_learn.columns}")
        Y_learn = clean_simplified_final_oh.loc[learn_index, [Y_COLUMN]]
        print(f"X_learn shape is: {X_learn.shape}")
        print(f"Y_learn shape is: {Y_learn.shape}")

        (X_train, Y_train, X_test, Y_test) = self.sp.stratified_train_test(X_learn.as_matrix(), Y_learn.as_matrix())
        print(f"X_train shape is: {X_train.shape}")
        print(f"Y_train shape is: {Y_train.shape}")
        print(f"Y_train sum is: {sum(Y_train)}")
        print(f"X_test shape is: {X_test.shape}")
        print(f"Y_test shape is: {Y_test.shape}")
        print(f"Y_test sum is: {sum(Y_test)}")

        return (X_blind, X_blind_index, X_train, Y_train, X_test, Y_test)

    def get_train_columns(self):
        return self.train_columns

    def convert_to_categorical(self, df, col_name, cat_name_for_NaN):
        col = df[col_name]
        col = col.astype("category")
        col.cat.add_categories(cat_name_for_NaN, inplace=True)
        col.fillna(cat_name_for_NaN, inplace=True)

        df[col_name] = col

    def clean_age(self, df, col_name):
        logic = [not (x & y) for x, y in zip(df[col_name] >= 18, df[col_name] <= 118)]
        df[col_name][logic] = np.nan

    def process_continuous_columns(self, df, col_name):
        is_nan = df[col_name].isna()
        df[col_name + "_is_nan"] = is_nan.astype("category")
        df[col_name][is_nan] = df[col_name].mean(axis=0, skipna=True)

    def scale_continuous_variable(self, df, columns):
        self.tr.setScaleTr(columns)
        return self.tr.fitScaleTr(df)