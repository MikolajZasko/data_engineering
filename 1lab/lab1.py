from pathlib import Path
import pandas as pd

def save_csv(frame, filename, *, index=False):
    frame.to_csv(Path(filename), index=index)

def main():

    # task 1.1
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    column_names = alphabet + alphabet.upper()

    df_letters_list 

    # Load inputs, implement each transformation, then write required outputs.
    pass

if __name__ == "__main__":
    main()