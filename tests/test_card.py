
import unittest

from bankers import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card()
    
    def test_move_bank(self):
        self.card.card = 'bank'
        self.assertEqual(self.card.getMovement(), 38)

    def test_draw_card(self):
        self.card.drawCard()
        self.assertEqual(type(self.card.card), str)
