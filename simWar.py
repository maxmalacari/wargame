# Simulate war card game
# Max Malacari - 1/01/2018

import random
import matplotlib.pyplot as plt

def main():

    verbose = False
    plot = True

    # some arrays for plotting
    turnArray = []
    cardArray1 = []
    cardArray2 = []
    sumArray1 = []
    sumArray2 = []
    
    # Define the available cards
    # 52 cards, 4 of each card, 13 unique cards (14 is ace)
    deck = []
    for card in range(2,15):
        for duplicate in range(0,4):
            deck.append(card)

    if verbose:
        print "There are", len(deck), "cards in the deck!"
        print "Shuffling deck..."

    random.shuffle(deck)

    # Initialize two players w/ 26 cards each
    players = [[0]*26 for i in range(2)]

    if verbose:
        print "Dealing cards..."
    
    for i in range(0,26):
        players[0][i] = deck[i]
        players[1][i] = deck[i+26]

    # Let's play the game!
    # Play until someone has all the cards
    turns = 0
    while (len(players[0]) > 0 and len(players[1]) > 0):

        if plot:
            turnArray.append(turns)
            cardArray1.append(len(players[0]))
            cardArray2.append(len(players[1]))
            sumArray1.append(sum(players[0]))
            sumArray2.append(sum(players[1]))
        
        turns += 1
        #print len(players[0]), len(players[1])
    
        p0card = players[0].pop(0)
        p1card = players[1].pop(0)
        cardStack = [p0card, p1card]

        if p0card > p1card:
            players[0].extend(cardStack)
        elif p1card > p0card:
            players[1].extend(cardStack)
        else:
            # Both players have same card - war time!
            winner = WarTime(players)
            players[winner].extend(cardStack) # winner takes card stack as well
            
        # Both players shuffle after each turn
        [random.shuffle(players[i]) for i in range(2)]

        if verbose:
            print "Player 1:", players[0], "-", len(players[0]), "card(s)."
            print "Player 2:", players[1], "-", len(players[1]), "card(s)."

        if (len(players[0]) + len(players[1])) > 52: # Just make sure we don't stuff up
            print "ERROR: Convservation of cards has been violated!!"
            return

    if plot:
        turnArray.append(turns)
        cardArray1.append(len(players[0]))
        cardArray2.append(len(players[1]))
        sumArray1.append(sum(players[0]))
        sumArray2.append(sum(players[1]))


    winner = 2
    if len(players[0]) > 0:
        winner = 1
    print "Took", turns, "turns for player", winner, "to win"

    if plot:
        plt.plot(turnArray,cardArray1, lw=2, color='b')
        plt.plot(turnArray,cardArray2, lw=2, color='r')
        plt.ylabel("Cards in hand")
        plt.xlabel("Turn")
        plt.grid(True)
        plt.ylim(0,52)
        plt.xlim(0,turns)
        plt.show()
        plt.plot(turnArray, sumArray1, lw=2, color='b')
        plt.plot(turnArray, sumArray2, lw=2, color='r')
        plt.ylabel("Card sum")
        plt.xlabel("Turn")
        plt.grid(True)
        plt.ylim(0,4*sum(range(0,15)))
        plt.xlim(0,turns)
        plt.show()

def WarTime(players):
    
    cardStack = []
    winner = -1

    while winner < 0:

        # Check if both players have enough cards to have a war, otherwise they lose all their cards
        if len(players[0]) < 2:
            cardStack.extend(players[0])
            players[1].extend(cardStack)
            players[0][:] = []
            winner = 1
            continue
        elif len(players[1]) < 2:
            cardStack.extend(players[1])
            players[0].extend(cardStack)
            players[1][:] = []
            winner = 0
            continue
        
        cardStack.append(players[0].pop(1)) # second card
        cardStack.append(players[1].pop(1))

        # comparison card
        p0card = players[0].pop(0)
        p1card = players[1].pop(0)
        cardStack.extend([p0card,p1card])
        
        if p0card > p1card:
            players[0].extend(cardStack)
            winner = 0
        elif p1card > p0card:
            players[1].extend(cardStack)
            winner = 1
        else:
            winner = -1 # Go again!

    # winner takes card stack from war
    return winner

main()
