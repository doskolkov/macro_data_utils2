import logging
import sys
from fuzzywuzzy import fuzz, process
import pandas as pd
import chardet
from typing import List, Tuple
import nltk
import json
import datetime


# Ensure NLTK's Punkt Sentence Tokenizer is installed
nltk.download('punkt', quiet=True)

def break_text_into_sentences(text):
    # Use NLTK's sent_tokenize function to split the text into sentences
    sentences = nltk.sent_tokenize(text)

    formatted_text = ""
    for i, sentence in enumerate(sentences, 1):
        formatted_text += f"{i}. {sentence}\n"

    return formatted_text


def break_text_into_sentences2(text):
    #nltk.download('punkt', quiet=True)
    sentences = nltk.sent_tokenize(text)
    sentences_list = [f"{sentence}" for i, sentence in enumerate(sentences, 1)]
    return sentences_list


def break_text_into_sentences_df(text, output_json_file=None):
    # Ensure NLTK's Punkt Sentence Tokenizer is installed
    # nltk.download('punkt', quiet=True)

    # Use NLTK's sent_tokenize function to split the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Create a dictionary with sentence numbers and sentences
    sentence_dict = {f" {i}": sentence for i, sentence in enumerate(sentences, 1)}

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(list(sentence_dict.items()), columns=['number', 'sentence'])

    # Save as JSON file if filename is provided
    if output_json_file is not None:
        with open(output_json_file, 'w') as f:
            json.dump(sentence_dict, f)

    return df


def break_text_into_paragraphs(text, output_json_file=None):
    # Use str.split function to break the text into paragraphs
    paragraphs = [paragraph.strip() for paragraph in text.split('\n') if paragraph.strip()]

    # Create a dictionary with paragraph numbers and paragraphs
    paragraph_dict = {f"{i}": paragraph for i, paragraph in enumerate(paragraphs, 1)}

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(list(paragraph_dict.items()), columns=['number', 'paragraph'])

    # Save as JSON file if filename is provided
    if output_json_file is not None:
        with open(output_json_file, 'w') as f:
            json.dump(paragraph_dict, f)

    return df

# Test the function
# text = "Hello world! This is a test. What do you think? Is it working well?"
# print(break_text_into_sentences(text))

# APP_LOGGER_NAME = 'DataManage'

def setup_logger(logger_name='DataManage', file_name=None):
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


def clean_name_column(opf_name_column: pd.Series) -> pd.Series:
    cleaned_name_column = opf_name_column.apply(lowercase_except_first)
    cleaned_name_column = cleaned_name_column.str.strip()
    cleaned_name_column = cleaned_name_column.str.split().str.join(' ')
    return cleaned_name_column


# compare two dataframes
def compare_fuzzy(df_1, col_name_1, df_2, col_name_2, threshold=80):
    """
    find closest matches from df_1 in df_2
    sources: https://www.geeksforgeeks.org/how-to-do-fuzzy-matching-on-pandas-dataframe-column-using-python/

    df_1  - first data frame
    col_name_1 - column name from df_1
    df_2
    """
    # empty lists for storing the matches
    # later
    mat1 = []
    mat2 = []
    p = []
    score = []
    score_p = []

    # converting dataframe column to
    # list of elements
    # to do fuzzy matching
    list1 = df_1[col_name_1].tolist()
    list2 = df_2[col_name_2].tolist()

    # taking the threshold as 80
    # threshold = 80

    # iterating through list1 to extract
    # it's closest match from list2
    for i in list1:
        # need some protections from int/floating
        mat1.append(process.extractOne(str(i), list2, scorer=fuzz.token_sort_ratio))

    df_1['matches'] = mat1

    # iterating through the closest matches
    # to filter out the maximum closest match
    for j in df_1['matches']:
        if j[1] >= threshold:
            p.append(str(j[0]))
            score_p.append(str(j[1]))
        mat2.append(",".join(p))
        score.append(",".join(score_p))
        p = []
        score_p = []
    # storing the resultant matches back
    # to dframe1
    df_1['matches'] = mat2
    df_1['scores'] = score
    # df_1['scores']  = df_1['scores'].str.replace('', '0')
    # df_1['scores']  = df_1['scores'].astype('Int64')
    return df_1


def compare_fuzzy_list(list1: List[str], list2: List[str], threshold: int = 80) -> dict:
    """
    Find closest matches from list1 in list2 using fuzzy matching.

    Args:
        list1 (List[str]): First list of strings.
        list2 (List[str]): Second list of strings.
        threshold (int, optional): Threshold for match scoring, default is 80.

    Returns:
        dict: Dictionary with the input strings and their closest matches.
    """

    matches = {}
    for opf_name in list1:
        match, score = process.extractOne(opf_name, list2, scorer=fuzz.token_sort_ratio)
        if score >= threshold:
            matches[opf_name] = match
        else:
            matches[opf_name] = None

    return matches


def compare_fuzzy2(df_1: pd.DataFrame, col_name_1: str, df_2: pd.DataFrame, col_name_2: str,
                   threshold: int = 80) -> pd.DataFrame:
    """
    Find closest matches from df_1 in df_2 using fuzzy matching.

    Args:
        df_1 (pd.DataFrame): First data frame.
        col_name_1 (str): Column name from df_1.
        df_2 (pd.DataFrame): Second data frame.
        col_name_2 (str): Column name from df_2.
        threshold (int, optional): Threshold for match scoring, default is 80.

    Returns:
        pd.DataFrame: DataFrame with the matches and scores appended as columns.
    """

    list1 = df_1[col_name_1].astype(str).tolist()
    list2 = df_2[col_name_2].astype(str).tolist()

    mat1 = [process.extractOne(i, list2, scorer=fuzz.token_sort_ratio) for i in list1]

    df_1['matches'] = mat1

    mat2 = [",".join(str(j[0]) for j in mat1 if j[1] >= threshold)]
    score = [",".join(str(j[1]) for j in mat1 if j[1] >= threshold)]

    df_1['matches'] = mat2
    df_1['scores'] = score

    return df_1


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


class DataLog:
    # define files and path names
    # debug and error information
    DEBUG_PRINT_FL = True
    error_status = False
    msg_text = dict()
    msg_full_text = dict()

    def __init__(self):
        self.error_text = None

    def add_error(self, error_status=True, error_text="", func_name=""):
        self.error_status = error_status
        self.error_text = error_text
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S DD.MM.YYYY")
        error_full_text = current_time + ""

    def add_msg(self, error_status=True, error_text=None):
        """

        """
        # self.__class__.__name__
        pass
