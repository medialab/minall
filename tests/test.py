import unittest

from buzzsumo import TestBuzzsumo


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestBuzzsumo("test_expected_values"))
    suite.addTest(TestBuzzsumo("test_repeated_calls"))


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
