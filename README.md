Summary 摘要
------------------
Code-searcher for Array30, a chinese input method. under X11 license (instead of
the tables that is under Array Input Method Public License)

It supports CJK characters, incl. Extension A - E.

行列30輸入法查碼器。除碼表外採用行列輸入法的開放授權外，採 X11 授權。支援含擴展 A 至 E 區之漢字。

Dependencies 相依套件
-------------------------
 * Python >= 3.4 (with "sqlite3" module)
 * Python3-PyQt4 >= 4.11
 * sqlite3 module for Python 3.4
 * libQt >= 4.8.5
 * pip3 (recommented)
 * Hanazono Font (for some characters in Extention blocks)

Install (under *nix) 安裝（於 *nix）
--------------------------------------

 1. Install the dependencies above. 安裝相依套件。
 2. Download the zip file of all the source code, and extract it. 下載源碼壓縮檔，解壓縮
 。
 3. Open a terminal and enter the main folder of the source code, then key in 打開終端機進入原始碼內容根目錄，輸入：

	
	./setup.py install
	

* p.s. if the depended packages listed above can be installed on Windows, it may be exexuted on Windows (I'm not so sure). 若上列相依套件可被 Windows 安裝，則可於 Windows 執行（不太確定）。


Run 執行
------------------------------
Execute ``findarray30code'' in a terminal.

執行 ``findarray30code'' 於終端機。

Remove (under *nix) 移除（於 *nix）
---------------------

It's recommended to remove it with "pip3". Please use the command after being sure that you have the authority to access the destination folder 建議使用 pip3 移除之，在確認您有存取目的資料夾權限後，請使用該指令：

    pip3 uninstall findarray30code
