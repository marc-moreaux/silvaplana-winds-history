from src import wind_reader

import os
from datetime import datetime


def test_date2datetime():
    dt = wind_reader.date2datetime("28.07. 14:50", today=datetime(2014, 7, 29))
    assert dt == '2014-07-28 14:50:00'

    dt = wind_reader.date2datetime("31.12. 23:50", today=datetime(2015, 1, 1))
    assert dt == '2014-12-31 23:50:00'


def test_get_new_winds():
    df = wind_reader.SilvaplanaReader().read_new_winds()
    assert len(df) > 15
    assert len(df.columns) >= 2


def test_append_to_db():
    df = wind_reader.SilvaplanaReader().read_new_winds()
    wReader = wind_reader.SilvaplanaReader()
    wReader.db_dir = "./db_test/"

    # Delete db_test file if it exists
    if os.path.isfile(wReader.db_file):
        os.remove(wReader.db_file)

    # Test adding df to db twice and see if it gets trunked
    wReader.append_to_db(df[:-10])
    wReader.append_to_db(df)
    db = wReader.load_db()
    assert len(df) == len(db)
