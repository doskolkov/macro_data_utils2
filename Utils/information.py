class INFO():
    EXCEL_FOLDER = "Excel_Folder"
    EXCEL_DB_MANAGER = "ExcelDBManager"
    FILE_MANAGE = "FileManage"
    MODEL_MANAGE = "ModelManage"

    date_column = "date"

    country_dict = {
        'kzt':'Kazakhstan',
        'rus':'Russia',
        'bel':'Belarus'
    }

    def get_db_path(self, ctry):
        return f"""{ctry}_DB.xlsx"""

    def get_model_path(self, ctry):
        return f"""{ctry}_Model2.xlsm"""

    DB_PATH = f'{EXCEL_FOLDER}\Kazakhstan_DB.xlsx'
    MODEL_PATH = f'{EXCEL_FOLDER}\Kazakhstan_Model2.xlsm'

class ModelInputInfoFields():
    country = "country"
    source = "source"
    stype = "source_type"
    input_file ="input_file"
    input_sheet = "input_sheet"
    fname = "name"
    is_real = "real"
    is_sa = "sa"
    transf = "transf"
    calc = "calc"
    is_makesa = "makesa"
    freq = "freq"
    ds = "start"
    de = "end"
    norm_d = "norm"
    output_sheet = "output_sheet"

    InputInstructionCols = [fname,input_sheet,output_sheet,is_real,is_sa,transf,calc,is_makesa,freq,ds,de,norm_d]

class ModelOutputUnits():
    m = "monthly"
    msa = "monthly_sa"
    q = "quarterly"
    qsa = "quarterly_sa"
    d = "daily"
    a = "annualy"
    w = "weekly"

    UnitsValueSet = set([m, msa, q, qsa, d, a, w])
