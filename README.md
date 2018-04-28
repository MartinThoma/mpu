# mpu
Martins Python Utilities (mpu) is a collection of utility functions and classes
with no other dependencies.

## Installation

```
$ pip install git+https://github.com/MartinThoma/mpu.git
```

It can, of course, also be installed via PyPI.


## Usage

```
from mpu.datastructures import EList

>>> l = EList([2, 1, 0])
>>> l[2]
0

>>> l[[2, 0]]
[0, 2]

>>> l[l]
[0, 1, 2]
```
