import random
from IPython.display import clear_output

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
        global pot
        pot += wager
        print("The pot this round is now:", pot)
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

class Dealer(Player):
    
    def __init__(self, name):
        super().__init__(name)
    
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

def empty_pot():
    
    """
    
    Creates an empty pot at the start of each round to store prize money. 
    This pot is then used to credit winnings at the end of the game.
    
    """
    global pot
    pot = 0

def create_deck():
    
    """
    
    Creates a deck of 52 playing cards using the keys in the cards dictionary.
    
    """
    
    global deck
    deck = list(cards.keys())

def deal():
    
    """
    
    Shuffles the deck.
    Assigns an empty list variable for both the player and the dealer, then populates this empty list with
    cards drawn from the top of the deck to generate a hand for the player.
    This function is used at the start of the game to deal the initial two cards to each player, with the dealer
    dealt cards last.
    
    """
    
    random.shuffle(deck)
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
        choice = input("stick or twist? ")
        while choice == "twist":
            gambler.draw_card()
            gambler.compute_score()
            gambler.show_score()
            dealer.show_hand()
            dealer.show_score()
            if dealer.score < 17:
                dealer.dealer_draw()
                dealer.show_hand()
            if gambler.score == 21:
                print(f"{gambler.name} got a blackjack!")
                break
            elif gambler.score > 21:
                print(f"{gambler.name} is bust!")
                break
            elif dealer.score > 21 and gambler.score <= 21:
                print(f"{dealer.name} is bust!")
                break
            elif dealer.score >= 17 and gambler.score > dealer.score:
                break
            else:
                pass
            choice = input("stick or twist? ")

def jackpot():
    
    """
    
    Pays out in the event the player wins.
    
    """
    
    print("You win! Congratulations!")
    global pot
    dealer.balance -= pot
    pot = pot * 2
    gambler.balance += pot
    print(f"Your balance is now {gambler.balance}")
    print(f"The house balance is now {dealer.balance}")

def endgame():
    if 21 - gambler.score < 0: # you are bust, house always wins
        print("Bust! You lose! House wins.")
        dealer.balance += pot
        print(f"Your balance is now {gambler.balance}")
        print(f"The house balance is now {dealer.balance}")

    elif 21 - gambler.score >= 0 and 21 - dealer.score < 0: # you are not bust, house is bust, you win
        print("The dealer is bust!")
        jackpot()

    elif 21 - gambler.score < 21 - dealer.score: # neither is bust, but you are closer than dealer
        print("You were closer to 21 than the dealer!")
        jackpot()

    elif 21 - gambler.score > 21 - dealer.score: # neither is bust, but dealer is closer than you
        print("You lose! The dealer was closer to 21 than you. House wins.")
        dealer.balance += pot
        print(f"Your balance is now {gambler.balance}")
        print(f"The house balance is now {dealer.balance}")

    else:
        print("Bet ends in a push. Bets will be refunded. No action this round.") # your score is tied with the dealer
        gambler.balance += pot
        print(f"Your balance is now {gambler.balance}")

def blackjack():
    
    """
    
    Plays the game of Blackjack. The deck is created at the beginning of the session. If at the beginning of a new
    hand, the deck has 10 or less cards remaining, the deck is rebuilt and a new pack of 52 cards used.
    
    """
    create_deck()
    play_again = "y"
    while play_again == "y":
        clear_output()
        gambler.reset()
        dealer.reset()
        empty_pot()
        if len(deck) <= 10:
            create_deck()
            print("The deck is running low on cards. The dealer introduces a new set of 52.")
        gambler.place_wager()
        deal()
        gambler.show_hand()
        dealer.show_partial_hand()
        gambler.compute_score()
        gambler.show_score()
        dealer.compute_partial_score()
        
        stick_or_twist()
        
        gambler.show_score()
        dealer.show_hand()
        dealer.show_score()
        
        while dealer.score < 17:
            dealer.dealer_draw()
            dealer.show_hand()
        
        if 17 <= dealer.score <= 21:
            print(f"{dealer.name} must stand. {dealer.name}\'s final score is: {dealer.score}")
        else:
            print(f"{dealer.name} is bust. {dealer.name}\'s final score is: {dealer.score}")
        endgame()
        play_again = input("Would you like to play another hand? Enter y to play again ")

blackjack()
