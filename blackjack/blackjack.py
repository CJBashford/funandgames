import random
from IPython.display import clear_output
from time import sleep



cards = {'Ace of Spades': 11, '2 of Spades': 2, '3 of Spades': 3, '4 of Spades': 4, '5 of Spades': 5, '6 of Spades': 6, 
        '7 of Spades': 7, '8 of Spades': 8, '9 of Spades': 9, '10 of Spades': 10, 'Jack of Spades': 10, 'Queen of Spades': 10,
       'King of Spades': 10,
        
        'Ace of Hearts': 11, '2 of Hearts': 2, '3 of Hearts': 3, '4 of Hearts': 4, '5 of Hearts': 5, '6 of Hearts': 6, 
        '7 of Hearts': 7, '8 of Hearts': 8, '9 of Hearts': 9, '10 of Hearts': 10, 'Jack of Hearts': 10, 'Queen of Hearts': 10,
       'King of Hearts': 10,
        
        'Ace of Diamonds': 11, '2 of Diamonds': 2, '3 of Diamonds': 3, '4 of Diamonds': 4, '5 of Diamonds': 5, '6 of Diamonds': 6, 
        '7 of Diamonds': 7, '8 of Diamonds': 8, '9 of Diamonds': 9, '10 of Diamonds': 10, 'Jack of Diamonds': 10, 'Queen of Diamonds': 10,
       'King of Diamonds': 10,
        
        'Ace of Clubs': 11, '2 of Clubs': 2, '3 of Clubs': 3, '4 of Clubs': 4, '5 of Clubs': 5, '6 of Clubs': 6, 
        '7 of Clubs': 7, '8 of Clubs': 8, '9 of Clubs': 9, '10 of Clubs': 10, 'Jack of Clubs': 10, 'Queen of Clubs': 10,
       'King of Clubs': 10}



class Pot:

    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.insurance_bet_balance = 0
        self.split_wager_balance = 0

    def empty_pot(self):

        """
        
        Empties the pot and resets, ready for the next round of play.

        """

        self.balance = 0
        self.insurance_bet_balance = 0
        self.split_wager_balance = 0


    def double_down(self):

        """
        
        Doubles the current pot wager when the bettor requests to double down on their hand.

        """

        self.balance = self.balance * 2



class Player:    

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.balance = 1000
        self.score = 0
        self.opening_wager = 0
        self.insurance_wager = 0
        self.split_wager = 0
        self.round_winnings = 0
        self.has_card_split = False
        self.surrendered = False
    


    def reset(self):
        
        """
        
        Removes all cards currently in the hand of a player at the start of the game and sets their score to 0.
        
        """
        
        self.hand = []
        self.score = 0
        self.opening_wager = 0
        self.insurance_wager = 0
        self.split_wager = 0
        self.round_winnings = 0
        self.has_card_split = False
        self.surrendered = False
    


    def show_hand(self):
        
        """
        
        Shows the cards currently in the hand of the player and prints this to the terminal.
        
        """
        
        print(f"{self.name}\'s hand is: {self.hand}")
        sleep(2)
    


    def draw_card(self):
        
        """
        
        Takes an additional card from the top of the deck and adds it to the current hand.
        
        """

        global deck
        self.hand.append(deck[-1])
        deck.pop()
        print(f"{self.name} drew the {self.hand[-1]}")
        self.show_hand()
    


    def place_wager(self, wager_type):
        
        """
        
        Places a wager on the next hand. User input is validated to check that the wager is both within the
        minimum and maximum wagering boundaries specified, as well as whether the current balance allows the
        wager to be placed. Takes the parameter wager_type, which specifies whether the wager is being placed at the beginning of the hand,
        or whether the wager is being placed as part of an insurance bet.
        
        Returns: an integer value for the amount wagered
        
        """

        minimum_bet = 2
        maximum_bet = 500
        
        if wager_type == "opening":
            while True:
                    print("Would you like to play with high or low stakes?")
                    stakes = input("High or Low Stakes (y/n): ").upper()
                    if stakes not in ["Y","N"]:
                        print("Invalid input")
                        continue
                    elif stakes == 'Y':
                        minimum_bet = 100
                        maximum_bet = 1000
                        print("High stakes chosen. Minimum bet per hand is now £100, maximum bet per hand is now £1000.")
                        break
                    else:
                        print("Low stakes chosen. Minimum bet per hand remains at £2, maximum bet per hand remains at £500")
                        break

            while True:
                try:
                    print(f"Your balance is: £{self.balance}")
                    wager = int(input("Wager Amount: £"))
                except ValueError:
                    print("Invalid number provided")
                    continue
                if wager < minimum_bet or wager > maximum_bet:
                    print("Please place a wager within the min/max wager boundaries")
                    continue
                elif (self.balance - wager) < 0:
                    print("Invalid balance available to place this wager")
                else:
                    break
            
            self.balance -= wager
            print(f"Your balance is now: £{self.balance}")
            pot.balance += wager
            print(f"The pot this round is now: £{pot.balance}")
            self.opening_wager += wager
            sleep(2)
            return wager

        elif wager_type == "insurance":
            wager_this_hand = self.opening_wager
            insurance_wager = wager_this_hand / 2
            self.balance -= insurance_wager
            print(f"Your balance is now: £{self.balance}")
            pot.insurance_bet_balance += insurance_wager
            print(f"The insurance pot this round is now: £{pot.insurance_bet_balance}")
            self.insurance_wager += insurance_wager
            sleep(2)
            return insurance_wager

        elif wager_type == "split":
            split_wager = self.opening_wager
            self.balance -= split_wager
            print(f"Your balance is now: £{self.balance}")
            pot.split_wager_balance += split_wager
            print(f"The split wager pot this round is now: £{pot.split_wager_balance}")
            self.split_wager += split_wager
            sleep(2)
            return split_wager

        else:
            pass


    def compute_score(self, hand):
        
        """
        
        Computes the current cumulative score for the cards held in the individuals hand.
    
        Returns:
        int: returns an integer value for the current total of the cards held in the hand.
    
        """

        values = []
        self.score = 0
        for i in hand:
            val = cards.get(i)
            values.append(val)
        for j in values:
            self.score += j
        substring = "Ace"
        ace_in_hand = any(substring in string for string in hand)
        if self.score > 21 and ace_in_hand:
            self.score -= 10
        return self.score
    


    def show_score(self, hand):
        
        """
        
        Shows a player's current score.
        
        """
        hand_score = self.compute_score(hand)
        print(f"{self.name}\'s score is: {hand_score}")
    


    def __str__(self):
        
        return self.name



    def surrender(self):

        """

        Gives player the option to surrender if they do not like their hand, and receive half of their bet back.

        """

        self.surrendered = True



    def double_down(self):

        """

        Gives player the option to double down on their bet and double their wager if they feel their hand is advantageous. They then receive one additional card only."

        """

        self.balance -= self.wager_this_hand
        print(f"{self.name} is confident in their hand and opts to double down on the bet!")
        print(f"Additional Wager Amount: £ {self.opening_wager}")
        print(f"Your balance is now: £{self.balance}")
        self.opening_wager += self.opening_wager
        pot.double_down()
        print(f"The pot this round is now: £{pot.balance}")
        sleep(2)
        self.draw_card()
        self.compute_score(self.hand)
        self.show_score(self.hand)



    def can_split(self):

        """

        Evaluates to true or false based on whether the player can split based on the two cards they are initially dealt having the same value.
        Player is allowed to split so long as pip/face value is the same, not limited by rank being the same.

        """

        values = []
        for i in self.hand:
            val = cards.get(i)
            values.append(val)
        if values[0] == values[1]:
            return True
        else:
            return False


class Dealer(Player):
    
    def __init__(self, name):
        super().__init__(name)
        self.balance = 5000
        self.round_payouts = 0
    


    def reset(self):
        super().reset()
        self.round_payouts = 0



    def dealer_draw(self):
        
        """

        Draws a card for the dealer.

        """

        print(f"{self.name} score is less than 17. {self.name} must draw a card")
        self.draw_card()
        self.compute_score(self.hand)
        print(f"{self.name}\'s score is: {self.score}")
    


    def show_partial_hand(self):
        
        """
        
        Shows one card in the dealer's hand and one hidden card at the beginning of the game.
        
        """
        
        print(f"{self.name}\'s hand is: {self.hand[:-1]} + ???")
        sleep(2)
    


    def compute_partial_score(self):
        
        """
        
        Calculates the score of the dealer's hand minus the hidden card.
        
        """
        
        dealer_score = self.compute_score()
        dealer_hidden_card_val = cards.get(self.hand[-1])
        dealer_hidden_score = dealer_score - dealer_hidden_card_val
        print(f"{self.name}\'s score is: {dealer_hidden_score} + ???")



    def up_card_is_ace(self):

        """

        Returns true if the dealer's up card is an ace, triggering choice for the player on whether to take an insurance bet.

        """

        first_card = self.hand[0]
        substring = "Ace"
        if substring in first_card:
            return True
        else:
            return False



class Scoreboard:

    def __init__(self):
        self.hands_played = 0
        self.player_wins = 0
        self.house_wins = 0
        self.rounds_drawn = 0
        self.total_player_wagers = 0
        self.total_player_winnings = 0
        self.total_house_winnings = 0
        self.total_house_payouts = 0



    def reset(self):

        """

        Resets scoreboard at the beginning of a new session of play.

        """

        self.hands_played = 0
        self.player_wins = 0
        self.house_wins = 0
        self.rounds_drawn = 0
        self.total_player_wagers = 0
        self.total_player_winnings = 0
        self.total_house_winnings = 0
        self.total_house_payouts = 0



    def show(self):

        """

        Shows the scoreboard at the end of each round.

        """

        sleep(2)
        print("***** SCOREBOARD *****")
        print("*** HAND OUTCOMES ***")
        if self.player_wins == 1:
            print(f"{gambler.name} has won {self.player_wins} hand.")
        else:
            print(f"{gambler.name} has won {self.player_wins} hands.")
        if self.house_wins == 1:
            print(f"{dealer.name} has won {self.house_wins} hand.")
        else:
            print(f"{dealer.name} has won {self.house_wins} hands.")
        if self.rounds_drawn == 1:
            print(f"{self.rounds_drawn} hand has ended in a push.")
        else:
            print(f"{self.rounds_drawn} hands have ended in a push.")
        sleep(2)
        print("*** BET OUTCOMES ***")
        print(f"{gambler.name} has placed wagers totalling £{self.total_player_wagers} and won a total of £{self.total_player_winnings} this session.")
        print(f"{gambler.name} has a net profit/loss of £{self.total_player_winnings - self.total_player_wagers} this session.")
        print(f"{dealer.name} has a net profit/loss of £{self.total_house_winnings - self.total_house_payouts} this session.")



# Initializing class variables to play game.
gambler = Player('Connor')
dealer = Dealer('Dealer')
pot = Pot('Casino')
scoreboard = Scoreboard()



def game_reset():

    """

    Resets the game.

    """

    clear_output()
    gambler.reset()
    dealer.reset()
    pot.empty_pot()



def create_deck():
    
    """
    
    Creates a deck of 52 playing cards using the keys in the cards dictionary, and shuffles them.
    
    """
    
    global deck
    deck = list(cards.keys())
    random.shuffle(deck)



def deal():
    
    """
    
    Assigns an empty list variable for both the player and the dealer, then populates this empty list with
    cards drawn from the top of the deck to generate a hand for the player.
    This function is used at the start of the game to deal the initial two cards to each player, with the dealer
    dealt cards last.
    
    """
    
    print("The cards are dealt, welcome to Blackjack!")
    sleep(2)
    counter = 0
    while (counter < 2):
        gambler.hand.append(deck[-1])
        deck.pop()
        dealer.hand.append(deck[-1])
        deck.pop()
        counter += 1



def stick_or_twist():
    
    """

    Operates the stick/twist loop within the game.

    """

    if gambler.score == 21:
        choice = "stick"
    else:
        choice = input("stick, twist, surrender or double down? ").lower()
        if choice == "surrender":
            gambler.surrender()
            endgame()
        elif choice == "double down":
            if gambler.balance > pot.balance:
                gambler.double_down()
            else:
                print("Insufficient balance to double down on your bet")
                choice = input("stick or twist? ").lower()
                while choice == "twist":
                    gambler.draw_card()
                    gambler.compute_score(gambler.hand)
                    gambler.show_score(gambler.hand)
                    if gambler.score == 21:
                        print(f"{gambler.name} got a blackjack!")
                        break
                    elif gambler.score > 21:
                        print(f"{gambler.name} is bust!")
                        break
                    else:
                        choice = input("stick or twist? ")
                        if choice == "twist":
                            dealer.show_hand()
                            dealer.show_score(dealer.hand)
                            sleep(2)
                        else:
                            break
        else:
            while choice == "twist":
                gambler.draw_card()
                gambler.compute_score(gambler.hand)
                gambler.show_score(gambler.hand)
                sleep(2)
                if gambler.score == 21 and len(gambler.hand) == 2:
                    print(f"{gambler.name} got a blackjack!")
                    break
                elif gambler.score == 21:
                    choice == "stick"
                elif gambler.score > 21:
                    print(f"{gambler.name} is bust!")
                    break
                else:
                    choice = input("stick or twist? ")



def dealer_play():

    """

    Determines the action the dealer takes after the player is finished.

    """

    dealer.show_hand()
    dealer.show_score(dealer.hand)
    sleep(2)
    while dealer.score < 17:
        dealer.dealer_draw()
        sleep(2)
    if dealer.score == 21 and len(dealer.hand) == 2:
        print(f"{dealer.name} has a blackjack!")
        sleep(2)
    elif dealer.score > 21:
        print(f"{dealer.name} is bust!")
        sleep(2)
    elif dealer.score >= 17 and dealer.score <= 21:
        print(f"{dealer.name} must stand.")
        sleep(2)
    else:
        pass



def place_insurance():

    """

    Allows the player the option to take an insurance bet against the house having a blackjack if the dealer's up card is an Ace.

    """

    if gambler.balance >= gambler.opening_wager / 2:
        while True:
                print("Dealer has an ace. Would you like to take an insurance bet?")
                insurance_bet = input("Place Insurance Bet yes/no: ").upper()
                if insurance_bet not in ["YES", "NO"]: 
                    print("Invalid input")
                    continue
                elif insurance_bet == 'NO':
                    break
                else:
                    gambler.place_wager("insurance")
                    break
    else:
        print(f"{dealer.name} has an ace. However, you do not have sufficient remaining balance to make an insurance bet")



def settle_insurance():

    """

    Settles insurance bets if any have been placed.

    """

    if gambler.insurance_wager > 0:
        if dealer.score == 21 and len(dealer.hand) == 2:
            # Winning insurance bet where dealer has blackjack
            insurance_payout = gambler.insurance_wager * 2
            dealer.balance -= insurance_payout
            dealer.round_payouts += insurance_payout
            pot.insurance_bet_balance += insurance_payout
            gambler.balance += pot.insurance_bet_balance
            gambler.round_winnings += pot.insurance_bet_balance
            pot.insurance_bet_balance = 0
            print(f"{dealer.name} had blackjack. {gambler.name} wins their insurance bet, paid out at 2/1 odds.")
            print(f"{gambler.name}\'s balance is now £{gambler.balance}")
            print(f"The house balance is now £{dealer.balance}")
        else:
            # Losing insurance bet where dealer does not have blackjack
            dealer.balance += gambler.insurance_wager
            dealer.round_winnings += gambler.insurance_wager
            print(f"Dealer does not have blackjack. {gambler.name} loses their insurance bet this round.")
            print(f"{gambler.name} lost £{gambler.insurance_wager} on this insurance bet.")
            print(f"The house balance is now £{dealer.balance}")
    else:
        print("No insurance bets this hand")



def basic_victory():

    """

    Set of actions that occur in several scenarios that result in a generic victory.

    """

    sleep(2)
    dealer.balance -= pot.balance
    dealer.round_payouts += pot.balance
    pot.balance = pot.balance * 2
    winnings = pot.balance
    gambler.balance += winnings
    gambler.round_winnings += winnings
    print(f"{gambler.name} won £{winnings} on this hand.")
    print(f"{gambler.name}\'s balance is now £{gambler.balance}")
    print(f"The house balance is now £{dealer.balance}")



def basic_loss():

    """

    Set of actions that occur in several scenarios that result in a generic loss.

    """

    sleep(2)
    dealer.balance += pot.balance
    dealer.round_winnings += pot.balance
    print(f"{gambler.name} lost £{pot.balance} on this hand.")
    print(f"{gambler.name}\'s balance is now £{gambler.balance}")
    print(f"The house balance is now £{dealer.balance}")



def jackpot(result):
    
    """
    
    Pays out in the event the player wins.
    
    """
    
    if result == "blackjack":
        print("BLACKJACK!!!!! You win! Congratulations!")
        sleep(2)
        # Getting blackjack pays out at 3/2 odds vs regular wins at Evens
        winnings = pot.balance * 1.5
        stake = pot.balance
        payout = winnings + stake
        dealer.balance -= winnings
        gambler.balance += payout
        gambler.round_winnings += payout
        dealer.round_payouts += payout
        print(f"{gambler.name} won £{payout} on this hand.")
        print(f"{gambler.name}\'s balance is now £{gambler.balance}")
        print(f"The house balance is now £{dealer.balance}")
    elif result == "21 no blackjack":
        print("You got 21 and beat the dealer! You win! Congratulations!")
        basic_victory()
    elif result == "dealer bust":
        print("The dealer is bust but you are not! You win! Congratulations!")
        basic_victory()
    elif result == "closest wins":
        print("You were closer to 21 than the dealer! You win! Congratulations!")
        basic_victory()
    else:
        pass
    pot.empty_pot()



def loss(result):

    """
    
    Handles endgame scenario where player loses

    """

    if result == "surrender":
        print(f"Game aborted! {gambler.name} surrendered")
        sleep(2)
        shared_spoils = pot.balance * 0.5
        gambler.balance += shared_spoils
        dealer.balance += shared_spoils
        dealer.round_winnings += shared_spoils
        gambler.round_winnings += shared_spoils
        print(f"{gambler.name} lost £{pot.balance * 0.5} on this hand.")
        print(f"{gambler.name}\'s balance is now £{gambler.balance}")
        print(f"The house balance is now £{dealer.balance}")
    elif result == "bust":
        # You are bust, house always wins
        print("Bust! You lose! House wins.")
        basic_loss()
    elif result == "close but no cigar":
        # Neither is bust, but dealer is closer than you
        print("You lose! The dealer was closer to 21 than you. House wins.")
        basic_loss()
    elif result == "push":
        # Bet ends in a push
        print("Bet ends in a push. Bets will be refunded. No action this round.") # your score is tied with the dealer
        sleep(2)
        refund = pot.balance
        gambler.balance += refund
        gambler.winnings += refund
        print(f"{gambler.name} is refunded £{refund} on this hand.")
        print(f"{gambler.name}\'s balance is now £{gambler.balance}")
    else:
        pass
    pot.empty_pot()



def update_scoreboard(result):

    """

    Updates the scoreboard at the end of the round.

    """

    losses = ["surrender", "bust", "close but no cigar"]
    wins = ["blackjack", "21 no blackjack", "dealer bust", "closest wins"]
    pushes = ["push"]

    scoreboard.hands_played += 1
    scoreboard.total_player_wagers += gambler.opening_wager
    scoreboard.total_player_wagers += gambler.insurance_wager
    scoreboard.total_player_winnings += gambler.round_winnings
    scoreboard.total_house_winnings += dealer.round_winnings
    scoreboard.total_house_payouts += dealer.round_payouts

    if result in losses:
        scoreboard.house_wins += 1
    elif result in wins:
        scoreboard.player_wins += 1
    elif result in pushes:
        scoreboard.rounds_drawn += 1
    else:
        pass



def split_cards():

    """
    
    Handles the splitting of cards if the player chooses to do so.

    """

    if gambler.balance > gambler.opening_wager / 2:
        while True:
            print(f"{gambler.name} is dealt two cards of the same value, and can choose to split the cards into two new hands.")
            split = input("Split cards? yes/no: ").upper()
            if split not in ["YES", "NO"]: 
                print("Invalid input")
                continue
            elif split == 'NO':
                break
            else:
                gambler.has_card_split = True
                gambler.second_hand = [] # Initializing a second hand for the player when they split cards.
                gambler.second_hand.append(gambler.hand[1])
                gambler.hand.pop(1)
                gambler.place_wager("split")
                gambler.hand.append(deck[-1])
                deck.pop()
                gambler.second_hand.append(deck[-1])
                deck.pop()
                first_hand_score = gambler.compute_score(gambler.hand)
                gambler.show_score(gambler.hand)
                second_hand_score = gambler.compute_score(gambler.second_hand)
                gambler.show_score(gambler.second_hand)






    else:
        print(f"{gambler.name} is dealt two cards of the same value. However, you do not have sufficient remaining balance to split the hand.")


def endgame():

    """
    
    Handles the endgame scenarios and triggers jackpot or loss scenarios based on the outcome of the game.

    """

    if surrendered == True:
        result = "surrender"
        loss(result)
    else:
        print(f"Your final score is {gambler.score}. Dealer's final score is {dealer.score}.")
        sleep(2)
        settle_insurance()
        sleep(2)

        if gambler.score == 21 and dealer.score != 21 and len(gambler.hand) == 2:
            result = "blackjack"
            jackpot(result)
        elif gambler.score == 21 and dealer.score != 21 and len(gambler.hand) > 2:
            result = "21 no blackjack"
            jackpot(result)
        elif 21 - gambler.score < 0: # you are bust, house always wins
            result = "bust"
            loss(result)
        elif 21 - gambler.score >= 0 and 21 - dealer.score < 0: # you are not bust, house is bust, you win
            result = "dealer bust"
            jackpot(result)
        elif 21 - gambler.score < 21 - dealer.score: # neither is bust, but you are closer than dealer
            result = "closest wins"
            jackpot(result)
        elif 21 - gambler.score > 21 - dealer.score: # neither is bust, but dealer is closer than you
            result = "close but no cigar"
            loss(result)
        else:
            result = "push"
            loss(result)
    update_scoreboard(result)
    scoreboard.show()
    sleep(2)



def blackjack():
    
    """
    
    Plays the game of Blackjack. The deck is created at the beginning of the session. If at the beginning of a new
    hand, the deck has 10 or less cards remaining, the deck is rebuilt and a new pack of 52 cards used.
    
    """

    create_deck()
    scoreboard.reset()
    play_again = "y"
    while play_again == "y":
        game_reset()
        if len(deck) <= 10:
            create_deck()
            print("The deck is running low on cards. The dealer introduces a new set of 52.")
            sleep(2)
        gambler.place_wager("opening")
        deal()
        gambler.show_hand()
        gambler.compute_score()
        gambler.show_score()
        dealer.show_partial_hand()
        dealer.compute_partial_score()
        if gambler.can_split():
            split_cards()
        else:
            pass
        if dealer.up_card_is_ace() and not gambler.has_card_split():
            place_insurance()
        else:
            pass
        if not gambler.has_card_split():
            stick_or_twist()
        else:
            pass
        sleep(2)
        if gambler.surrendered():
            dealer_play()
            endgame()
        if gambler.balance == 0:
            print("Out of money, game over!")
            play_again = "n"
        else:
            play_again = input("Would you like to play another hand? Enter y to play again ")



def main():
    blackjack()



if __name__ == "__main__":
    main()