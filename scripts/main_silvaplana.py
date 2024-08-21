import sys

sys.path.insert(0, './')
if True:
    from src.wind_reader import SilvaplanaReader

SilvaplanaReader().update_db()
