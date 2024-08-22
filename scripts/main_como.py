import sys

sys.path.insert(0, './')
if True:
    from src.como_reader import ComoReader

ComoReader('Dervio').update_db()
# ComoReader('Perledo_Cantone').update_db()
ComoReader('Oliveto_Lario').update_db()

ComoReader('Gera_Lario').update_db()  # 2
'''
ComoReader('Gera_Lario').update_db()  # 2
ComoReader('Pian_di_Spagna').update_db()  # 2
ComoReader('Gravedona').update_db()  # 2
ComoReader('Dongo').update_db()  # 2
ComoReader('Ossuccio').update_db()  # 2
ComoReader('Mandello').update_db()  # 2
ComoReader('Lecco').update_db()  # 2
ComoReader('Garlate').update_db()  # 2
'''
