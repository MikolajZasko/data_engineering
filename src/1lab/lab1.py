from pathlib import Path
import pandas as pd
import numpy as np
import pickle
import pandas.api.types as ptypes
import json

def save_csv(frame, filename, *, index=False):
    frame.to_csv(Path(filename), index=index)

# Create a random number generator
rng = np.random.default_rng()

def execute_in_script_folder():
    # Get the folder where this exact .py script is located
    script_dir = Path(__file__).resolve().parent

    # Build an absolute path to your file relative to the script
    return script_dir / "lab1_ex03_stats.json"

file_path = execute_in_script_folder()

def main():

    # task 1.1
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    column_names = alphabet + alphabet.upper()

    data_frame_contents = {}

    for letter in column_names:

        # Generate an array of 1,000 random values
        values = rng.normal(loc=21, scale=37, size=100)

        data_frame_contents[letter] = values

    df = pd.DataFrame(data_frame_contents)

    letters_df = df

    # task 1.2
    rows_amount = 100
    all_states = ['CA', 'TX', 'NY', 'FL', 'IL']
    # all_years = [x for x in range(2000, 2025)]

    evens = [x for x in range(100,-100, -2)]

    # pick random values
    random_states = rng.choice(all_states, size=rows_amount)
    random_years = rng.integers(2000, 2025, size=rows_amount)
    random_vals = rng.normal(loc=100, scale=20, size=rows_amount)

    df = pd.DataFrame({
    'even': evens,
    'state': random_states,
    'year': random_years,
    'val': random_vals
    })
    df = df.set_index('even')

    states_df = df

    with open("lab1_ex01_letters.pkl", "wb") as file:
        pickle.dump(letters_df, file)

    with open("lab1_ex01_states.pkl", "wb") as file:
        pickle.dump(states_df, file)

    # task 2
    df = pd.read_csv('lab1_ex02.csv')
    missing_vals = df.isnull().sum()

    csv_metadata = []

    row_amount = len(df)

    for key, val in missing_vals.items():
        

        col_data = {
            "name": key,
            "missing": val/row_amount
        }

        if ptypes.is_integer_dtype(df[key]):
            col_data["type"] = "int"
        elif ptypes.is_float_dtype(df[key]):
            col_data["type"] = "float"
        else:
            col_data["type"] = "other"

        csv_metadata.append(col_data)

    with open("lab1_ex02_fields.json", "w", encoding='utf-8') as f:
        json.dump(csv_metadata,f, indent=4)

    # task 3
    summary_all = df.describe(include='all')
    raw_dict = summary_all.to_dict()

    summary_formatted = {}
    for col, stats in raw_dict.items():
        summary_formatted[col] = {
            k: v for k, v in stats.items() if pd.notna(v)
        }

    with open("lab1_ex03_stats.json", "w", encoding='utf-8') as f:
        json.dump(summary_formatted, f, indent=4)


    # task 4
    df.columns = (
        df.columns.str.lower()
        .str.replace(r"[^a-z0-9_ ]", "", regex=True)
        .str.replace(" ", "_")
    )

    df.index.name = "id"

    save_csv(df,"lab1_ex04_columns.csv")

if __name__ == "__main__":
    main()