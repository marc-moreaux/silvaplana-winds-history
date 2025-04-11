from src import como_reader
import os


def test_main():
    wReader = como_reader.ComoReader('Dervio')
    wReader.db_dir = "./db_test/"
    df = wReader.read_new_winds()

    # Delete db_test file if it exists
    if os.path.isfile(wReader.db_file):
        os.remove(wReader.db_file)

    # Test adding df to db twice and see if it gets trunked
    wReader.append_to_db(df[:-10])
    wReader.append_to_db(df)
    db = wReader.load_db()
    assert len(df) == len(db)


def test_all_cities():
    '''Test extracting cities one after the other
    '''
    cities = como_reader.parameters.keys()
    for city in cities:
        print(f'trying to get data from {city}')
        wReader = como_reader.ComoReader(city)
        wReader.db_dir = "./db_test/"
        df = wReader.read_new_winds()
        wReader.append_to_db(df)
