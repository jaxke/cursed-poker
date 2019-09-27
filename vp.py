import curses
import math
from random import randrange
import CardDrawer
import ScoreBoard
import time



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

'''
    hand: [[1, 'diamonds'], [1, 'spades'], [3, 'clubs'], [4, 'hearts'], [4, 'diamonds']]
'''

class Main:
    suites = ["clubs", "diamonds", "hearts", "spades"]
    card_names = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    dims = [15, 12]
    scr = None

    ylocation_scoreboard = 0
    ylocation_cards = 0
    ylocation_hold = 0
    location_tokens = [0,0]
    location_bet = [0,0]

    scoreboard = None
    tokens = 50
    bet_tiers = [1, 5, 10]

    def __init__(self, stdscr):
        self.scr = stdscr
        self.scoreboard = ScoreBoard.ScoreBoard(self.dims, self.scr)
        self.ylocation_cards = self.scoreboard.get_scoreboard_height() + 1
        self.ylocation_hold = self.ylocation_cards + self.dims[1]
        self.location_tokens = [0, self.ylocation_hold + 1]
        self.location_bet = [self.dims[0] - 3, self.ylocation_hold + 1]
        self.main()

    def rank_hand(self, hand):
        high = 0
        hand_ranking = {}
        cards_having_rank = []

        for card in hand:
            if int(card[0]) == 1:
                high = 1
                break
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

        suites = [card[1] for card in hand]
        if suites.count(suites[0]) == len(hand):
            hand_ranking = {high: "flush"}
            if high == 1:
                return "royal flush"
        
        if "three of a kind" in list(hand_ranking.values()) and ("low pair" in list(hand_ranking.values()) or "jacks or better" in list(hand_ranking.values())):
            return "full house"
        elif list(hand_ranking.values()).count("low pair") + list(hand_ranking.values()).count("jacks or better") == 2:
            return "two pairs"
        elif "low pair" in list(hand_ranking.values()):
            return "low pair"    
        elif "jacks or better" in list(hand_ranking.values()):
            return "jacks or better"
        elif "three of a kind" in list(hand_ranking.values()):
            return "three of a kind"

        for i in range(1, len(vals)):
            if not vals[i]-1 == vals[i-1]:
                break
            if i == len(vals)-1:
                if "flush" in list(hand_ranking.values()):
                    return "straigh flush"
                else:
                    return "straight"
        
        if "flush" in list(hand_ranking.values()):
            return "flush"
        elif "four of a kind" in list(hand_ranking.values()):
            return "four of a kind"
        
        if not hand_ranking:
            return self.card_names[high-1] + " high"

    def print_hand(self, hand):
        if not hand:
            hand_display = CardDrawer.CardDrawer().get_hand_of_empty_cards(self.dims)
        else:
            hand_display = CardDrawer.CardDrawer().get_hand(hand, self.dims)
        self.scr.addstr(self.ylocation_cards, 0, hand_display, curses.A_REVERSE)
        self.scr.refresh()


    # TODO change name, shadows additional class
    # Take in existing cards so there's no collision (there can only be 1 card of same value&suite)
    def draw_cards(self, n, existing_cards):
        cards = []
        if False:  #DEBUG
            return [[11, "hearts"], [11, "clubs"], [11, "hearts"], [10, "hearts"], [10, "clubs"]]
        
        # Can't do it in for loop because we can't reset the loop without incrementing the iterator
        i = 0
        while i < n:
            suite = self.suites[randrange(3)]
            value = randrange(1, 14)
            # Checks for collision between cards that are drawn now or were part of player's entire hand (including the cards that will be discarded)
            if [value, suite] in cards or (existing_cards and [value, suite] in existing_cards):
                continue
            cards.append([value, suite])
            i += 1
        return cards


    def update_held(self, held):
        self.scr.addstr(self.ylocation_hold, 0, " "* 5*(self.dims[0]+4), curses.A_STANDOUT)
        holdstr = ""
        for i in range(0, 5):
            if held and i in held:
                holdstr += "HOLD" + " "*self.dims[0]
            else:
                holdstr += " " *(self.dims[0]+4)  
        self.scr.addstr(self.ylocation_hold, 0, holdstr, curses.A_STANDOUT)
        self.scr.refresh()

    def print_token_information(self):
        self.scr.addstr(self.location_bet[1], self.location_bet[0], "TOKENS: " + str(self.tokens), curses.A_BOLD)
        

    def print_bet_information(self, bet):
        # TODO fix this space issue
        self.scr.addstr(self.location_tokens[1], self.location_tokens[0], "BET: " + str(bet) + " ", curses.A_BOLD)
        self.scr.refresh()


    def shuffle(self, hand):
        # "Shuffle animation" 4 times
        for i in range(4):
            random_hand = []
            # 5 cards per hand
            for j in range(5):
                random_hand.append([randrange(14), self.suites[randrange(4)]])
            self.print_hand(random_hand)
            time.sleep(0.2)
            self.print_hand(None)
            if i != 3:
                time.sleep(0.2)
        
        tmp_hand = [[0,0], [0,0], [0,0], [0,0], [0,0]]
        for i in range(5):
            tmp_hand[i] = hand[i]
            if i == 4:
                time.sleep(0.85)
            else:
                time.sleep(0.35)
            self.print_hand(tmp_hand)
        self.print_hand(hand)

    def increase_bet(self, old_bet):
        bet = 0
        if old_bet == 1:
            bet = 5
        elif old_bet == 5:
            bet = 10
        else:
            bet = 1
        self.print_bet_information(bet)
        return bet
                
    # TODO add "deal" function to remove repetition, it should function in both re-deal and drawing new cards to hand

    def main(self):
        bet = 1
        self.scoreboard.draw_to_scr(None)
        self.print_hand(None)

        self.print_token_information()
        self.print_bet_information(bet)

        # Wait for the user input before dealing
        c = self.scr.getch()
        while c != ord(" "):
            if c == ord('q'):
                return
            elif c == ord('b'):
                bet = self.increase_bet(bet)
            
            c = self.scr.getch()

        while True:
            self.tokens -= bet
            self.print_token_information()
            cards = self.draw_cards(5, None)
            ranked = self.rank_hand(cards)
            # Even if we've got the cards already, don't reveal the rank before cards are shuffled
            self.scoreboard.draw_to_scr(None)
            self.print_hand(None)
            self.shuffle(cards)
            self.scoreboard.draw_to_scr(ranked)
            held = []

            c = self.scr.getch()

            while c >= 49 and c <= 53 or c in [97, 115, 100, 102, 103]:
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

                self.update_held(held)
                c = self.scr.getch()

            # Space bar is "Deal"
            if c == ord(' '):
                tmp_hand = []
                # The cards that are re-dealt
                drawn_cards = self.draw_cards(5 - len(held), cards)
                for i in range(len(cards)):
                    if i not in held:
                        tmp_hand.append([0,0])
                        cards[i] = drawn_cards[-1]
                        drawn_cards.pop(-1)
                    else:
                        tmp_hand.append(cards[i])

                self.print_hand(tmp_hand)
                self.scr.refresh()
                for i in range(len(tmp_hand)):
                    if tmp_hand[i] == [0,0]:
                        for j in range(2):
                            tmp_hand[i] = [randrange(14), self.suites[randrange(4)]]
                            self.print_hand(tmp_hand)
                            time.sleep(0.1)
                            tmp_hand[i] = [0,0]
                            self.print_hand(tmp_hand)
                            time.sleep(0.1)
                        tmp_hand[i] = cards[i]
                        self.print_hand(tmp_hand)
                        time.sleep(0.2)
                        

                self.print_hand(cards)
                ranked = self.rank_hand(cards)
                self.scoreboard.draw_to_scr(ranked)
                held = []
                self.update_held(None)

                # Lower than "jacks or better" is a loss, credits are already deduced.
                if ranked == "low pair" or "high" in ranked:
                    pass
                # Refund bet at draw
                elif ranked == "jacks or better":
                    self.tokens += bet
                    self.print_token_information()
                else:
                    self.tokens += self.scoreboard.get_reward(bet, ranked)
                    self.print_token_information()

                c = self.scr.getch()
                while c != ord(' '):
                    if c == ord('b'):
                        bet = self.increase_bet(bet)
                    elif c == ord('q'):
                        return
                    c = self.scr.getch()

            

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    #curses.nocbreak()
    #stdscr.keypad(False)
    #curses.echo()
    main = Main(stdscr)
