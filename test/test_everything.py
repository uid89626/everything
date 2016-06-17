# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:47:00 2016

@author: Aaron Carlton
"""

import pytest
import mt


@pytest.mark.parametrize('lib', mt.all)
def test_imports(lib):
    assert lib

if __name__ == '__main__':
    pytest.main(['-vs', '.'])
