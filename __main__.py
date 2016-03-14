#!/usr/bin/env python3
#-*-coding:utf-8-*-
import sqlite3
import sys
from PyQt4 import QtGui, uic

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
    return db, c

def find_code(char,c):

    raw_query = c.execute('''SELECT code FROM ime WHERE char = ?''', (char,))
    raw_code = [i[0] for i in raw_query.fetchall()]
    code = [rawcode2truecode(i) for i in raw_code]
    code = sorted(code,reverse=True)
    print(code)
    return code, c


def rawcode2truecode(raw):
    #1^ = Q, 1- = A, 1v = Z, 2^ = W, 2- = S ......, 0^ = P, 0- = :, 0v = ?
    raw_code_order = "QAZWSXEDCRFVTGBYHNUJMIK<OL>P:?"
    true_code = ""

    for i in raw:
        i_index = raw_code_order.index(i)
        uncorrected_column = i_index // 3
        #correct the column no. 2 -> 3; 9 -> 0
        column = str(uncorrected_column + 1)[-1]
        raw_number = i_index % 3
        raw = ['^','-','v'][raw_number] # 0=^;1=-;2=v
        column_and_raw = column + raw
        true_code = true_code + column_and_raw

    return true_code

db,c = import_all_table()

find_code("越",c)
