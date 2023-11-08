from .Utils import setup_logger, get_config
from .ExcelUtils import DataExcel
from .DBManagerExcel import DBManagerExcel
from .DBManagerSQL import DBManagerSQL
from .VariableManager import Variable


class ModelManager(DataExcel):
    """

    Class to manage model updates - top level:
    - read file with settings
    - read Model excel file with instructions
    - determine data sources
    - initiate ExcelDBManager ans SqlDBManager

    """
    model_path = ""
    config_files = ["config.yaml"]

    database_sources = []
    db_data_sheets = []
    model_input_sheets_info = {}
    InputVarsTranformDict = {}
    raw_model_data_stage1 = {}
    raw_model_data_to_transform = {}
    transformation_stages = []
    model_data = {}

    def __init__(self, model_path):
        """
        Load model settings

        Args:
            model_path:
        """
        self.model_path = model_path
        self.logex = setup_logger('Model', 'data.log')

        # Load model settings
        info_settings = get_config(self.config_files)
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))

        self.model_fields = info_settings['ModelInfoFields']
        self.dsi = self.model_fields['DataSourceInfoFields']
        self.rdli = self.model_fields['RawDataLocationInfoFields']
        self.ti = self.model_fields['TransformationInstructionFields']

        self.config = info_settings['ModelInputInfoFields']

        self.config_output = info_settings['ModelOutputUnits']
        self.UnitsValueSet = set([self.config_output['m'],
                                  self.config_output['msa'],
                                  self.config_output['q'],
                                  self.config_output['qsa'],
                                  self.config_output['d'],
                                  self.config_output['a'],
                                  self.config_output['w']])
        self.SourceTypeManagerMap = {
            'RE_INT_DB':DBManagerExcel,
            'SQL':DBManagerSQL
        }

        self.database_sources = {}
        self.variables = []
        self.properly_defined_variables = []
        self.undefined_variables_with_ts = []
        self.undefined_variables = []

    # def _package_path(self):
    #     return files("ModelManager")
    def initialize_model_schema(self):
        inputs_sheet = self.load_excel(self.model_path, 'input')
        var_list_columns = self.InputInfoCols
        for source_type in inputs_sheet[self.dsi['sourcetype']].unique():
            self.database_sources[source_type] = {}
            source_type_part = inputs_sheet.loc[inputs_sheet[self.dsi['sourcetype']] == source_type]
            for source in source_type_part[self.dsi['source']].unique():
                self.database_sources[source_type][source] = {}
                source_part = source_type_part.loc[source_type_part[self.dsi['source']] == source]
                for input_file in source_part[self.dsi['input_file']].unique():
                    self.database_sources[source_type][source][input_file] = {}
                    input_file_part = source_part.loc[source_part[self.dsi['input_file']] == input_file]
                    for input_sheet in input_file_part[self.dsi['input_sheet']].unique():
                        self.database_sources[source_type][source][input_file][
                            input_sheet] = self.SourceTypeManagerMap.get(source_type)(source, input_file, input_sheet)
                        input_sheet_part = input_file_part.loc[input_file_part[self.dsi['input_sheet']]==input_sheet]
                        for variable_fname in input_sheet_part[self.rdli['fname']].unique():
                            fname_part = input_sheet_part.loc[input_sheet_part[self.rdli['fname']]==variable_fname]
                            for is_real in fname_part[self.rdli['is_real']].unique():
                                is_real_part = fname_part.loc[fname_part[self.rdli['is_real']]==is_real]
                                for is_sa in is_real_part[self.rdli['is_sa']].unique():
                                    is_sa_part = is_real_part.loc[is_real_part[self.rdli['is_sa']]==is_sa]
                                    variable_info = {
                                        self.rdli['fname']:variable_fname,
                                        self.rdli['is_real']:is_real,
                                        self.rdli['is_sa']:is_sa
                                    }
                                    datasource_info = {
                                        self.dsi['source_type']: source_type,
                                        self.dsi['source']: source,
                                        self.dsi['input_file']: input_file,
                                        self.dsi['input_sheet']: input_sheet
                                    }
                                    destinations = []
                                    for destination_row in is_sa_part.iterrows():
                                        destination = {}
                                        for col in self.ti.keys():
                                            destination[col] = destination_row[col]
                                        destinations.append(destination)
                                    self.variables.append(Variable(
                                        variable_info=variable_info,
                                        datasource_info=datasource_info,
                                        dataloader_instance=self.database_sources[source_type][source][input_file][input_sheet],
                                        destinations=destinations
                                    ))

    def define_variables(self, date_from = None, date_till = None):
        for variable in self.variables:
            variable.define(date_from=date_from,date_till=date_till)
            if variable.raw_data_obtained and variable.raw_data_properties_defined:
                self.properly_defined_variables.append(variable)
            elif variable.raw_data_obtained:
                self.undefined_variables_with_ts.append(variable)
            else:
                self.undefined_variables.append(variable)

    def transform_variables(self):
        pass
    def put_variables(self):
        pass
    def assert_model_integrity(self):
        pass

