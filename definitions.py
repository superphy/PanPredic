#!/usr/bin/env python

"""
    Definitions for PanPredic
"""

import os

PAN_IDENT = '98'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER_CONFIG = os.path.join(ROOT_DIR, 'logging.conf')
DATA_DIR = os.path.join(ROOT_DIR, 'Data/')

PAN_RESULTS = ROOT_DIR + '/tests/data/panResults2'
NOVEL_RESULTS = ROOT_DIR + '/tests/data/novelResults'
