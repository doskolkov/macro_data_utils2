import pandas as pd
import numpy as np
import xlrd
from time import time
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

        self.db_data_sheets = []

        self.model_input_sheets_info = {}
        self.InputVarsTranformDict = {}

        self.raw_model_data_stage1 = {}
        self.raw_model_data_to_transform = {}
        self.model_data = {}


    def get_model_inputs(self, return_method_output = False):
        model_sheet_names = xlrd.open_workbook(self.model_path, on_demand=True).sheet_names()
        inputs_sheet = pd.read_excel(self.model_path, sheet_name='input')#.sort_values(by=mif.fname)
        output_keys = list(inputs_sheet[mif.output_sheet].unique())
        self.db_data_sheets = list(inputs_sheet[mif.input_sheet].unique())
        self.InputVarsTranformDict = inputs_sheet[mif.InputInstructionCols].set_index(mif.fname).to_dict()
        for k in output_keys:
            self.model_input_sheets_info[k] = inputs_sheet.loc[inputs_sheet[mif.output_sheet]==k].reset_index().drop(columns = 'index')
        print(f'Successfully obtained model inputs || Model input keys are {self.model_input_sheets_info.keys()}')


        if return_method_output:
            return self.model_input_sheets_info
        else:
            return 0
    def get_model_data(self, return_method_output = False):
        assert len(self.model_input_sheets_info.keys()) > 0, f'get_model_data level || Model inputs dict has no keys, should contain either subset of {mou.UnitsValueSet}'
        assert len(self.db_data_sheets) > 0, f'get_model_data level || Input sheets list is empty. It must contain either subset of DB sheets list'
        assert len(set.intersection(set(self.model_input_sheets_info.keys()),
                                    mou.UnitsValueSet)) > 0, f'get_model_data level || None of Model Data keys, {self.model_inputs.keys} is in {mou.UnitsValueSet}'
        for k in self.model_input_sheets_info.keys():
            assert k in mou.UnitsValueSet, f'get_model_data level || Model data input key {k} is not in {mou.UnitsValueSet}'

        db_sheet_names = xlrd.open_workbook(self.db_path, on_demand=True).sheet_names()

        assert len(set.intersection(set(self.db_data_sheets),set(db_sheet_names))) == len(self.db_data_sheets), f'Was not able to find sheets {np.setdiff1d(self.db_unique_input_sheets,db_sheet_names)} in {self.db_path} file'
        for sheet in self.db_data_sheets:
            try:
                self.raw_model_data_stage1[sheet] = pd.read_excel(self.db_path,sheet_name=sheet).set_index(info.date_column)
            except:
                raise Exception(f'get_model_data level || There is no date column in sheet {sheet} in file {self.db_path} or it is called incorrectly')

        for input_sheet in self.model_input_sheets_info.keys():
            current_input = self.model_input_sheets_info.get(input_sheet)
            input_sheet_current_state = pd.DataFrame()
            for source_sheet in list(current_input[mif.input_sheet].unique()):
                print(f'get_model_data level || constructing raw input sheet; input sheet is {input_sheet}, source sheet is {source_sheet}')
                source_sheet_cols_to_select = list(current_input.loc[current_input[mif.input_sheet]==source_sheet][mif.fname])
                source_sheet_cols = self.raw_model_data_stage1.get(source_sheet).columns
                not_present_source_sheet_cols = np.setdiff1d(source_sheet_cols_to_select, source_sheet_cols)
                print(f'{len(not_present_source_sheet_cols)} of {len(source_sheet_cols_to_select)} were not found. These are {not_present_source_sheet_cols}')
                source_sheet_cols_to_select = list(set(source_sheet_cols_to_select)-set(not_present_source_sheet_cols))
                if len(input_sheet_current_state.columns) == 0:
                    input_sheet_current_state = self.raw_model_data_stage1.get(source_sheet)[source_sheet_cols_to_select]
                else:
                    input_sheet_current_state = input_sheet_current_state.join(self.raw_model_data_stage1.get(source_sheet)[source_sheet_cols_to_select])
                for col in not_present_source_sheet_cols:
                    input_sheet_current_state[col] = None
            self.raw_model_data_to_transform[input_sheet] = input_sheet_current_state

        if return_method_output:
            return self.raw_model_data_to_transform
        else:
            return 0

    def perform_data_tranformation(self, return_method_output = False):
        start = time()
        TC = TrasformationsConfig()
        for transformation in TC.transMethodsDict.keys():
            method = TC.transMethodsDict.get(transformation).get('method')
            info_cols = TC.transMethodsDict.get(transformation).get('cols')
            for input_sheet in self.raw_model_data_to_transform.keys():
                info_table = self.model_input_sheets_info.get(input_sheet)[[mif.fname]+info_cols]
                info_dict = info_table.set_index(mif.fname).to_dict()
                self.model_data[input_sheet] = self.raw_model_data_to_transform.get(input_sheet).apply(lambda x: method(x, info_dict))
        end = time()
        all_time = end-start

        if return_method_output:
            return self.model_data
        else:
            return 0



    def put_model_data(self):

        assert len(self.model_data.keys()) > 0, f'put_model_data level || Model data dict has no keys, should contain either subset of {mou.UnitsValueSet}'
        assert len(set.intersection(set(self.model_data.keys()),mou.UnitsValueSet)) > 0, f'put_model_data level || None of Model Data keys, {self.model_data.keys} is in {mou.UnitsValueSet}'
        for k in self.model_data.keys():
            assert k in mou.UnitsValueSet, f'put_model_data level || Model data key {k} is not in {mou.UnitsValueSet}'

