#!/usr/bin/env python
#-*-coding:utf-8-*-
import sqlite3

def table2list(table_tsv):
    with open(table_tsv,'r',encoding='utf-16') as tsv:
        code_list = []
        for line in tsv:
            line_stripped = line.strip()
            code_char_mapping = tuple(line_stripped.split())

            code_list.append(code_char_mapping)
    return code_list


def list2sqlite(code_list):

    db = sqlite3.connect('table_db.sqlite')
    c = db.cursor()

    c.execute('''CREATE TABLE ime
    (code text, char text)''')
    c.executemany(
            'INSERT INTO ime VALUES (?,?)', code_list)
    db.commit()
    db.close()

def import_all_table():
    import os
    import re
    table_folder = os.path.join('.','table')
    for file in os.listdir(table_folder):
        if re.match('.+\.txt$',file):
            file_path = os.path.join(table_folder,file)
            list = table2list(file_path)
            list2sqlite(list)




import_all_table()




