
import curses

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
    board_skeleton = ""

    def __init__(self, dims, scr):
        self.cell_width = max([len(hand) for hand in self.winning_hands])+1
        #scr.addstr(0, 0, self.get_scoreboard_sceleton(dims), curses.A_REVERSE)
        self.dims = dims
        self.scr = scr
        # cell width * number of columns + 2 vbars + number of columns-1 (the separator of each tier)
        self.board_width = (len(self.tiers)+1)*self.cell_width + 2 + len(self.tiers)-2
        self.board_skeleton = self.get_scoreboard_sceleton()

    def get_reward(self, bet, rank):
        return bet * self.scaling[self.winning_hands.index(rank)]

    def get_scoreboard_height(self):
        return 2 + len(self.winning_hands)

    def get_scoreboard_sceleton(self):
        sclt = self.symbols["1"] + self.symbols["hbar"]*(self.board_width) + self.symbols["2"] + "\n"
        for i in reversed(range(len(self.winning_hands))):
            sclt += self.symbols["vbar"] + self.winning_hands[i] + " "*self.get_empty_space_after_entry(self.winning_hands[i]) + self.symbols["vbar"]
            for tier in self.tiers:
                reward = str(tier * self.scaling[i])
                sclt += reward + " "*self.get_empty_space_after_entry(reward) + self.symbols["vbar"]
            sclt += "\n"
        sclt += self.symbols["4"] + self.symbols["hbar"]*(self.board_width) + self.symbols["3"] + "\n"
        return sclt

    def get_empty_space_after_entry(self, entry):
        return self.cell_width - len(entry)

    # We are going to draw the board here and we need the player's highest rank (if above low pair) which will be highlighted.
    def draw_to_scr(self, hand_rank):
        for i, line in enumerate(self.board_skeleton.split("\n")):
            if i == 0:
                self.scr.addstr(i, 0, line, curses.A_DIM)
            elif i == len(self.winning_hands)+1:
                self.scr.addstr(i, 0, line, curses.A_DIM)
                break
            # Reversed winning_hands because the scoreboard is drawn "upside-down"
            elif hand_rank and hand_rank == self.winning_hands[::-1][i-1]:
                for j, c in enumerate(line):
                    if c != self.symbols["vbar"]:
                        self.scr.addstr(i, j, c, curses.A_REVERSE)
                    else:
                        self.scr.addstr(i, j, c, curses.A_DIM)
            else:
                self.scr.addstr(i, 0, line, curses.A_DIM)


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    sb = ScoreBoard([15,12], stdscr)
    a=sb.get_scoreboard_sceleton()
    sb.draw_to_scr(None)
    c = stdscr.getch()
    if c == ord('q'):
        import sys; sys.exit()
    while True:
        pass