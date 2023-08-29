import pandas as pd
import numpy as np
import xlrd
from time import time
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
import warnings
import logging
import warnings
warnings.filterwarnings("ignore")

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

        self.transformation_stages = []

        self.model_data = {}


    def get_model_inputs(self, return_method_output = False):
        model_sheet_names = xlrd.open_workbook(self.model_path, on_demand=True).sheet_names()
        inputs_sheet = pd.read_excel(self.model_path, sheet_name='input')
        var_list = pd.read_excel(self.db_path, sheet_name='var_list')
        var_list_columns = [mif.variable] + mif.InputInfoCols
        inputs_sheet = inputs_sheet.merge(var_list[var_list_columns], how='left',left_on=mif.InputInfoCols, right_on=mif.InputInfoCols)
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
        stage_dict = {'stage':'s1'}
        data_dict = {}
        for sheet in self.db_data_sheets:
            try:
                self.raw_model_data_stage1[sheet] = pd.read_excel(self.db_path,sheet_name=sheet).set_index(info.date_column)
                data_dict[sheet] = pd.read_excel(self.db_path,sheet_name=sheet).set_index(info.date_column)
            except:
                raise Exception(f'get_model_data level || There is no date column in sheet {sheet} in file {self.db_path} or it is called incorrectly')
        stage_dict['data'] = data_dict
        self.transformation_stages.append(stage_dict)

        stage_dict = {'stage':'pretransform'}
        data_dict = {}
        for input_sheet in self.model_input_sheets_info.keys():
            current_input = self.model_input_sheets_info.get(input_sheet)

            input_sheet_data_current_state = {}
            for source_sheet in list(current_input[mif.input_sheet].unique()):
                # input_sheet_current_state = pd.DataFrame()
                print(f'get_model_data level || constructing raw input sheet; input sheet is {input_sheet}, source sheet is {source_sheet}')
                input_source_sheet = current_input.loc[current_input[mif.input_sheet]==source_sheet]
                source_sheet_cols_to_select = list(input_source_sheet.loc[~pd.isnull(input_source_sheet[mif.variable])][mif.variable])

                source_sheet_cols = self.raw_model_data_stage1.get(source_sheet).columns
                var_list_absent_cols = list(input_source_sheet.loc[pd.isnull(input_source_sheet[mif.variable])][mif.fname])

                print(f'{len(var_list_absent_cols)} of {len(input_source_sheet)} were not found. These are {var_list_absent_cols}')

                input_sheet_data_current_state[source_sheet] = self.raw_model_data_stage1.get(source_sheet)[source_sheet_cols_to_select]

                for col in var_list_absent_cols:
                    input_sheet_data_current_state[source_sheet][col] = None
            data_dict[input_sheet] = input_sheet_data_current_state
            self.raw_model_data_to_transform[input_sheet] = input_sheet_data_current_state
        stage_dict['data'] = data_dict
        self.transformation_stages.append(stage_dict)
        if return_method_output:
            return self.raw_model_data_to_transform
        else:
            return 0

    def perform_data_tranformation(self, return_method_output = False):
        start = time()
        TC = TrasformationsConfig()
        for transformation in TC.transMethodsDict.keys():
            stage_dict = {'stage':transformation}
            data_dict = {}
            prev_data_dict = self.transformation_stages[-1].get('data')
            method = TC.transMethodsDict.get(transformation).get('method')
            info_cols = TC.transMethodsDict.get(transformation).get('cols')
            change_name = TC.transMethodsDict.get(transformation).get('change_name')
            for input_sheet in prev_data_dict.keys():
                info_table = self.model_input_sheets_info.get(input_sheet)[[mif.fname, mif.variable] + info_cols]
                info_table[mif.variable] = info_table[mif.variable].fillna(info_table[mif.fname])
                info_dict = info_table.set_index(mif.variable).to_dict()
                input_sheet_current_state = {}
                for source_sheet in prev_data_dict.get(input_sheet).keys():
                    input_sheet_current_state[source_sheet] = prev_data_dict.get(input_sheet).get(source_sheet).apply(lambda x: method(x, info_dict))
                data_dict[input_sheet] = input_sheet_current_state
            stage_dict['data'] = data_dict
            self.transformation_stages.append(stage_dict)

        stage_dict = {'stage':'input sheet final join'}
        data_dict = {}
        prev_data_dict = self.transformation_stages[-1].get('data')
        for input_sheet in prev_data_dict.keys():
            input_sheet_current_state = pd.DataFrame()
            for source_sheet in prev_data_dict.get(input_sheet).keys():
                if len(input_sheet_current_state) == 0:
                    input_sheet_current_state = prev_data_dict.get(input_sheet).get(source_sheet)
                else:
                    input_sheet_current_state = input_sheet_current_state.join(prev_data_dict.get(input_sheet).get(source_sheet))
            data_dict[input_sheet] = input_sheet_current_state
        stage_dict['data'] = data_dict
        self.model_data = self.transformation_stages[-1].get('data')
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

