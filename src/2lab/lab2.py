from pathlib import Path
import pandas as pd
import numpy as np
import pickle
import pandas.api.types as ptypes
import json
from enum import Enum
from pandas.api.types import CategoricalDtype

# Create a random number generator
rng = np.random.default_rng()

def execute_in_script_folder():
    if "__file__" in globals():
        # Running as a standalone .py script
        return Path(__file__).resolve().parent
    else:
        # Running inside a Jupyter Notebook or interactive shell
        return Path.cwd()

def save_pkl_file(filename : str, df):

    file_path = execute_in_script_folder() / filename

    with open(file_path, "wb") as file:
        pickle.dump(df, file)

def save_json_file(filename, df):
    
    file_path = execute_in_script_folder() / filename

    with open(file_path, "w", encoding='uft-8') as file:
        json.dump(df,file,indent=4)

def save_csv_file(filename, frame, *, index=False):
    frame.to_csv(Path(filename), index=index)

def read_txt_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

file_path = execute_in_script_folder()

def write_record(record, filename):
    Path(filename).write_text(json.dumps(record, allow_nan=False), encoding="utf-8")

def main():
    # task 1
    df = pd.read_csv('lab2_ex01.csv', sep=";", decimal=",")

    save_csv_file("lab2_ex01_df.pkl", df)

    # task 2
    df1 = df.copy(True)

    filename = "lab2_ex02.txt"
    txt_contents = read_txt_file(filename)

    txt_list = [line.strip() for line in txt_contents.split("\n") if line.strip()]
    txt_dict = {val: index for index, val in enumerate(txt_list,start=1)}

    filename = "lab2_ex02_scale.pkl"

    save_pkl_file(filename, df1)

    # modify the vals
    col_name = "rating_767"

    for key, val in txt_dict.items():
        df1[col_name] = df1[col_name].replace(txt_dict)

    # task 3
    df2 = df.copy(True)

    custom_cat_type = CategoricalDtype(categories=txt_list, ordered=False)

    df2[col_name] = df2[col_name].astype(custom_cat_type)
    
    filename = "lab2_ex03_categories.pkl"

    save_pkl_file(filename, df2)

    # task 4
    df3 = df.copy(True)

    non_numeric_cols = df3.select_dtypes(exclude=['number'])

    # Find which columns contain at least one digit anywhere inside them
    mask = non_numeric_cols.apply(lambda col: col.str.contains(r'\d', na=False).any())

    # Keep only those specific columns
    filtered_df3 = non_numeric_cols.loc[:, mask]

    #
    #  \ - line break instead of a huge () ???
    #   cool functions: rename(), map() / mapper() ???
    #

    save_pkl_file("lab2_ex04_numbers.pkl", filtered_df3)

    # task 5 - skipped 4 to match task with dataframe naming
    df5 = df.copy(True)

    df5 = df5.select_dtypes(exclude="number")
        
    df5_unique_cols = df5.nunique()

    df5_unique_cols = df5_unique_cols[df5_unique_cols > 10]

    df5 = df5.drop(columns=df5_unique_cols.index)

    filtered_df = df5[df5.apply(lambda col: col.str.fullmatch(r'[a-z]+', na=False)).all(axis=1)]

    no_txt_match = filtered_df.apply(lambda col: not col.dropna().isin(txt_list).any())
    filtered_df = filtered_df[filtered_df.columns[no_txt_match]]

    for i, col_name in enumerate(df5.columns, start=1):
        # One-hot encode with boolean values and no prefixes
        dummies = pd.get_dummies(df5[col_name], prefix='', prefix_sep='', dtype=bool)
        
        # Save to the required file naming format
        filename = f"lab2_ex05_col{i}.pkl"
        dummies.to_pickle(filename)


if __name__ == "__main__":
    main()