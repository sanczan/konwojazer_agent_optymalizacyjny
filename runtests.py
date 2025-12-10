#!/usr/bin/env python3
"""Prosty runner do uruchamiania wszystkich testów jednostkowych."""
import sys
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1
)
