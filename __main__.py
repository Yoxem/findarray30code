#!/usr/bin/env python3
#-*-coding:utf-8-*-
import sqlite3
import sys
import ui, ui2
from PyQt4 import QtGui, QtCore


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
    code_with_index = [rawcode2truecode(i) for i in raw_code]
    code = [i[0] for i in sorted(code_with_index,key= lambda x : x[1])]
    return code

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
        about_dialog = QtGui.QWidget()
        about_dialog_ui = ui2.Ui_Dialog()
        about_dialog_ui.setupUi(about_dialog)
        about_dialog.show()

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
        
    def input_characters(self):
        import re
        characters = self.lineEdit.text()
        
        #some CJK ext B,C,etc arerepensented in utf16 in pyqt qlineedit.
        #convert it to utf8
        #characters = characters.encode(encoding='utf-16',errors='surrogatepass').decode('utf-8')
        #print('\\u'+"\\u".join("{:x}".format(ord(c)) for c in characters))
        chinese_char_pattern = re.compile("^[一-鿌㐀-䶵𠀷𠂁𠁍]+$",re.UNICODE)
        is_chinese_chars = chinese_char_pattern.match(characters)

        if is_chinese_chars:
           char_code_list = [(ch,find_code(ch,self.c)) for ch in characters]
           self.show_result(char_code_list)
        else:
            print("error")
        
def main():
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()

    

if __name__ == '__main__':
    main()
    


