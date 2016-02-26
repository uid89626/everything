# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:51:37 2016

@author: Aaron Carlton
"""
import types

def mt(obj, mtt=str):
    """Magic Type. Return dict of items from object of given mtt type
    """
    return {n: getattr(obj, n) for n in dir(obj) if isinstance(getattr(obj, n), mtt)}

def pmf(obj):
    """Private Method Filter. Filter '_' and '__' from names in object
    """
    return [n for n in dir(obj) if not '__' in n and not '_' in n]

def ti(obj):
    """Total Inspect(object)"""
    return {typename:mt(obj, getattr(types, typename)) for typename in pmf(types)}
