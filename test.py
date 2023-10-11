"""This script tests the ADH Event Store Python sample script"""

import unittest
from program import main


class ADHEventStoreE2ETest(unittest.TestCase):
    """Tests for the ADH Security Python sample"""

    @classmethod
    def test_main(cls):
        """End to end test for main function"""
        main(True)


if __name__ == '__main__':
    unittest.main()
