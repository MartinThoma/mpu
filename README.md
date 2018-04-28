# mpu
Martins Python Utilities (mpu) is a collection of utility functions and classes
with no other dependencies.

The total size of the package will never be bigger than 10 MB. This makes it
a candidate to include into AWS Lambda projects.


## Installation

```
$ pip install git+https://github.com/MartinThoma/mpu.git
```

It can, of course, also be installed via PyPI.


## Usage

### Datastructures

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

### Shell

To enchance your terminals output, you might want to do something like:

```
from mpu.shell import Codes
print('{c.GREEN}{c.UNDERLINED}Works{c.RESET_ALL}'.format(c=Codes))
```
