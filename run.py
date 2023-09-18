import pandas as pd
import numpy as np

from New_code.DataManager import InputHandler
from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif
from Utils.information import ModelOutputUnits as mou

from New_code.TimeSeriesTransformations import type_transformations, normalization_transformations, frequency_transformations
from New_code.TimeSeriesTransformations import FrequencyException

import warnings
import random
warnings.filterwarnings("ignore")

import datetime
from datetime import timedelta
from dateutil.relativedelta import *

random.seed(20)
rand_indexes = [random.randint(1,361) for t in range(1,51,1)]

sd = datetime.datetime(1996,12,31)
nd = datetime.datetime(1998,12,31)
dates = [sd]
init_val = 1
vals = [init_val]
for t in range(1, 360, 1):
    dates.append(sd+relativedelta(months=+1*t))
    # dates = [datetime.datetime.fromtimestamp(d) for d in dates]
    vals.append(vals[-1]*(1+0.005))
for t in rand_indexes:
    vals[t] = None
sample_ts = pd.DataFrame({'dates': dates, 'vals': vals}).set_index('dates')['vals']
null_ts = sample_ts.apply(lambda x: None)


month_ts = sample_ts
null_month_ts = null_ts

vals = [init_val]
dates = [sd]
for t in range(1, 900,1):
    dates.append(sd+relativedelta(days=+1*t))
    # dates = [datetime.datetime.fromtimestamp(d) for d in dates]
    vals.append(vals[-1]*(1+0.005))
for t in rand_indexes:
    vals[t] = None
day_ts = pd.DataFrame({'dates': dates, 'vals': vals}).set_index('dates')['vals']
null_day_ts = day_ts.apply(lambda x: None)

vals = [init_val]
dates = [sd]
for t in range(1, 360,1):
    dates.append(sd+relativedelta(weeks=+1*t))
    # dates = [datetime.datetime.fromtimestamp(d) for d in dates]
    vals.append(vals[-1]*(1+0.005))
for t in rand_indexes:
    vals[t] = None
week_ts = pd.DataFrame({'dates': dates, 'vals': vals}).set_index('dates')['vals']
null_week_ts = week_ts.apply(lambda x: None)

vals = [init_val]
dates = [sd]
for t in range(1, 360,1):
    dates.append(sd+relativedelta(months=+3*t))
    # dates = [datetime.datetime.fromtimestamp(d) for d in dates]
    vals.append(vals[-1]*(1+0.005))
for t in rand_indexes:
    vals[t] = None
quart_ts = pd.DataFrame({'dates': dates, 'vals': vals}).set_index('dates')['vals']
null_quart_ts = quart_ts.apply(lambda x: None)

vals = [init_val]
dates = [sd]
for t in range(1, 360,1):
    dates.append(sd+relativedelta(years=+1*t))
    vals.append(vals[-1]*(1+0.005))
for t in rand_indexes:
    vals[t] = None
year_ts = pd.DataFrame({'dates': dates, 'vals': vals}).set_index('dates')['vals']
null_year_ts = year_ts.apply(lambda x: None)

instance_dict = {
    'type':type_transformations(),
    'norm':normalization_transformations(),
    'freq':frequency_transformations()
}

def test_transform_method(sample_ts,null_ts,instance,method, norm_date = None):

    config = instance_dict.get(instance).get_config()
    ap_method = config.get(method)
    if instance == 'type':
        res = ap_method(sample_ts)
        null_res = ap_method(null_ts)
    elif instance == 'norm':
        res = ap_method(sample_ts, norm_date)
        null_res = ap_method(null_ts, norm_date)
    elif instance == 'freq':
        res = ap_method(sample_ts)
        null_res = ap_method(null_ts)
    return res, null_res
# test_transform_method(sample_ts)
# res = instance_dict.get('freq').get_series_frequency(day_ts)
# res, null_res = test_transform_method(sample_ts, null_ts, 'freq','index', norm_date=nd)
# ft_key = "weekly_sum"
# res, null_res = test_transform_method(day_ts, null_day_ts, instance='freq', method = ft_key)
#
# test_result = pd.DataFrame({'sample':day_ts,'sample_res':res,'null':null_day_ts,'null_res':null_res})

IH = InputHandler('kzt')
IH.get_model_inputs()
IH.get_model_data()
IH.perform_data_transformation()
IH.put_model_data()