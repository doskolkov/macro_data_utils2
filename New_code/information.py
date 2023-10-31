import yaml


class INFO:
    """

    """
    config = None

    def __init__(self):
        # Load the YAML configuration
        with open('../Utils/config.yaml', 'r') as file:
            info = yaml.safe_load(file)
            self.config = info['INFO']

    def get_db_path(self, ctry):
        country_name = self.config['country_dict'][ctry]
        return f"{country_name}_DB.xlsx"

    def get_model_path(self, ctry):
        country_name = self.config['country_dict'][ctry]
        return f"{country_name}_Model.xlsm"


class ModelInputInfoFields:
    """

    """
    config = None

    def __init__(self):
        # Load the YAML configuration
        with open('../Utils/config.yaml', 'r') as file:
            info = yaml.safe_load(file)
            self.config = info['ModelInputInfoFields']

        self.InputInfoCols = [self.config['fname'], self.config['is_real'], self.config['is_sa']]
        self.InputInstructionCols = [self.config['fname'],
                                     self.config['input_sheet'],
                                     self.config['output_sheet'],
                                     self.config['is_real'],
                                     self.config['is_sa'],
                                     self.config['transf'],
                                     self.config['calc'],
                                     self.config['is_makesa'],
                                     self.config['freq'],
                                     self.config['ds'],
                                     self.config['de'],
                                     self.config['norm_d']
                                     ]


class ModelOutputUnits:
    """

    """
    config = None

    def __init__(self):
        # Load the YAML configuration
        with open('../Utils/config.yaml', 'r') as file:
            info = yaml.safe_load(file)
            self.config = info['ModelOutputUnits']

        self.UnitsValueSet = set([self.config['m'],
                                  self.config['msa'],
                                  self.config['q'],
                                  self.config['qsa'],
                                  self.config['d'],
                                  self.config['a'],
                                  self.config['w']])

# Example usage:
# country_code = 'kzt'

# print(get_db_path(country_code))    # Outputs: "Kazakhstan_DB.xlsx"
# print(get_model_path(country_code)) # Outputs: "Kazakhstan_Model2.xlsm"


class INFO_old():
    EXCEL_FOLDER = "Excel_Folder"
    EXCEL_DB_MANAGER = "ExcelDBManager"
    FILE_MANAGE = "FileManage"
    MODEL_MANAGE = "ModelManage"

    date_column = "date"

    country_dict = {
        'kzt': 'Kazakhstan',
        'rus': 'Russia',
        'bel': 'Belarus'
    }

    def get_db_path(self, ctry):
        return f"""{ctry}_DB.xlsx"""

    def get_model_path(self, ctry):
        return f"""{ctry}_Model2.xlsm"""

    DB_PATH = f'{EXCEL_FOLDER}\Kazakhstan_DB.xlsx'
    MODEL_PATH = f'{EXCEL_FOLDER}\Kazakhstan_Model2.xlsm'

    country = "country"
    source = "source"
    sourcetype = "source_type"
    input_file = "input_file"
    input_sheet = "input_sheet"
    fname = "name"
    is_real = "real"
    is_sa = "sa"
    transf = "transf"
    stype = "type"
    calc = "calc"
    is_makesa = "makesa"
    freq = "freq"
    ds = "start"
    de = "end"
    norm_d = "norm"
    output_sheet = "output_sheet"
    variable = "variable"

    m = "monthly"
    msa = "monthly_sa"
    q = "quarterly"
    qsa = "quarterly_sa"
    d = "daily"
    a = "annualy"
    w = "weekly"
