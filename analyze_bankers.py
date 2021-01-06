import random
import matplotlib.pyplot as plt


class Tile:

	def __init__(self, name='銀行', move_type='normal'):
		self.name = name
		self.move_type = move_type

	def getName(self):
		return self.name

	def getMoveType(self):
		return self.move_type

	def getMove(self, card, position):
		if self.move_type == 'sairei':
			dice_num = dice()
			if dice_num % 2 == 1:
				dice_num = -dice_num
			return dice_num
		elif self.move_type == 'card':
			card.setPosition(position)
			card.drawCard()
			return card.getMovement()
		elif self.move_type == 'redice':
			return dice()
		elif self.move_type == 'boat':
			return 7
		elif self.move_type == 'tikko':
			return 2
		elif self.move_type == 'noriokure':
			return 4
		else:
			return 0


class Card:
	NORMAL_CARDS = ['normal' for i in range(11)]
	MOVE_CARDS = [
		'15', 'next card', 'next card', 'bank', 'back to corner', 'chuou', 'theatre',
		'sairei', 'koun'
	]
	CARDS = NORMAL_CARDS + MOVE_CARDS
	CARD_POSITION = [2, 17, 23, 28, 32, 37]
	CORNER_POSITION = [0, 11, 20, 31]
	CHUOU_POSITION = 25
	THEATRE_POSITION = 26
	SAIREI_POSITION = 20
	KOUN_POSITION = 21

	def __init__(self, card='normal', position=2):
		self.cards = Card.CARDS.copy()
		self.card = card
		self.position = position

	def moveCorner(self):
		position = [self.position] + Card.CORNER_POSITION
		position.sort()
		corner = Card.CORNER_POSITION[(
			(position.index(self.position) - 1) % len(Card.CORNER_POSITION))]
		return -((self.position - corner) % len(BOARD))

	def setPosition(self, position):
		self.position = position

	def getCard(self):
		return self.card

	def drawCard(self):
		if len(self.cards) <= 0:
			self.cards = Card.CARDS.copy()
		self.card = self.cards.pop(random.randint(0, len(self.cards) - 1))

	def moveBank(self):
		return -self.position % len(BOARD)

	def moveChuou(self):
		return (Card.CHUOU_POSITION - self.position) % len(BOARD)

	def moveTheatre(self):
		return (Card.THEATRE_POSITION - self.position) % len(BOARD)

	def moveSairei(self):
		return (Card.SAIREI_POSITION - self.position) % len(BOARD)

	def moveKoun(self):
		return (Card.KOUN_POSITION - self.position) % len(BOARD)

	def moveNextcard(self):
		nextcard = Card.CARD_POSITION[(
			(Card.CARD_POSITION.index(self.position) + 1) % len(Card.CARD_POSITION))]
		return (nextcard - self.position) % len(BOARD)

	def getMovement(self):
		if self.card == '15':
			return 15
		elif self.card == 'next card':
			return self.moveNextcard()
		elif self.card == 'koun':
			return self.moveKoun()
		elif self.card == 'sairei':
			return self.moveSairei()
		elif self.card == 'bank':
			return self.moveBank()
		elif self.card == 'chuou':
			return self.moveChuou()
		elif self.card == 'theatre':
			return self.moveTheatre()
		elif self.card == 'back to corner':
			return self.moveCorner()
		else:
			return 0


# 定数定義
BOARD = [
	Tile(), Tile('寺町'), Tile('カード', 'card'), Tile('京町'), Tile('本町通'), Tile(
		'内海汽船', 'redice'),
	Tile('都道'), Tile('明治通'), Tile('納税'), Tile('公開堂通'), Tile('中央通'), Tile(
		'モーターボード', 'boat'), Tile('租税割戻'), Tile('栄町'), Tile('取引所通'), Tile(
			'遊覧飛行機旅行', 'redice'), Tile('山手台'), Tile('カード', 'card'), Tile('築港', 'tikko'),
	Tile('野球場'), Tile('祭礼', 'sairei'), Tile('幸運'), Tile('神宮通'), Tile(
		'カード', 'card'), Tile('大手町'), Tile('中央線', 'redice'), Tile('国立劇場'),
	Tile('扇町'), Tile('カード', 'card'), Tile('昭和通'), Tile('市場通'), Tile(
		'列車に乗り遅れ', 'noriokure'), Tile('カード', 'card'), Tile('遺産相続'), Tile('元町通'), Tile(
			'バス旅行', 'redice'), Tile('一番街'), Tile('カード', 'card'), Tile('銀座街'), Tile('日本橋')
]

panel_counter = [0 for i in range(40)]


def where_board(count):
	return count % len(BOARD)


def dice():
	return random.randint(1, 6) + random.randint(1, 6)


def stepEval(steps, count, card):
	if (count + steps) % len(BOARD) == 18:
		if steps == 7:
			return steps
	if steps == 0:
		return 0
	else:
		count += steps
		next_steps = BOARD[where_board(count)].getMove(card, where_board(count))
		return steps + stepEval(next_steps, count, card)


# -- main ---
if __name__ == '__main__':
	count = 0
	card = Card()
	while count < 1000000:
		dice_num = dice()
		steps = stepEval(dice_num, count, card)
		count += steps
		panel_counter[where_board(count)] += 1
	print('Result:')
	for i in range(len(BOARD)):
		print(BOARD[i].getName(), panel_counter[i])
	fig = plt.figure()
	xaxis = [i for i in range(40)]
	plt.bar(xaxis, panel_counter)
	plt.show()
