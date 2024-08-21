from src import como_reader
import os


def test_main():
    df = como_reader.ComoReader().read_new_winds()
    wReader = como_reader.ComoReader()
    wReader.db_dir = "./db_test/"

    # Delete db_test file if it exists
    if os.path.isfile(wReader.db_file):
        os.remove(wReader.db_file)

    # Test adding df to db twice and see if it gets trunked
    wReader.append_to_db(df[:-10])
    wReader.append_to_db(df)
    db = wReader.load_db()
    assert len(df) == len(db)
