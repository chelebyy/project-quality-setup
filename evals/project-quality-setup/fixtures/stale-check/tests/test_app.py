import unittest
from app import can_read

class AccessTests(unittest.TestCase):
    def test_owner_can_read(self):
        self.assertTrue(can_read('owner', 'owner'))

    def test_other_user_cannot_read(self):
        self.assertFalse(can_read('owner', 'visitor'))
