#!/usr/bin/env python3
#-*-coding:utf-8-*-
from distutils.core import setup
from findarray30code.__version__ import __version__

setup(
    name='FindArray30Code',
    version=__version__,
    author='Yoxem Chen',
    url="https://github.com/Yoxem/findarray30code",
    requires=['PyQt4'],
    packages=['findarray30code',],
    license='X11 License',
    long_description=open('README.md').read(),
    package_data={'findarray30code': ['tables/*' , 'LICENSE'],
              },
    scripts=['bin/findarray30code'],
)
