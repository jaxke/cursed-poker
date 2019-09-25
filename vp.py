import curses
import math
from random import randrange
import CardDrawer

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
#curses.nocbreak()
#stdscr.keypad(False)
#curses.echo()

suites = ["clubs", "diamonds", "hearts", "spades"]
dims = [15, 12]

'''
    will lose:
    high (guaranteed):  returns the highest card               
    pair:               pair of 2-10

    will result in draw:
    jacks or better:    pair of 11-14

    will win:
    two pairs:          any 2 "pair"s
    three of a kind:    3 cards of same value
    straight:           all 5 cards are in any subsequential order
    flush:              all 5 cards have the same suite
    full house:         "three of a kind" and "pair"
    four of a kind:     4 cards of same value
    straight flush:     "flush" and "straigh"
    royal flush:        "flush" and ace high

'''
def rank_hand(hand):
    high = 0
    hand_ranking = {}
    cards_having_rank = []

    for card in hand:
        if int(card[0]) > high:
            high = int(card[0])

    vals = sorted([int(card[0]) for card in hand])
    for val in vals:
        occurences_of_val = vals.count(val)
        if occurences_of_val >= 2:
            if occurences_of_val == 2:
                if val >= 11 or val == 1:
                    hand_ranking[val] = "jacks or better"
                else:
                    hand_ranking[val] = "low pair"
            elif occurences_of_val == 3:
                hand_ranking[val] = "three of a kind"
            elif occurences_of_val == 4:
                hand_ranking[val] = "four of a kind"

    for i in range(1, len(vals)):
        #import pdb; pdb.set_trace()
        if not vals[i]-1 == vals[i-1]:
            break
        if i == len(vals)-1:
            hand_ranking[val] = "straight"

    if "three of a kind" in hand_ranking and ("low_pair" in hand_ranking or "jacks or better" in hand_ranking):
        hand_ranking = {0: "full house"}
    
    if not hand_ranking:
        hand_ranking[high] = "high"

    return hand_ranking



def print_hand(hand, scr):
    hand_display = CardDrawer.CardDrawer().get_hand(hand, dims)
    scr.addstr(0, 0, hand_display, curses.A_REVERSE)
    scr.refresh()


# TODO change name, shadows additional class
def draw_cards(n):
    cards = []
    if False:  #DEBUG
        return [[1, "diamonds"], [1, "spades"], [3, "clubs"], [4, "hearts"], [4, "diamonds"]]
    for i in range(n):
        suite = suites[randrange(3)]
        value = randrange(1, 14)
        cards.append([value, suite])
    return cards


def update_held(held, scr):
    stdscr.addstr(dims[1], 0, " "* 5*(dims[0]+4), curses.A_REVERSE)
    holdstr = ""
    for i in range(0, 5):
        if held and i in held:
            holdstr += "HOLD" + " "*dims[0]
        else:
            holdstr += " " *(dims[0]+4)  
    stdscr.addstr(dims[1], 0, holdstr, curses.A_REVERSE)
    scr.refresh()



def main():
    cards = draw_cards(5)
    print_hand(cards, stdscr)
    ranked = rank_hand(cards)
    stdscr.addstr(dims[0], 0, " ".join(list(ranked.values())), curses.A_REVERSE)
    stdscr.refresh()
    held = []
    while True:
        c = stdscr.getch()
        if c >= 49 and c <= 53 or c in [97, 115, 100, 102, 103]:
            if c == ord('1') or c == ord('a'):
                if 0 in held:
                    held.remove(0)
                else:
                    held.append(0)

            elif c == ord('2') or c == ord('s'):
                if 1 in held:
                    held.remove(1)
                else:
                    held.append(1)

            elif c == ord('3') or c == ord('d'):
                if 2 in held:
                    held.remove(2)
                else:
                    held.append(2)

            elif c == ord('4') or c == ord('f'):
                if 3 in held:
                    held.remove(3)
                else:
                    held.append(3)

            elif c == ord('5') or c == ord('g'):
                if 4 in held:
                    held.remove(4)
                else:
                    held.append(4)

            update_held(held, stdscr)

        if c == ord(' '):
            drawn_cards = draw_cards(5 - len(held))
            for i in range(len(cards)-1):
                if i not in held:
                    cards[i] = drawn_cards[-1]
                    drawn_cards.pop(-1)

            print_hand(cards, stdscr)
            ranked = rank_hand(cards)
            stdscr.move(2, 0)
            stdscr.clrtoeol()
            stdscr.addstr(dims[0], 0, " ".join(list(ranked.values())), curses.A_REVERSE)
            update_held(None, stdscr)

            if 

        if c == ord('q'):
            break

if __name__ == "__main__":
    main()
