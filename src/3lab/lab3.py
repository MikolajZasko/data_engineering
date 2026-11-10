from pathlib import Path

def save_records(frame, filename):
    frame.to_json(Path(filename), orient="records")

def main():
    # Load parameters, combine/reshape tables and write required outputs.
    # Optional exercises must not be prerequisites for required work.
    pass

if __name__ == "__main__":
    main()