import logging
import sys
import pandas as pd
from pathlib import Path
import yaml
from importlib.resources import files

def package_path():
    return files("ModelManager")

def get_config(filenames):
    pth = Path(package_path())
    result = {}
    try:
        for filename in filenames:
            with open(pth / filename, "r") as application_yaml:
                result.update(yaml.safe_load(application_yaml))
    except FileNotFoundError as e:
        return None

    return result



def setup_logger(logger_name='ModelManager', file_name=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)
    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def get_logger(logger_name, module_name):
    return logging.getLogger(logger_name).getChild(module_name)


def lowercase_except_first(s: str) -> str:
    """
    Convert uppercase letters to lowercase in the input string, except for the first character, which is made uppercase.

    Args:
        s (str): Input string.

    Returns:
        str: String with uppercase letters converted to lowercase, except for the first character, which is made uppercase.
    """
    return s[0].upper() + s[1:].lower()


def clean_name(opf_name: str) -> str:
    opf_name = str(opf_name)
    if opf_name is not None:
        cleaned_name = lowercase_except_first(opf_name)
        cleaned_name = cleaned_name.strip()
        cleaned_name = " ".join(cleaned_name.split())
    else:
        cleaned_name = opf_name
    return cleaned_name




def fill_period(df_annual, new_index):
    """
    Reindex annual period to monthly/weekly based on new index\

    df_annual - table with annual data
    new_index - index with new dates
    """

    df = df_annual.reindex(new_index, method='ffill')
    df.index.name = 'date'
    return df
    # print(df)


# function to transform annual to monthly data
def fill_monthly(df):
    start_date = df.index.min() - pd.DateOffset(month=1) - pd.DateOffset(day=1)
    end_date = df.index.max() + pd.DateOffset(month=12)
    dates = pd.date_range(start_date, end_date, freq='MS')
    dates.name = 'date'
    df = df.reindex(dates, method='ffill')
    return df
    # print(df)


# replace ...  to N/A and 0
def clean_data(df):
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(0)
    return df


def df_to_dict(df_data):
    """
    Convert dataframe with time series into dictionary of TS
    """
    df_dict = {}  # weights_df #need to transform
    for col_names in df_data.columns:
        df_dict[col_names] = df_data.filter(items=[col_names])

    return df_dict


def dict_to_df(df_dict):
    """
    Convert dictionary with items to dataframe series

    """
    # находим самый длинный элемент в словаре
    nlen = len(df_dict)
    сolnames = list(df_dict.keys())
    num_col_len = 0
    df_index_col = 0

    for col_names in df_dict:
        df_col = df_dict[col_names]
        num_col = len(df_col)
        if num_col > num_col_len:
            num_col_len = num_col
            df_index_col = df_col.index

    df_data = pd.DataFrame(columns=сolnames, index=df_index_col)

    for col_names in df_dict:
        df_col = df_dict[col_names]
        df_data[col_names].loc[df_col.index] = df_col[col_names]
    return df_data


def detect_char_encod(prod_data):
    """
    function to detect character encoding
    """
    for ind, str_row in prod_data.iterrows():
        str_enc = chardet.detect(str_row.name_rus)  # .encode()
        print(str_row.name_rus + ': ' + str(str_enc['confidence']))
    # print(str_row.name_rus.)


def detect_delimiter(file_path):
    # Detect the file encoding
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())

    # Read the first few lines of the file to determine the delimiter
    with open(file_path, 'r', encoding=result['encoding']) as f:
        sample = f.read(1024 * 4)  # Read 4 KB of the file as a sample

    # Count the occurrences of different delimiters in the sample
    delimiter_counts = {delimiter: sample.count(delimiter) for delimiter in [',', ';']}

    encode = result['encoding']
    delime = max(delimiter_counts, key=delimiter_counts.get)
    # Return the delimiter with the highest count
    # return max(delimiter_counts, key=delimiter_counts.get)
    return encode, delime


def transform_time_frequency(df, from_freq, to_freq, method):
    """
    Transform time frequencies from daily, weekly, monthly, and quarterly to weekly, monthly,
    quarterly, and annual using different methods.

    Args:
        df (pandas.DataFrame): The DataFrame to transform.
        from_freq (str): The current frequency of the DataFrame, e.g. 'D' for daily, 'W' for weekly,
            'M' for monthly, or 'Q' for quarterly.
        to_freq (str): The desired frequency of the transformed DataFrame, e.g. 'W' for weekly,
            'M' for monthly, 'Q' for quarterly, or 'A' for annual.
        method (str): The transformation method to use, e.g. 'end' for end of the period, 'mean'
            for period average, or 'sum' for period sum.

    Returns:
        pandas.DataFrame: The transformed DataFrame.
    """
    # Convert the DataFrame to the current frequency
    if from_freq != 'D':
        df = df.resample(from_freq).sum()

    # Define a dictionary of transformation methods
    methods = {
        'end': 'last',
        'mean': 'mean',
        'sum': 'sum'
    }

    # Apply the specified transformation method
    if method in methods:
        df = df.resample(to_freq).apply(methods[method])

    # Convert the DataFrame to the desired frequency
    if to_freq == 'A':
        df = df.resample(to_freq).sum()
    else:
        df = df.resample(to_freq).asfreq()

    return df


def count_and_report(logger, total_items: int, existing_items: int, new_items: int):
    logger.info(f"Total items: {total_items}")
    logger.info(f"Existing items: {existing_items}")
    logger.info(f"New items added: {new_items}")

    # logger.info("Total items: " + str(len(new_transactions)))