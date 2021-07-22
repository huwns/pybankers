
import unittest

from analyze_bankers import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card()
    
    def test_move_bank(self):
        self.card.card = 'bank'
        self.assertEqual(self.card.getMovement(), 38)