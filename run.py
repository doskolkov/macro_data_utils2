import pandas as pd

from New_code.DataManager import InputHandler
from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif
from Utils.information import ModelOutputUnits as mou

from New_code.TimeSeriesTransformations import type_transformations

import warnings
warnings.filterwarnings("ignore")

import datetime
from datetime import timedelta
from dateutil.relativedelta import *
sd = datetime.datetime(1997,4,1)
# nd = datetime.datetime(2000,1,1)
# dates = [sd]
# init_val = 1
# vals = [init_val]
# for t in range(1, 350, 1):
#     dates.append(sd+relativedelta(months=+1*t))
#     vals.append(vals[-1]*(1+0.005))
# sample_ts = pd.DataFrame({'dates': dates, 'vals': vals}).set_index('dates')['vals']
#
# tt = type_transformations()
# ttconfig = tt.get_config()
#
# res = ttconfig.get('pp')(sample_ts)

IH = InputHandler('kzt')
IH.get_model_inputs()
IH.get_model_data()
IH.perform_data_tranformation()