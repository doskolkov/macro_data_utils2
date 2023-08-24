from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif

class type_transformations():

    def get_config(self):
        config = {
            'index': self.series_to_index,
            'rate': self.series_to_rate,
            'value': self.value_to_value,
            'index_to_rate': self.index_to_rate
        }
        return config
    def series_to_index(self, ts):
        ts*=1
        return ts
    def series_to_rate(self, ts):
        ts *= 1
        return ts
    def value_to_value(self, ts):
        ts *= 1
        return ts
    def index_to_rate(self, ts):
        ts *= 1
        return ts

class frequency_transformations():
    def get_config(self):
        config = {}

class normalization_transformations():

    def get_config(self):
        config = {}

class seasonal_adjustment_transformations():

    def get_config(self):
        config = {}