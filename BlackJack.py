"""
Author: Marion Veloria
Started: 22/5/18
Vision: Enjoyed playing blackjack growing up and
        wanted to create the game using python
"""

import random

#used for shuffling process (store cards)
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item): #add to the top of the stack  
        try:
            return self.items.append(item)
        except IndexError:
            return 'The stack is empty!'
    
    def pop(self): #remove from the top of the stack (added most recently)
        try:
            return self.items.pop()	
        except IndexError:
            return 'The stack is empty!'
    
    def is_empty(self):
        return self.items == []
        
    def size(self):
        return len(self.items)

#used for shuffling process (store cards)
class Queue:
    def __init__(self):
        self.items = []
        
    def is_empty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
    
    def enqueue(self, item): #add to rear of queue
        self.items.insert(0, item)
        
    def dequeue(self): #remove from front of queue
        try:
            result = self.items.pop()
        except IndexError:
            result = 'The queue is empty.'
        return result

#cards used in the game and processes for shuffling
class Deck:     
    def __init__(self):     
        self.cards = Stack()      
        cardlist = ['AS', 'AH', 'AC', 'AD', '2S', '2H', '2C', '2D', '3S', '3H', '3C', '3D', '4S', 
                    '4H', '4C', '4D', '5S', '5H', '5C', '5D',  '6S', '6H', '6C', '6D', '7S', '7H','7C', 
                    '7D', '8S', '8H', '8C', '8D', '9S', '9H', '9C', '9D', 'TS', 'TH', 'TC', 'TD', 'JS', 
                    'JH', 'JC', 'JD', 'QS', 'QH', 'QC', 'QD', 'KS', 'KH', 'KC', 'KD'] 
        #add cards to stack
        for i in range(52):
            card_output = cardlist[i]
            self.cards.push(card_output) 
            
    def __str__(self):
        card_output = ''
        count1 = 0
        count2 = 13
        while count2 < 53:
            for card in self.cards.items[count1:count2]:
                card_output = card_output + card + ' '
            card_output = card_output + '\n'
            count1 += 13
            count2 += 13
        return card_output

    #pop values from self.cards for a given number of times and push to s1
    #remaining values pushed to s2, afterwards both s1 and s2 contents
    #pushed back to self.cards
    def shuffleONE(self, no):
        s1 = Stack()
        s2 = Stack()
        for number in range(0,no): 
            s1.push(self.cards.pop()) 
        while not self.cards.is_empty():
            s2.push(self.cards.pop())
        while not s1.is_empty() or not s2.is_empty(): 
            if not s1.is_empty():
                self.cards.push(s1.pop())
            if not s2.is_empty():
                self.cards.push(s2.pop())

    #pop values from self.cards for a given number of times and enqueue to q1
    #remaining values pushed to s2, afterwards both q1 and s2 contents
    #pushed/dequeued back to self.cards            
    def shuffleTWO(self, no):
        q1 = Queue()
        s2 = Stack()
        for number in range(0, no):
            q1.enqueue(self.cards.pop())
        while not self.cards.is_empty():
            s2.push(self.cards.pop())
        while not q1.is_empty() or not s2.is_empty():
            if not q1.is_empty():
                self.cards.push(q1.dequeue())
            if not s2.is_empty():
                self.cards.push(s2.pop())

    #pop values from self.cards for a given number of times and enqueue to q1
    #remaining values enqueued to q2, afterwards both q1 and q2 contents
    #dequeued back to self.cards             
    def shuffleTHREE(self, no):
        q1 = Queue()
        q2 = Queue()
        for number in range(0, no):
            q1.enqueue(self.cards.pop())
        while not self.cards.is_empty():
            q2.enqueue(self.cards.pop())
        while not q1.is_empty() or not q2.is_empty():
            if not q1.is_empty():
                self.cards.push(q1.dequeue())
            if not q2.is_empty():
                self.cards.push(q2.dequeue())  
                
class Player:
    def __init__(self):
        self.cards = Stack() #players hand
        
    def points_eval(self):
        count = 0 #card value
        count1 = 0 #number of aces 
        for card in self.cards.items[:]:
            value = card[0] #seperates value from suit
            cards = "KQJT"
            if value in cards:
                count += 10
            elif value == 'A':
                count1 += 1
            else:
                count += int(value)
        #checks the number of aces to ensure combined value
        #of the aces does not excede 21, 
        #by adjusting total value of aces below 21
        #e.g. 3 A's = 13 instead of 33 (11 + 1 + 1)
        if count1 == 1:
            if count + 11 <= 21:
                count += 11
            else:
                count += 1
        if count1 == 2:
            if count + 12 <= 21:
                count += 12
            else:
                count += 2 
        if count1 == 3:
            if count + 13 <= 21:
                count += 13
            else:
                count += 3
        if count1 == 4:
            if count + 14 <= 21:
                count += 14
            else:
                count += 4
        return count
    
    def __str__(self):
        output = "["
        output2 = ""
        for card in self.cards.items[:]:
            output2 = output2 + str(card[0])
        for card in self.cards.items[0:len(output2) - 1]:
            output = output + "'" + str(card) + "'" + ', '
        for card in self.cards.items[len(output2) - 1:len(output2)]:
            output = output + "'" + str(card) + "'" + ']'       
        return output

#visuals
def symbols ():
    print("*" * 80)

#computers brain
def computer (userValue, dealerValue):
    if userValue > dealerValue: 
        return 1
    else:
        if dealerValue < 11:
            return 1
        if dealerValue < 15: #80 % chance dealer will hit
            num1 = random.randint(1, 10);
            if num1 >= 2:
                return 0
            else:
                return 1
        if dealerValue < 18: #50% chance delaer will hit
            num1 = random.randint(1, 10);
            if num1 >= 5:
                return 0
            else:
                return 1
        else:
            return 0

#mainloop
endgame = False
endMenu = False
Gdeck = Deck()
#intro
userName = input("Enter your name: ")
print()
symbols()
print("Welcome " + userName+ ",")
print()
print("This game you will be playing is called blackjack or 21.")
print("The aim is to have a higher total card value than the dealer")
print("but not over the value of 21. The cards K,Q,J,T all have a value of 10,")
print("while A can have a value of 11 or 1. The letters after the value is the")
print("card suit e.g. KD is King of Diamonds. Hope you Enjoy " + userName + "!")
symbols()
print()
while (endMenu == False):
    #menu
    symbols()
    introInput = input("Play, Enter 1 \nExit, Enter 2 \n\nYour Entry: ")
    symbols()
    print()
    #if user decides to play
    if introInput == "1":
        endgame = False
        #randomize deck
        random1 = random.randint(1, 53);
        random2 = random.randint(1, 53);
        random3 = random.randint(1, 53);
        Gdeck.shuffleONE(random1)
        Gdeck.shuffleTWO(random2)
        Gdeck.shuffleTHREE(random3)
        #instantiate user and dealer
        P1 = Player()
        Dealer = Player()
        P1.cards.push(Gdeck.cards.pop())
        Dealer.cards.push(Gdeck.cards.pop())
        P1.cards.push(Gdeck.cards.pop())
        Dealer.cards.push(Gdeck.cards.pop())
        #visual representation
        symbols()
        print("Your cards = ", end = "")
        print(P1)
        print("Your total cards value = ", end = "")
        print(P1.points_eval())
        print()
        print("Dealer's cards = ", end = "")
        print(Dealer)
        print("Dealer's total cards value = ", end = "")
        print(Dealer.points_eval())
        symbols()
        print()
        #game running
        while (endgame == False):
            #checks if user or dealer have gone over 21
            if P1.points_eval() > 21:
                print("$$$$$ GAME OVER! Better luck next time " + userName +" $$$$$")
                break
            if Dealer.points_eval() > 21:
                print("$$$$$ CONGRATULATIONS YOU WIN! " + userName + " $$$$$")
                break
            input1 = input("Do you want one more card? Enter (y/n) ")
            print()
            if input1 == 'y':
                endgame = False
                #decides if computer stays or hits
                game = computer(P1.points_eval(), Dealer.points_eval())
                if game == 1:
                    Dealer.cards.push(Gdeck.cards.pop())
                P1.cards.push(Gdeck.cards.pop())
                #visual representation
                symbols()
                print("Your cards = ", end = "")
                print(P1)
                print("Your total cards value = ", end = "")
                print(P1.points_eval())
                print()
                print("Dealer's cards = ", end = "")
                print(Dealer)
                print("Dealer's total cards value = ", end = "")
                print(Dealer.points_eval())
                symbols()
                print()
            elif input1 == 'n':
                endgame = True
                #dealer keeps playing if his total card value is lower
                for i in range(5):
                    if (P1.points_eval() > Dealer.points_eval()) and (Dealer.points_eval() < 21):
                        Dealer.cards.push(Gdeck.cards.pop())
                        #visual representation
                        print("Dealer hits!")
                        print()
                        symbols()
                        print("Your cards = ", end = "")
                        print(P1)
                        print("Your total cards value = ", end = "")
                        print(P1.points_eval())
                        print()
                        print("Dealer's cards = ", end = "")
                        print(Dealer)
                        print("Dealer's total cards value = ", end = "")
                        print(Dealer.points_eval())
                        symbols()
                        print()
                #determines winner
                if Dealer.points_eval() > 21:
                    print("$$$$$ CONGRATULATIONS YOU WIN! " + userName + " $$$$$")
                    print()
                elif P1.points_eval() > Dealer.points_eval():
                    print("$$$$$ CONGRATULATIONS YOU WIN! " + userName + " $$$$$")
                    print()
                elif Dealer.points_eval() > P1.points_eval():
                    print("$$$$$ GAME OVER! Better luck next time " + userName +" $$$$$")
                    print()
                else:
                    print("$$$$$ DRAW! $$$$")
                    print()
            else:
                symbols()
                print("Please enter y or n")
                symbols()
                print()
    #if user decides to exit
    elif introInput == "2":
        endMenu = True
        print("See you next time " + userName + "!!!!!")
        print()
    #if user type invalid command
    else:
        print("!!!!!!!!!! Please enter 1 or 2 !!!!!!!!!!\n")
