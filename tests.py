import subprocess
import unittest


class BehaveToolkitTestCase(unittest.TestCase):

    def test_flake8(self):
        subprocess.check_call(['flake8', 'behave_toolkit/'])

if __name__ == '__main__':
    unittest.main()
