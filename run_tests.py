import unittest

from test.test_poly import PolyArcLengthTest


def run_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(PolyArcLengthTest))
     
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == '__main__':
    run_tests()