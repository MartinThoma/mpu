#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest

# First party
import mpu.ml


def test_negative_class_number():
    with pytest.raises(ValueError):
        mpu.ml.indices2one_hot([0, 1, 1], 0)
