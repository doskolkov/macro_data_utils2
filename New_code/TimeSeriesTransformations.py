from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif

import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

class type_transformations():
    '''
    Class contains methods to perfrom type transformations. There is also a config to call the methods by their code
    '''

    change_rates_scale = 100
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
        '''
        calculates year-on-year change of ts
        Args:
            ts: pd.timeseries indexed by dates

        Returns: pd.timeseries indexed by dates

        '''
        orig_df = pd.DataFrame({'value': ts}).reset_index()
        datecol = orig_df.columns[0]
        orig_df['year'] = orig_df[datecol].apply(lambda x: x.year)
        orig_df['month'] = orig_df[datecol].apply(lambda x: x.month)
        work_df = orig_df#.fillna(0)
        work_df['py_value'] = work_df.groupby('month')['value'].shift(1)
        work_df['yoy_change'] = (work_df['value']/work_df['py_value']-1)*self.change_rates_scale
        yoy_ts = work_df[[datecol,'yoy_change']].set_index(datecol)['yoy_change']

        return yoy_ts
    def ytd_accumulated(self, ts):
        '''
        calculates year-to-date sum of a ts
        Args:
            ts: pd.timeseries indexed by dates

        Returns: pd.timeseries indexed by dates

        '''
        orig_df = pd.DataFrame({'value':ts}).reset_index()
        datecol = orig_df.columns[0]
        orig_df['year'] = orig_df[datecol].apply(lambda x: x.year)
        orig_df['month'] = orig_df[datecol].apply(lambda x: x.month)
        work_df = orig_df.fillna(0)
        work_df['ytd'] = work_df.groupby('year')['value'].cumsum()
        ytd_ts = work_df[[datecol,'ytd']].set_index(datecol)['ytd']

        return ytd_ts

    def pp_change(self, ts):
        '''
        returns period-to-prev period change rate
        Args:
            ts: pd.timeseries indexed by dates

        Returns: pd.timeseries indexed by dates

        '''
        orig_df = pd.DataFrame({'value': ts}).reset_index()
        datecol = orig_df.columns[0]
        orig_df['pp_change'] = (orig_df['value']/orig_df['value'].shift(1)-1)*self.change_rates_scale
        pp_ts = orig_df[[datecol,'pp_change']].set_index(datecol)['pp_change']
        return pp_ts


    # ['yoy' - over same period from last year

class frequency_transformations():
    def get_config(self):
        config = {}

class normalization_transformations():

    def get_config(self):
        config = {}

class seasonal_adjustment_transformations():

    def get_config(self):
        config = {}