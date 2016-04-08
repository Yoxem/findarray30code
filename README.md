Summary
---------------
Code-searcher for Array30, a chinese input method. under X11 license
It supports CJK characters, incl. Extension A - E.

Dependencies
----------------
 * Python >= 3.4 (with "sqlite3" module)
 * Python3-PyQt4 >= 4.11
 * sqlite3 module for Python 3.4
 * libQt >= 4.8.5
 * pip3 (recommented)
 * Hanazono Font (for some characters in Extention blocks)

Install (Under *nix)
-----------------------------

 1. Install the dependencies above
 2. download the zip file of all the source code, and extract it.
 3. open a terminal and enter the main folder of the source code, then key in:
     
     ./setup.py install

 4. If the depended packages listed above can be install on windows, it may be executed on Windows (I'm not so sure).

Remove
---------------

It's recommented to remove it with "pip3". Please use the command after being sure that you have the authority to access the folder:

    pip3 uninstall findarray30code
