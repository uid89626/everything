# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 12:53:50 2015

@author: SESA72332
"""

from setuptools import setup


def readme(fname='README.md'):
    with open(fname) as f:
        return f.read()

setup(name="Everything",
      version="1.0",
      url='z',
      license='CC BY-SA',
      description="Everything.",
      author='Aaron S. Carlton',
      author_email='uid89626@gmail.com',
      long_description=readme(),
      zip_safe=False,
#      py_modules=['mt'], #python files as modules. still imported by this name.. 'import mt'
      packages=['mt', ], #packages are folders. each must have __init__.py These are imported by this name... 'import mt'
      )
