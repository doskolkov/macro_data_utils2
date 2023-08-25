import pandas as pd
import numpy as np

from New_code.DataManager import InputHandler
from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif
from Utils.information import ModelOutputUnits as mou

from New_code.TimeSeriesTransformations import type_transformations, normalization_transformations

import warnings
import random
warnings.filterwarnings("ignore")

import datetime
from datetime import timedelta
from dateutil.relativedelta import *

random.seed(20)
rand_indexes = [random.randint(1,361) for t in range(1,51,1)]

sd = datetime.datetime(1997,4,1)
nd = datetime.datetime(1998,6,1)
dates = [sd]
init_val = 1
vals = [init_val]
for t in range(1, 360, 1):
    dates.append(sd+relativedelta(months=+1*t))
    vals.append(vals[-1]*(1+0.005))
for t in rand_indexes:
    vals[t] = np.nan
sample_ts = pd.DataFrame({'dates': dates, 'vals': vals}).set_index('dates')['vals']
null_ts = sample_ts.apply(lambda x: np.nan)
instance_dict = {
    'type':type_transformations(),
    'norm':normalization_transformations()
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
    return res, null_res
# test_transform_method(sample_ts)

# res, null_res = test_transform_method(sample_ts, null_ts, 'norm','index', norm_date=nd)
# test_result = pd.DataFrame({'sample':sample_ts,'sample_res':res,'null':null_ts,'null_res':null_res})

IH = InputHandler('kzt')
IH.get_model_inputs()
IH.get_model_data()
IH.perform_data_tranformation()
IH.put_model_data()