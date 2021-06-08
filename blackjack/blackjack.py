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

    def empty_pot(self):

        """
        
        Empties the pot and resets, ready for the next round of play.

        """

        self.balance = 0


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
    


    def reset(self):
        
        """
        
        Removes all cards currently in the hand of a player at the start of the game and sets their score to 0.
        
        """
        
        self.hand = []
        self.score = 0
    


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
    


    def place_wager(self):
        
        """
        
        Places a wager on the next hand. User input is validated to check that the wager is both within the
        minimum and maximum wagering boundaries specified, as well as whether the current balance allows the
        wager to be placed.
        
        Returns: an integer value for the amount wagered
        
        """
        minimum_bet = 2
        maximum_bet = 500
        

        while True:
                print("Would you like to play with high or low stakes?")
                stakes = input("High or Low Stakes (y/n): ").upper()
                if stakes not in ["Y","N"]:
                    print("Invalid input")
                    continue
                elif stakes == 'Y':
                    minimum_bet = 100
                    maximum_bet = 1000
                    print("High stakes chosen. Minimum bet per hand is now 100, maximum bet per hand is now 1000.")
                    break
                else:
                    print("Low stakes chosen. Minimum bet per hand remains at 2, maximum bet per hand remains at 500")
                    break

        while True:
            try:
                print("Your balance is:", self.balance)
                wager = int(input("Wager Amount: "))
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
        print("Your balance is now:", self.balance)
        pot.balance += wager
        print("The pot this round is now:", pot.balance)
        sleep(2)
        return wager
    


    def compute_score(self):
        
        """
        
        Computes the current cumulative score for the cards held in the individuals hand.
    
        Returns:
        int: returns an integer value for the current total of the cards held in the hand.
    
        """
        values = []
        self.score = 0
        for i in self.hand:
            val = cards.get(i)
            values.append(val)
        for j in values:
            self.score += j
        substring = "Ace"
        ace_in_hand = any(substring in string for string in self.hand)
        if self.score > 21 and ace_in_hand:
            self.score -= 10
        return self.score
    


    def show_score(self):
        
        """
        
        Shows a player's current score.
        
        """
        
        print(f"{self.name}\'s score is: {self.score}")
        
    def __str__(self):
        return self.name



    def surrender(self):

        """

        Gives player the option to surrender if they do not like their hand, and receive half of their bet back.

        """

        global surrendered
        surrendered = True



    def double_down(self):

        """

        Gives player the option to double down on their bet and double their wager if they feel their hand is advantageous. They then receive one additional card only."

        """

        self.balance -= pot.balance
        print(f"{self.name} is confident in their hand and opts to double down on the bet!")
        print("Additional Wager Amount:", pot.balance)
        print("Your balance is now:", self.balance)
        pot.double_down()
        print("The pot this round is now:", pot.balance)
        sleep(2)
        self.draw_card()
        self.compute_score()
        self.show_score()



class Dealer(Player):
    
    def __init__(self, name):
        super().__init__(name)
        self.balance = 5000
    


    def dealer_draw(self):
        
        """

        Draws a card for the dealer.

        """

        print(f"{self.name} score is less than 17. {self.name} must draw a card")
        self.draw_card()
        self.compute_score()
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
        
        dealer_score = dealer.compute_score()
        dealer_hidden_card_val = cards.get(dealer.hand[-1])
        dealer_hidden_score = dealer_score - dealer_hidden_card_val
        print(f"{self.name}\'s score is: {dealer_hidden_score} + ???")



gambler = Player('Connor')
dealer = Dealer('Dealer')
pot = Pot('Casino')



def game_reset():

    """

    Resets the game.

    """

    clear_output()
    gambler.reset()
    dealer.reset()
    pot.empty_pot()
    global surrendered
    surrendered = False



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
                    gambler.compute_score()
                    gambler.show_score()
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
                            dealer.show_score()
                            sleep(2)
                        else:
                            break
        else:
            while choice == "twist":
                gambler.draw_card()
                gambler.compute_score()
                gambler.show_score()
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
    dealer.show_score()
    sleep(2)
    while dealer.score < 17:
        dealer.dealer_draw()
        sleep(2)
    if dealer.score > 21:
        print(f"{dealer.name} is bust!")
        sleep(2)
    elif dealer.score >= 17 and dealer.score <= 21:
        print(f"{dealer.name} must stand.")
        sleep(2)
    else:
        pass



def basic_victory():

    """

    Set of actions that occur in several scenarios that result in a generic victory.

    """

    sleep(2)
    dealer.balance -= pot.balance
    pot.balance = pot.balance * 2
    gambler.balance += pot.balance
    print(f"{gambler.name} won {pot.balance} on this hand.")
    print(f"{gambler.name}\'s balance is now {gambler.balance}")
    print(f"The house balance is now {dealer.balance}")



def basic_loss():

    """

    Set of actions that occur in several scenarios that result in a generic loss.

    """

    sleep(2)
    dealer.balance += pot.balance
    print(f"{gambler.name} lost {pot.balance} on this hand.")
    print(f"{gambler.name}\'s balance is now {gambler.balance}")
    print(f"The house balance is now {dealer.balance}")




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
        print(f"{gambler.name} won {payout} on this hand.")
        print(f"{gambler.name}\'s balance is now {gambler.balance}")
        print(f"The house balance is now {dealer.balance}")
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
        gambler.balance += pot.balance * 0.5
        dealer.balance += pot.balance * 0.5
        print(f"{gambler.name} lost {pot.balance * 0.5} on this hand.")
        print(f"{gambler.name}\'s balance is now {gambler.balance}")
        print(f"The house balance is now {dealer.balance}")
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
        gambler.balance += pot.balance
        print(f"{gambler.name} is refunded {pot.balance} on this hand.")
        print(f"{gambler.name}\'s balance is now {gambler.balance}")
    else:
        pass
    pot.empty_pot()



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
    sleep(2)



def blackjack():
    
    """
    
    Plays the game of Blackjack. The deck is created at the beginning of the session. If at the beginning of a new
    hand, the deck has 10 or less cards remaining, the deck is rebuilt and a new pack of 52 cards used.
    
    """

    create_deck()
    play_again = "y"
    while play_again == "y":
        game_reset()
        if len(deck) <= 10:
            create_deck()
            print("The deck is running low on cards. The dealer introduces a new set of 52.")
            sleep(2)
        gambler.place_wager()
        deal()
        gambler.show_hand()
        gambler.compute_score()
        gambler.show_score()
        dealer.show_partial_hand()
        dealer.compute_partial_score()
        stick_or_twist()
        sleep(2)
        if surrendered == False:
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
