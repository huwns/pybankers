"""ボードゲーム「バンカース」における各マスの止まりやすさを計算する。"""

import random
import matplotlib.pyplot as plt

def dice():
    """2つのサイコロの目の合計を出力する関数

    Returns:
        int: 2つのサイコロの目の合計
    """

    return random.randint(1, 6) + random.randint(1, 6)

class Card:
    """カードのデッキを表すクラス"""

    NORMAL_CARDS = ['normal' for i in range(11)]
    MOVE_CARDS = [
        '15', 'next card', 'next card', 'bank', 'back to corner', 'chuou',
        'theatre', 'sairei', 'koun'
    ]
    CARDS = NORMAL_CARDS + MOVE_CARDS
    CARD_POSITION = [2, 17, 23, 28, 32, 37]
    CORNER_POSITION = [0, 11, 20, 31]
    CHUOU_POSITION = 25
    THEATRE_POSITION = 26
    SAIREI_POSITION = 20
    KOUN_POSITION = 21

    # この初期値設定はどういうこと？
    def __init__(self, card='normal', position=2):
        self.cards = Card.CARDS.copy()
        self.card = card
        self.position = position

    def drawCard(self):
        """カードを引く"""

        if len(self.cards) <= 0:
            self.cards = Card.CARDS.copy()
        self.card = self.cards.pop(random.randint(0, len(self.cards) - 1))

    def moveCorner(self):
        """角に移動するカードによる移動数を計算"""

        position = [self.position] + Card.CORNER_POSITION
        position.sort()
        corner = Card.CORNER_POSITION[(
            (position.index(self.position) - 1) % len(Card.CORNER_POSITION))]
        return -((self.position - corner) % len_BOARD)

    def moveBank(self):
        """「銀行」へ行くカードの移動数を計算"""

        return -self.position % len_BOARD

    def moveChuou(self):
        """「中央線」へ行くカードの移動数を計算"""

        return (Card.CHUOU_POSITION - self.position) % len_BOARD

    def moveTheatre(self):
        """「劇場」へ行くカードによる移動数を計算"""

        return (Card.THEATRE_POSITION - self.position) % len_BOARD

    def moveSairei(self):
        """「祭礼」へ行くカードによる移動数を計算"""

        return (Card.SAIREI_POSITION - self.position) % len_BOARD

    def moveKoun(self):
        """「幸運」へ行くカードによる移動数を計算"""

        return (Card.KOUN_POSITION - self.position) % len_BOARD

    def moveNextcard(self):
        """「次のカード」へ行くカードによる移動数を計算"""

        nextcard = Card.CARD_POSITION[(
            (Card.CARD_POSITION.index(self.position) + 1) % len(Card.CARD_POSITION))]
        return (nextcard - self.position) % len_BOARD

    def getMovement(self):
        """カードによる移動数を出力するメソッド"""

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


class Tile:
    """バンカースのマスを表すクラス"""

    def __init__(self, name='銀行', move_type='normal'):
        self.name = name
        self.move_type = move_type

    def getMove(self, card, position):
        """移動に関わる特殊マスでの移動数を計算するメソッド

        Args:
            card (Card): Cardクラス
            position (int): どのマス目にいるか

        Returns:
            int: 移動に関わる特殊マスでの移動数
        """

        if self.move_type == 'sairei':
            dice_num = dice()
            if dice_num % 2 == 1:
                dice_num = -dice_num
            return dice_num
        elif self.move_type == 'card':
            card.position = position
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

# 定数定義
BOARD = [
    Tile(), Tile('寺町'), Tile('カード', 'card'), Tile('京町'), Tile('本町通'),
    Tile('内海汽船', 'redice'),Tile('都道'), Tile('明治通'), Tile('納税'),
    Tile('公開堂通'), Tile('中央通'), Tile('モーターボード', 'boat'), Tile('租税割戻'),
    Tile('栄町'), Tile('取引所通'), Tile('遊覧飛行機旅行', 'redice'), Tile('山手台'),
    Tile('カード', 'card'), Tile('築港', 'tikko'), Tile('野球場'), Tile('祭礼', 'sairei'),
    Tile('幸運'), Tile('神宮通'), Tile('カード', 'card'), Tile('大手町'),
    Tile('中央線', 'redice'), Tile('国立劇場'), Tile('扇町'), Tile('カード', 'card'),
    Tile('昭和通'), Tile('市場通'), Tile('列車に乗り遅れ', 'noriokure'),
    Tile('カード', 'card'), Tile('遺産相続'), Tile('元町通'), Tile('バス旅行', 'redice'),
    Tile('一番街'), Tile('カード', 'card'), Tile('銀座街'), Tile('日本橋')
]

len_BOARD = len(BOARD)

def where_board(count):
    """総カウントから剰余算により現在いるマスを計算する。"""

    return count % len_BOARD

class AnalyzeBankers:
    """各マスの止まりやすさを計算するクラス"""

    def __init__(self, max_count):
        self.max_count = max_count
        self.panel_counter = [0 for i in range(40)]
        self.count = 0
        self.card = Card()

    def stepEval(self, steps, count):
        """1ターンの最終到達点を計算する再帰関数

        Args:
            steps (int): 最終到達点までに進んだマス目の数
            count (int): 現在の総カウント
            card (Card): カードクラスのインスタンス

        Returns:
            int: 最終到達点までに進んだマス目の数
        """

        if (count + steps) % len_BOARD == 18:
            if steps == 7:
                return steps
        if steps == 0:
            return 0
        else:
            count += steps
            next_steps = BOARD[where_board(count)].getMove(self.card, where_board(count))
            return steps + self.stepEval(next_steps, count)

    def analyze(self):
        """1ターンで最終的にどこに止まったかを記録していくことで、止まりやすい家を算出する。"""
        
        while self.count < self.max_count:
            dice_num = dice()
            steps = self.stepEval(dice_num, self.count)
            self.count += steps
            self.panel_counter[where_board(self.count)] += 1
        return self.panel_counter


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Bankers Analysis Tool')
    parser.add_argument('max_count', type=int, help='max steps count')
    args = parser.parse_args(['10000'])
    ab = AnalyzeBankers(args.max_count)
    panel_counter = ab.analyze()
    print('Result:')
    for i in range(len_BOARD):
        print(BOARD[i].name, panel_counter[i])
    fig = plt.figure()
    xaxis = [i for i in range(len_BOARD)]
    plt.bar(xaxis, panel_counter)
    plt.show()

if __name__ == '__main__':
    main()
