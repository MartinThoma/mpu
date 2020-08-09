#!/usr/bin/env python


# Third party
import pytest

# First party
import mpu.ml


def test_negative_class_number():
    with pytest.raises(ValueError):
        mpu.ml.indices2one_hot([0, 1, 1], 0)


def test_indices2one_hot():
    assert mpu.ml.indices2one_hot([0, 0], 1) == [[1], [1]]
