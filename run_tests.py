import unittest

from test.test_poly import PolyArcLengthTest
from test.test_qss import QSS3ArcLengthTest


def run_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(PolyArcLengthTest))
    test_suite.addTest(unittest.makeSuite(QSS3ArcLengthTest))
     
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == '__main__':
    run_tests()