from src import read_winds

import os
from datetime import datetime


def test_date2datetime():
    dt = read_winds.date2datetime("28.07. 14:50", today=datetime(2014, 7, 29))
    assert dt == datetime(year=2014, month=7, day=28, hour=14, minute=50)

    dt = read_winds.date2datetime("31.12. 23:50", today=datetime(2015, 1, 1))
    assert dt == datetime(year=2014, month=12, day=31, hour=23, minute=50)


def test_get_new_winds():
    df = read_winds.WindReader().read_new_winds()
    assert len(df) > 20
    assert len(df.columns) >= 2


def test_append_to_db():
    df = read_winds.WindReader().read_new_winds()
    wReader = read_winds.WindReader()
    wReader.db_dir = "./db_test/"

    # Delete db_test file if it exists
    if os.path.isfile(wReader.db_file):
        os.remove(wReader.db_file)

    # Test adding df to db twice and see if it gets trunked
    wReader.append_to_db(df[:-10])
    wReader.append_to_db(df)
    db = wReader.load_db()
    assert len(df) == len(db)
