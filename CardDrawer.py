
import math

class CardDrawer(object):
    symbols = {"vbar": "║", "hbar": "═", "1": "╔", "2": "╗", "3": "╝", "4": "╚", "clubs": "♣", "diamonds": "♦", "hearts": "♥", "spades": "♠"}

    # 13, 9
    def get_hand(self, cards, dims):
        card_visual_representations = []
        for card in cards:
            card_visual_representations.append(self.get_card_repr(card[0], card[1], dims))
        return self.get_side_by_side_representation(card_visual_representations, dims)

    def get_card_repr(self, value, suite, dims):
        if value == 1:
            value = "A"
        elif value == 11:
            value = "J"
        elif value == 12:
            value = "Q"
        elif value == 13:
            value = "K"
        else:
            value = str(value)

        cardstr = ""
        for i in range(dims[1]):
            if i == 0:
                cardstr += self.symbols["1"]
                cardstr += self.symbols["hbar"] * (dims[0]-2)
                cardstr += self.symbols["2"]
                cardstr += "\n"
                continue
                
            elif i == math.floor(dims[1]/2) - 1 or i == math.floor(dims[1]/2 + 1):
                cardstr += self.symbols["vbar"]
                cardstr += " " * math.floor(dims[0]/2 - 1)
                cardstr += self.symbols[suite]
                cardstr += " " * (math.floor(dims[0]/2) - 1)
                cardstr += self.symbols["vbar"]
                cardstr += "\n"
                continue

            elif i == math.floor(dims[1]/2):
                cardstr += self.symbols["vbar"]
                cardstr += " " * math.floor(dims[0]/2 - 1)
                cardstr += value
                if value == "10":
                    cardstr += " " * (math.floor(dims[0]/2) - 2)
                else:
                    cardstr += " " * (math.floor(dims[0]/2) - 1)
                cardstr += self.symbols["vbar"]
                cardstr += "\n"
                continue

            elif i == dims[1]-1:
                cardstr += self.symbols["4"]
                cardstr += self.symbols["hbar"]* (dims[0]-2)
                cardstr += self.symbols["3"]
                cardstr += "\n"
                continue
            else:
                cardstr += self.symbols["vbar"]
                cardstr += " " * (dims[0] - 2)
                cardstr += self.symbols["vbar"]
                cardstr += "\n"
        return cardstr

    def get_side_by_side_representation(self, cards, dims):
        sbs_repr = ""
        for i in range(dims[0] - 3):
            for card in cards:
                sbs_repr += card.split("\n")[i] + " " * 4
            sbs_repr += "\n"
        return sbs_repr

if __name__ == "__main__":
    testhand = [[10, "spades"], [11, "spades"], [6, "hearts"], [1, "clubs"], [4, "spades"]]
    cd = CardDrawer()
    print(cd.get_hand(testhand))


