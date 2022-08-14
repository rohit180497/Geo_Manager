import numpy as np


import numpy as np
import pandas as pd

from common.utils.geo_manager import GeoManager
from common.utils.util_manager import tprint


class GeoProximity:

    def __init__(self, df, search_field, pincode_field='pincode') -> None:
        self.df = df
        self.search_field = search_field
        self.pincode_field = pincode_field
        self.__initialize_dist_mat()

    def __initialize_dist_mat(self):
        gm = GeoManager()

        self.df = self.df.join(pd.DataFrame
                                (gm.get_county_state(self.df[self.pincode_field])).T)

        self.df.rename({0: 'geo_county', 1: 'geo_state'}, axis=1, inplace=True)

        df_search_pin = self.df[[
            self.search_field, self.pincode_field
        ]].copy()

        tprint('First draft for distance matrix started')

        dist_mat = pd.DataFrame([df_search_pin[self.pincode_field].tolist()] * len(df_search_pin),
                                    columns=df_search_pin[self.search_field].values,
                                    index=df_search_pin[self.search_field].values)

        tprint('First Distance Matrix Computed! ')

        x = dist_map.copy()
        y = dist_map.T.copy()

        tprint'Flattening Distance matrix to craete a searchable series')
        z=[]
        for i in range(len(x)):
            z.append(gm.get_flight_distance(x.iloc[:, i], y.loc[:, i]))

        self.dist_mat=pd.DataFrame(z, columns = x.columns, index = y.columns)
        tprint('Distance matrix ready for search computed')

    def search_k_nearest(self, search_key, k = 5):
        search_result=dict(zip(self.dist_mat.loc[search_key].sort_values()[:k+1].index),
                            self.dist_mat.loc[search_key].sort_values()[:k+1].values))

        search_df=self.df[(self.df[self.search_field].isin(
            search_result.keys()))].copy()
        search_df[self.search_field]=search_df[self.search_field].astype(
            "Category")
        search_df[self.search_field].cat.set_categories(
            search_result.keys(), inplace=True)
        search_df=search_df.sort_values(
            [self.search_field]).reset_index(drop=True)

        search_df["Disance"]=search_result.values()

        key_df=search_df[search_df[self.search_field] == search_key].copy()

        search_df=search_df[search_df[self.search_field] != search_key].copy()

        search_df=pd.concat([key_df, search_df], axis=0, ignore_index=True)

        return search_df.reset_index(drop=True)
