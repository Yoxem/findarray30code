#!/usr/bin/env python3
#-*-coding:utf-8-*-
from distutils.core import setup
from findarray30code.__version__ import __version__

setup(
    name='findarray30code',
    version=__version__,
    author='Yoxem Chen',
    author_email='yoxem.tem98@nctu.edu.tw',
    url="https://github.com/Yoxem/findarray30code",
    requires=['PyQt4'],
    packages=['findarray30code',],
    license='X11 License',
    long_description=open('README.md').read(),
    package_data={'findarray30code': ['tables/*' , 'LICENSE'],
              },
    scripts=['bin/findarray30code'],
)
