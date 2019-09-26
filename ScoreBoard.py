

class ScoreBoard:
    symbols = {"vbar": "║", "hbar": "═", "1": "╔", "2": "╗", "3": "╝", "4": "╚"}
    dims = []
    scr = None
    tiers = [1, 5, 10]
    winning_hands = ["jacks or better", "two pairs", "three of a kind", "straight", "flush", "full house", "four of a kind", "straight flush", "royal flush"]
    cell_width = 0
    bet = 5
    board_width = 0
    # This is the reward that player gets per above winning hands (initial bet*scaling)
    scaling = [1, 2, 3, 4, 6, 9, 25, 50, 250]

    def __init__(self, dims, scr):
        self.cell_width = max([len(hand) for hand in self.winning_hands])+1
        #scr.addstr(0, 0, self.get_scoreboard_sceleton(dims), curses.A_REVERSE)
        self.dims = dims
        self.scr = scr
        # cell width * number of columns + 2 vbars + number of columns-1 (the separator of each tier)
        self.board_width = (len(self.tiers)+1)*self.cell_width + 2 + len(self.tiers)-2

    def get_scoreboard_sceleton(self):
        sclt = self.symbols["1"] + self.symbols["hbar"]*(self.board_width) + self.symbols["2"] + "\n"
        for i in range(len(self.winning_hands)):
            sclt += self.symbols["vbar"] + self.winning_hands[i] + " "*self.get_empty_space_after_entry(self.winning_hands[i]) + self.symbols["vbar"]
            for tier in self.tiers:
                reward = str(tier * self.scaling[i])
                sclt += reward + " "*self.get_empty_space_after_entry(reward) + self.symbols["vbar"]
            sclt += "\n"
        sclt += self.symbols["4"] + self.symbols["hbar"]*(self.board_width) + self.symbols["3"] + "\n"
        return sclt

    def get_empty_space_after_entry(self, entry):
        return self.cell_width - len(entry)

if __name__ == "__main__":
    sb = ScoreBoard([15,12], None)
    print(sb.get_scoreboard_sceleton())