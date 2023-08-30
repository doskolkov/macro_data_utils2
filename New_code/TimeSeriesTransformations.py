from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif

import numpy as np
import pandas as pd
from datetime import datetime

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
            'rate': self.unity_transformation,
            'value': self.unity_transformation,
            'index_to_rate': self.index_to_rate,
            'yoy': self.yoy_change,
            'ytd': self.ytd_accumulated,
            'pp': self.pp_change
        }
        return config
    def series_to_index(self, ts, norm_value = 100):
        '''
        transforms series to index. nan values are ignored.
        Args:
            ts: pd.timeseries indexed with dates
            norm_value: index normalization value

        Returns: pd.timeseries indexed with dates

        '''
        work_ts = ts.dropna()
        trs = work_ts/work_ts.shift(1)
        raw_index_ts = trs.fillna(1).cumprod()*norm_value
        index_ts = ts.apply(lambda x: np.nan).fillna(raw_index_ts)
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
        calculates year-to-date sum of a ts.
        !!!!  nans may be wrong
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

    def unity_transformation(self, ts):
        return ts

    # ['yoy' - over same period from last year

class frequency_transformations():
    def get_config(self):
        config = {
            'weekly_eop':self.weekly_eop,
            'monthly_eop':self.monthly_eop,
            'quarterly_eop':self.quarterly_eop,
            'annual_eop':self.annual_eop,
            'weekly_avr':self.weekly_avr,
            'monthly_avr':self.monthly_avr,
            'quarterly_avr':self.quarterly_avr,
            'annual_avr':self.annual_avr,
            'weekly_sum':self.weekly_sum,
            'monthly_sum':self.monthly_sum,
            'quarterly_sum':self.quarterly_sum,
            'annual_sum':self.annual_sum
        }
        return config
    def weekly_eop(self,ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to weekly")

        elif freq == 'd':
            orig_df = pd.DataFrame({'value':ts}).reset_index()
            datecol = orig_df.columns[0]
            orig_df['day'] = orig_df[datecol].apply(lambda x: x.weekday())
            orig_df['week'] = orig_df[datecol].apply(lambda x: x.week)
            orig_df = orig_df.merge(orig_df.groupby('week')['day'].max().reset_index().rename(columns={'day':'max_week_day'}), how = 'left', left_on = 'week',right_on='week')
            ts = orig_df.loc[orig_df['day']==orig_df['max_week_day']][[datecol,'value']].set_index(datecol)['value']

        return ts
    def monthly_eop(self,ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d','m']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to monthly")

        return ts

    def quarterly_eop(self, ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d','m','q']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to quarterly")

        return ts

    def annual_eop(self, ts):
        freq = self.get_series_frequency(ts)
        return ts
    def weekly_avr(self, ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to weekly")

        if freq == 'd':
            orig_df = pd.DataFrame({'value':ts}).reset_index()
            datecol = orig_df.columns[0]
            orig_df['day'] = orig_df[datecol].apply(lambda x: x.weekday())
            orig_df['week'] = orig_df[datecol].apply(lambda x: x.week)
            orig_df = orig_df.merge(
                orig_df.groupby('week')['day'].max().reset_index().rename(columns={'day': 'max_week_day'}), how='left',
                left_on='week', right_on='week')
            orig_df = orig_df.merge(orig_df.groupby('week')['value'].mean().reset_index().rename(columns={'value':'week_avr_value'}), how='left',left_on='week',right_on='week')
            ts = orig_df.loc[orig_df['day']==orig_df['max_week_day']][[datecol,'week_avr_value']].set_index(datecol)['week_avr_value']

        return ts
    def monthly_avr(self, ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d','m']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to monthly")

        return ts
    def quarterly_avr(self, ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d','m','q']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to quarterly")

        return ts

    def annual_avr(self, ts):
        freq = self.get_series_frequency(ts)
        return ts
    def weekly_sum(self, ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w', 'd']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to weekly")

        if freq == 'd':
            orig_df = pd.DataFrame({'value': ts}).reset_index()
            datecol = orig_df.columns[0]
            orig_df['day'] = orig_df[datecol].apply(lambda x: x.weekday())
            orig_df['week'] = orig_df[datecol].apply(lambda x: x.week)
            orig_df = orig_df.merge(
                orig_df.groupby('week')['day'].max().reset_index().rename(columns={'day': 'max_week_day'}), how='left',
                left_on='week', right_on='week')
            orig_df = orig_df.merge(
                orig_df.groupby('week')['value'].sum().reset_index().rename(columns={'value': 'week_avr_value'}),
                how='left', left_on='week', right_on='week')
            ts = orig_df.loc[orig_df['day'] == orig_df['max_week_day']][[datecol, 'week_avr_value']].set_index(datecol)[
                'week_avr_value']

        return ts
    def monthly_sum(self, ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d','m']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to monthly")

        return ts

    def quarterly_sum(self, ts):
        freq = self.get_series_frequency(ts)
        if freq not in ['w','d','m','q']:
            raise FrequencyException(f"Cannot convert given frequency {freq} to quarterly")

        return ts

    def annual_sum(self, ts):
        freq = self.get_series_frequency(ts)
        return ts
    def unity_transformation(self, ts):

        return ts

    def get_series_frequency(self, ts):
        ts_df = pd.DataFrame({'value': ts}).reset_index()
        datecol = ts_df.columns[0]
        try:
            ts_df[datecol] = ts_df[datecol].apply(lambda x: x.to_pydatetime())
            date_diff_ts = [d.astype('timedelta64[D]') / np.timedelta64(1, 'D') for d in np.diff(ts_df[datecol])]
        except:
            date_diff_ts = [d.days for d in np.diff(ts_df[datecol])]
        ts_df['year'] = ts_df[datecol].apply(lambda x: x.year)
        ts_df['month'] = ts_df[datecol].apply(lambda x: x.month)
        if min(date_diff_ts)<5:
            return 'd'
        elif min(date_diff_ts)<10:
            return 'w'
        elif min(date_diff_ts)<65:
            return 'm'
        elif min(date_diff_ts)<120:
            return 'q'
        elif min(date_diff_ts)>250:
            return 'y'

class normalization_transformations():

    def get_config(self):
        config = {
            'index':self.index_normalization,
            'rate':self.unity_transformation,
            'value':self.unity_transformation,
            'yoy':self.unity_transformation,
            'ytd':self.unity_transformation,
            'pp':self.unity_transformation
        }
        return config
    def index_normalization(self, ts, norm_date, norm_value=100):
        '''
        !!! If norm_date value is null, it should choose other norm_date
        Args:
            ts:
            norm_date:
            norm_value:

        Returns:

        '''

        if pd.isnull(ts[norm_date]):
            norm_ts = ts
        else:
            norm_ts = ts / ts[norm_date] * norm_value

        return norm_ts

    def unity_transformation(self, ts, norm_date):

        return ts
class seasonal_adjustment_transformations():

    def get_config(self):
        config = {
            'sa':self.unity_transformation
        }
        return config
    def unity_transformation(self, ts):

        return ts

class FrequencyException(Exception):
    pass