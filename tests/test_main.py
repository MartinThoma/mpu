# core modules
import unittest

# internal modules
from mpu import parallel_for


class DatastructuresInit(unittest.TestCase):

    def test_parallel_for(self):
        import time

        def looping_function(payload):
            i, j = payload
            time.sleep(1)
        parameters = list((i, i + 1) for i in range(50))
        out = parallel_for(looping_function, parameters)
        print(out)
