# -*- coding: utf-8 -*-
"""Sammelt die Artikeldaten aus dem Ordner art/."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "art"))

import a01, a02, a03, a04, a05, a06, a07, a08, a09, a10  # noqa: E402

ARTICLES = [
    a01.A, a02.A, a03.A, a04.A, a05.A,
    a06.A, a07.A, a08.A, a09.A, a10.A,
]
