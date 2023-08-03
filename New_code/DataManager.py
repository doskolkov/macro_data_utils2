import pandas as pd
import numpy as np
import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
import warnings
import logging

from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif
from Utils.information import ModelOutputUnits as mou
from New_code.transformations import TrasformationsConfig


info = info()
class InputHandler():
    def __init__(self, country_code, mode = 'append', src = 'excel'):
        self.db_path = info.get_db_path(info.country_dict.get(country_code))
        self.model_path = info.get_model_path(info.country_dict.get(country_code))

        self.db_input_sheets = []

        self.model_inputs = {}
        self.InputVarsTranformDict = {}

        self.raw_model_data = {}
        self.model_data = {}


    def get_model_inputs(self, return_method_output = False):
        inputs_sheet = pd.read_excel(self.model_path, sheet_name='input')
        output_keys = list(inputs_sheet[mif.output_sheet].unique())
        self.db_input_sheets = list(inputs_sheet[mif.input_sheet].unique())
        self.InputVarsTranformDict = inputs_sheet[mif.InputInstructionCols].set_index(mif.fname).to_dict()
        for k in output_keys:
            self.model_inputs[k] = inputs_sheet.loc[inputs_sheet[mif.output_sheet]==k].reset_index().drop(columns = 'index')
        print(f'Successfully obtained model inputs || input keys are {self.model_inputs.keys()}')


        if return_method_output:
            return self.model_inputs
        else:
            return 0
    def get_model_data(self):
        assert len(self.model_inputs.keys()) > 0, f'get_model_data level ||Model inputs dict has no keys, should contain either subset of {mou.UnitsValueSet}'
        assert len(self.db_input_sheets) > 0, f'get_model_data level || Input sheets list is empty. It must contain either subset of DB sheets list'
        assert len(set.intersection(set(self.model_inputs.keys()),
                                    mou.UnitsValueSet)) > 0, f'get_model_data level || None of Model Data keys, {self.model_inputs.keys} is in {mou.UnitsValueSet}'
        for k in self.model_inputs.keys():
            assert k in mou.UnitsValueSet, f'get_model_data level || Model data input key {k} is not in {mou.UnitsValueSet}'

        db_sheet_names = xlrd.open_workbook(self.db_path, on_demand=True).sheet_names()

        assert len(set.intersection(set(self.db_input_sheets),set(db_sheet_names))) == len(self.db_input_sheets), f'Was not able to find sheets {np.setdiff1d(self.db_input_sheets,db_sheet_names)} in {self.db_path} file'
        for sheet in self.db_input_sheets:
            try:
                self.raw_model_data[sheet] = pd.read_excel(self.db_path,sheet_name=sheet).set_index(info.date_column)
            except:
                raise Exception(f'get_model_data level || There is no date column in sheet {sheet} in file {self.db_path} or it is called incorrectly')
        print(3)

    def perform_data_tranformation(self):
        True

    def put_model_data(self):

        assert len(self.model_data.keys()) > 0, f'put_model_data level || Model data dict has no keys, should contain either subset of {mou.UnitsValueSet}'
        assert len(set.intersection(set(self.model_data.keys()),mou.UnitsValueSet)) > 0, f'put_model_data level || None of Model Data keys, {self.model_data.keys} is in {mou.UnitsValueSet}'
        for k in self.model_data.keys():
            assert k in mou.UnitsValueSet, f'put_model_data level || Model data key {k} is not in {mou.UnitsValueSet}'

