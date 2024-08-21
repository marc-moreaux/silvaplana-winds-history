import sys

sys.path.insert(0, './')
if True:
    from src.como_reader import ComoReader

ComoReader('Dervio').update_db()
