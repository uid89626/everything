# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:51:37 2016

@author: Aaron Carlton
"""
import types

def mt(obj, mtt=str, filterprivates=True):
    """Magic Type. Return dict of items from object of given mtt type

    :fltr: boolean filter private methods
    """
    if filterprivates:
        return {n: getattr(obj, n) for n in pmf(obj) if isinstance(getattr(obj, n), mtt)}
    else:
        return {n: getattr(obj, n) for n in dir(obj) if isinstance(getattr(obj, n), mtt)}


def pmf(obj):
    """Private Method Filter. Filter '_' and '__' from names in object
    """
    return [n for n in dir(obj) if '__' not in n and not n.startswith('_')]


def ti(obj):
    """Total Inspect(object)"""
    return {typename:mt(obj, getattr(types, typename)) for typename in pmf(types)}
