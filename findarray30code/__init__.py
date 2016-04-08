#!/usr/bin/env python3
#-*-coding:utf-8-*-
import sqlite3
import sys
from findarray30code import ui, ui2
import re

from PyQt4 import QtGui, QtCore

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

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
    main_dirname = os.path.dirname(os.path.abspath(__file__))

    db ,c = create_new_db(':memory:')
    table_folder = os.path.join(main_dirname, 'tables')
    table_folder_files = os.listdir(table_folder)

    for file in table_folder_files:
        if re.match('.+\.txt$',file):

            file_path = os.path.join(table_folder,file)
            list = table2list(file_path)
            list2sqlite(list,c)

    db.commit()
    return db, c

def rawcode2truecode(raw):
    #1^ = Q, 1- = A, 1v = Z, 2^ = W, 2- = S ......, 0^ = P, 0- = :, 0v = ?
    raw_code_order = "QAZWSXEDCRFVTGBYHNUJMIK,OL.P;/"
    true_code = ""
    index = 0
    for i in raw:
        i_index = raw_code_order.index(i)
       
        uncorrected_column = i_index // 3
        #correct the column no. 2 -> 3; 9 -> 0
        column = str(uncorrected_column + 1)[-1]
        row_number = i_index % 3
        row = ['^','-','v'][row_number] # 0=^;1=-;2=v
        column_and_row = column + row
        true_code = true_code + column_and_row
        index = index * 30 + i_index
    index = (5-len(raw))*(30**5) + index
    return true_code,index

class MainWindow(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        self.db,self.c = import_all_table()

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.lineEdit.returnPressed.connect(self.input_characters)
        self.pushButton.clicked.connect(self.input_characters)
        self.pushButton_2.clicked.connect(self.clear_input)
        self.action_About.triggered.connect(self.show_about)
       
    def clear_input(self):
        self.label_2.setText("")
        self.lineEdit.clear()

    def show_about(self):
        #version no.
        from findarray30code.__version__ import __version__
        
        about_dialog = QtGui.QDialog()
        about_dialog_ui = ui2.Ui_Dialog()
        about_dialog_ui.setupUi(about_dialog)
        
        #import license
        from os.path import abspath, dirname, join
        license_file_path = join(dirname(abspath(__file__)),"LICENSE")
        license_content_raw = open(license_file_path,"r").read()
        license_content = re.sub("\n+", "<br/>",license_content_raw)

        about_dialog_info = '''
<html>
<body><div align=\"center\">
<span style=\" font-size:18pt; font-weight:600;\">findarray30code</span><p/>'''
        about_dialog_info += str(__version__)
        about_dialog_info += '''
<p/>查詢行列 30 輸入法碼表的工具。<p/>支援 CJK Ext. A - E 的罕字。<br/><a href=\"https://github.com/Yoxem/findarray30code \"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/Yoxem/findarray30code</span></a><p/>Copyright (C) 2016 Yoxem Chen (aka Kian-ting Tan) <p/>Input method tables: Liao, Ming-te et. al.<p/>
under X11 License<p/></div>
<div align=\"left\">
<h3>License</h3>
<span style=\" font-size:9pt;\">
'''
        about_dialog_info +=  license_content + \
                                   "</span></div></body></html>"

        about_dialog_ui.label.setText(about_dialog_info)


        about_dialog.exec_()


    def show_result(self,char_code):
        result = ""
        header = "<table style=\"vertical-align:top;\"><tr><td colspan=2>查碼結果：</td></tr>"
        result = header + result

        for (char,code) in char_code:
            result = result + '<tr><td style="font-size:x-large;' + \
                'vertical-align:top;">' + \
                char + '</td><td>'
               
            for i in range(len(code)):
                if (i < len(code) - 1):
                    result = result + code[i] + '<br/>'
                else:
                    result = result + code[i] + '</td></tr>'
       
        result = result + '</table>'
        self.label_2.setText(result)

    def find_code(self,char):
        c = self.c
        if (char != "" and char != None):
            raw_query = c.execute('''SELECT code FROM ime WHERE char = ?''', (char,))
            raw_code = [i[0] for i in raw_query.fetchall()]
            code_with_index = [rawcode2truecode(i) for i in raw_code]
            code = [i[0] for i in sorted(code_with_index,key= lambda x : x[1])]
            return char,code
        else:
            pass
       
    def input_characters(self):
        characters = self.lineEdit.text()
        chinese_char_pattern = re.compile(u"[一-鿌㐀-䶵𠀀-𪛖𪜀-𫜴𫝀-𫠝𫠠-𬺡]",re.UNICODE)
        chinese_chars_split = chinese_char_pattern.findall(characters)

        char_code_list = [self.find_code(ch) for ch in chinese_chars_split]
        self.show_result(char_code_list)
       
def main():
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()

if __name__ == '__main__':
    main()
