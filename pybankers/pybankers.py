"""ボードゲーム「バンカース」における各マスの止まりやすさを計算する."""

import random
from typing import List

import matplotlib.pyplot as plt  # type:ignore


__all__ = ["AnalyzeBankers", "Card", "Tile"]


def dice() -> int:
    """2つのサイコロの目の合計を出力する関数.

    Returns:
        int: 2つのサイコロの目の合計
    """
    return random.randint(1, 6) + random.randint(1, 6)


class Card:
    """カードのデッキを表すクラス."""

    NORMAL_CARDS: List[str] = ["normal" for i in range(11)]
    MOVE_CARDS: List[str] = [
        "15",
        "next card",
        "next card",
        "bank",
        "back to corner",
        "chuou",
        "theatre",
        "sairei",
        "koun",
    ]
    CARDS: List[str] = NORMAL_CARDS + MOVE_CARDS
    CARD_POSITION: List[int] = [2, 17, 23, 28, 32, 37]
    CORNER_POSITION: List[int] = [0, 11, 20, 31]
    CHUOU_POSITION: int = 25
    THEATRE_POSITION: int = 26
    SAIREI_POSITION: int = 20
    KOUN_POSITION: int = 21

    # この初期値設定はどういうこと？
    def __init__(self, card: str = "normal", position: int = 2) -> None:
        """Init."""
        self.cards: List[str] = Card.CARDS.copy()
        self.card: str = card
        self.position: int = position

    def draw_card(self) -> None:
        """カードを引く."""
        if len(self.cards) <= 0:
            self.cards = Card.CARDS.copy()
        self.card = self.cards.pop(random.randint(0, len(self.cards) - 1))

    def move_corner(self):
        """角に移動するカードによる移動数を計算."""
        position = [self.position] + Card.CORNER_POSITION
        position.sort()
        corner = Card.CORNER_POSITION[
            ((position.index(self.position) - 1) % len(Card.CORNER_POSITION))
        ]
        return -((self.position - corner) % LEN_BOARD)

    def move_bank(self):
        """「銀行」へ行くカードの移動数を計算."""
        return -self.position % LEN_BOARD

    def move_chuou(self):
        """「中央線」へ行くカードの移動数を計算."""
        return (Card.CHUOU_POSITION - self.position) % LEN_BOARD

    def move_theatre(self):
        """「劇場」へ行くカードによる移動数を計算."""
        return (Card.THEATRE_POSITION - self.position) % LEN_BOARD

    def move_sairei(self):
        """「祭礼」へ行くカードによる移動数を計算."""
        return (Card.SAIREI_POSITION - self.position) % LEN_BOARD

    def move_koun(self):
        """「幸運」へ行くカードによる移動数を計算."""
        return (Card.KOUN_POSITION - self.position) % LEN_BOARD

    def move_nextcard(self):
        """「次のカード」へ行くカードによる移動数を計算."""
        nextcard = Card.CARD_POSITION[
            ((Card.CARD_POSITION.index(self.position) + 1)
                % len(Card.CARD_POSITION))
        ]
        return (nextcard - self.position) % LEN_BOARD

    def get_movement(self):
        """カードによる移動数を出力するメソッド."""
        result = 0
        if self.card == "15":
            result = 15
        elif self.card == "next card":
            result = self.move_nextcard()
        elif self.card == "koun":
            result = self.move_koun()
        elif self.card == "sairei":
            result = self.move_sairei()
        elif self.card == "bank":
            result = self.move_bank()
        elif self.card == "chuou":
            result = self.move_chuou()
        elif self.card == "theatre":
            result = self.move_theatre()
        elif self.card == "back to corner":
            result = self.move_corner()

        return result


class Tile:
    """バンカースのマスを表すクラス."""

    def __init__(self, name="銀行", move_type="normal"):
        """Init."""
        self.name = name
        self.move_type = move_type

    def get_move(self, card, position):
        """移動に関わる特殊マスでの移動数を計算するメソッド.

        Args:
            card (Card): Cardクラス
            position (int): どのマス目にいるか

        Returns:
            int: 移動に関わる特殊マスでの移動数
        """
        if self.move_type == "sairei":
            dice_num = dice()
            if dice_num % 2 == 1:
                dice_num = -dice_num
            return dice_num
        elif self.move_type == "card":
            card.position = position
            card.draw_card()
            return card.get_movement()
        elif self.move_type == "redice":
            return dice()
        elif self.move_type == "boat":
            return 7
        elif self.move_type == "tikko":
            return 2
        elif self.move_type == "noriokure":
            return 4
        else:
            return 0


# 定数定義
BOARD = [
    Tile(),
    Tile("寺町"),
    Tile("カード", "card"),
    Tile("京町"),
    Tile("本町通"),
    Tile("内海汽船", "redice"),
    Tile("都道"),
    Tile("明治通"),
    Tile("納税"),
    Tile("公開堂通"),
    Tile("中央通"),
    Tile("モーターボード", "boat"),
    Tile("租税割戻"),
    Tile("栄町"),
    Tile("取引所通"),
    Tile("遊覧飛行機旅行", "redice"),
    Tile("山手台"),
    Tile("カード", "card"),
    Tile("築港", "tikko"),
    Tile("野球場"),
    Tile("祭礼", "sairei"),
    Tile("幸運"),
    Tile("神宮通"),
    Tile("カード", "card"),
    Tile("大手町"),
    Tile("中央線", "redice"),
    Tile("国立劇場"),
    Tile("扇町"),
    Tile("カード", "card"),
    Tile("昭和通"),
    Tile("市場通"),
    Tile("列車に乗り遅れ", "noriokure"),
    Tile("カード", "card"),
    Tile("遺産相続"),
    Tile("元町通"),
    Tile("バス旅行", "redice"),
    Tile("一番街"),
    Tile("カード", "card"),
    Tile("銀座街"),
    Tile("日本橋"),
]

LEN_BOARD = len(BOARD)


def where_board(count):
    """総カウントから剰余算により現在いるマスを計算する.

    >>> where_board(40)
    0
    """
    return count % LEN_BOARD


class AnalyzeBankers:
    """各マスの止まりやすさを計算するクラス."""

    def __init__(self, max_count):
        """Init."""
        self.max_count = max_count
        self.panel_counter = [0 for i in range(40)]
        self.count = 0
        self.card = Card()

    def step_eval(self, steps, count):
        """1ターンの最終到達点を計算する再帰関数.

        Args:
            steps (int): 最終到達点までに進んだマス目の数
            count (int): 現在の総カウント
            card (Card): カードクラスのインスタンス

        Returns:
            int: 最終到達点までに進んだマス目の数
        """
        if (count + steps) % LEN_BOARD == 18:
            if steps == 7:
                return steps
        if steps == 0:
            return 0

        count += steps
        next_steps = BOARD[where_board(count)].get_move(
            self.card, where_board(count)
        )
        return steps + self.step_eval(next_steps, count)

    def analyze(self):
        """1ターンで最終的にどこに止まったかを記録していくことで、止まりやすい家を算出する."""
        while self.count < self.max_count:
            dice_num = dice()
            steps = self.step_eval(dice_num, self.count)
            self.count += steps
            self.panel_counter[where_board(self.count)] += 1
        return self.panel_counter


def main():
    """Main function."""
    import argparse
    parser = argparse.ArgumentParser(
        description=r"""
PyBankers - The board game Bankers analyzer.
__________        __________                __                        
\______   \___.__.\______   \_____    ____ |  | __ ___________  ______
|     ___<   |  | |    |  _/\__  \  /    \|  |/ // __ \_  __ \/  ___/
|    |    \___  | |    |   \ / __ \|   |  \    <\  ___/|  | \/\___ \ 
|____|    / ____| |______  /(____  /___|  /__|_ \\___  >__|  /____  >
        \/             \/      \/     \/     \/    \/           \/ """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("max_count")
    args = parser.parse_args()
    analyze_bankers = AnalyzeBankers(args.max_count)
    panel_counter = analyze_bankers.analyze()
    print("Result:")
    for i in range(LEN_BOARD):
        print(BOARD[i].name, panel_counter[i])
    plt.figure()
    xaxis = list(range(LEN_BOARD))
    plt.bar(xaxis, panel_counter)
    plt.show()


if __name__ == "__main__":
    main()
