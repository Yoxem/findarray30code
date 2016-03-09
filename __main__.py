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

def connect_db(db_filename):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    return db,c

def create_new_db(db_filename):
    db, c = connect_db(db_filename)
    c.execute('''CREATE TABLE ime (code text, char text)''')  
    return db, c


def list2sqlite(code_list,c):

    c.executemany(
            'INSERT INTO ime VALUES (?,?)', code_list)

def import_all_table():
    import os
    import re
    main_dirname = os.path.dirname(os.path.abspath(__file__))

    db ,c = create_new_db(':memory:')
    table_folder = os.path.join(main_dirname, 'table')
    table_folder_files = os.listdir(table_folder)

    for file in table_folder_files:
        if re.match('.+\.txt$',file):

            file_path = os.path.join(table_folder,file)
            list = table2list(file_path)
            list2sqlite(list,c)

    db.commit()

def find_code(char,c):

    raw_code = c.execute('''SELECT code FROM ime WHERE char = ?''', (c,)) 
    code = [rawcode2truecode(i) for i in raw_code]
    return code, c

def rawcode2truecode(raw):
    raw_code_order = "QAZWSXEDCRFVTGBYHNUJMIK<OL>P:?"
    true_code = ""

    for i in raw:
        i_index = raw_code_order.index(i)
        column = str(i_index // 3)
        raw_number = index % 3
        raw = ['^','-','v'][raw_number]
        column_and_raw = column + raw
        true_code = true_code + column_and_raw

    return true_code

import_all_table()
