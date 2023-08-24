from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif

import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

class type_transformations():

    def get_config(self):
        '''

        Returns: dict; dictionary that contains methods of the class

        '''
        config = {
            'index': self.series_to_index,
            'rate': self.series_to_rate,
            'value': self.value_to_value,
            'index_to_rate': self.index_to_rate,
            'yoy': self.yoy_change,
            'ytd': self.ytd_accumulated,
            'pp': self.pp_change
        }
        return config
    def series_to_index(self, ts, norm_value = 100):
        '''
        !!!! nans may not be touched
        Args:
            ts: pd.timeseries indexed with dates
            norm_value: index normalization value

        Returns: pd.timeseries indexed with dates

        '''
        trs = ts/ts.shift(1)
        index_ts = trs.fillna(1).cumprod()*norm_value
        return index_ts
    def series_to_rate(self, ts): # не меняем
        '''
        does nothing to a ts
        Args:
            ts: pd.timeseries indexed with dates

        Returns: pd.timeseries indexed with dates

        '''
        return ts
    def value_to_value(self, ts): # не меняем
        '''
        multiplies input by unity
        Args:
            ts: pd.timeseries indexed with dates

        Returns: pd.timeseries indexed with dates

        '''
        ts *= 1
        return ts
    def index_to_rate(self, ts):
        ts *= 1
        return ts

    def yoy_change(self, ts):
        ts *= 1
        return ts
    def ytd_accumulated(self, ts):
        ts *= 1
        return ts

    def pp_change(self, ts):
        ts *= 1
        return ts


    # ['yoy' - over same period from last year
#     'ytd' - накопленный с начала года
# 'pp' к прошлому периоду

class frequency_transformations():
    def get_config(self):
        config = {}

class normalization_transformations():

    def get_config(self):
        config = {}

class seasonal_adjustment_transformations():

    def get_config(self):
        config = {}