import random as r
import time
import sys
from colorama import Fore, Style

#Constantes
SYMB_NUM = 3 #número de símbolos (o programa funciona para qualquer número de símbolos > 1)
START_AMOUNT = 500 #créditos iniciais do jogador
SYMBOLS = ['#','$','%','&','@','£','€']
CHANCES = [50, 40, 30, 20, 10, 5, 1]
PRIZE_MULTIPLIERS = [5, 10, 20, 70, 200, 1000, 100000]

def color(val):
    if val == 0:  # 0
        return Fore.LIGHTGREEN_EX
    elif val == 1:  # 1
        return Fore.BLUE
    elif val == 2:  # 2
        return Fore.LIGHTWHITE_EX
    elif val == 3:  # 3
        return Fore.RED
    elif val == 4:  # 4
        return Fore.CYAN
    elif val == 5:  # 5
        return Fore.MAGENTA
    elif val == 6:  # 6
        return Fore.YELLOW

class player():
    def __init__(self):
        self.credits = START_AMOUNT
        self.bet_val = 0

    def bet(self, val):
        if val > self.credits:
            print("You don't have enough credits to bet this amount!")
        else:
            self.bet_val = val
            self.credits -= val

class SlotMachine():
    def __init__(self):
        self.val = []
        for i in range(SYMB_NUM):
            self.val.append(SYMBOLS[0]) #default combination
    
    def roll(self):
        for i in range(SYMB_NUM):
            self.val[i] = r.randint(1, 156) # 1 - 50 = #, 51 - 90 = $, ...
            #print(self.val[i])
            #Converter os valores a símbolos com base na chance respetiva
            aux = self.val[i]
            j = -1
            while (aux > 0):
                j+=1
                aux -= CHANCES[j] #subtrai as chances para descobrir a gama de valores em que se encontra
            self.val[i] = SYMBOLS[j]
    
    def display(self):
        anim = []
        for k in range(SYMB_NUM):
            anim.append(0)
        #Fazer uma animação dos três slots, com auxílio do import sys
        for i in range(29):
            sys.stdout.write('\r'+"[ ")
            for k in range(SYMB_NUM):
                iter_sym = SYMBOLS.index(self.val[k])+anim[k] #símbolo a desenhar nesta iteração
                print(color(iter_sym)+SYMBOLS[iter_sym]+Style.RESET_ALL+" ",end="")
                if k < SYMB_NUM-1:
                    print("| ",end="")
            print("]",end="")
            sys.stdout.flush()
            
            for j in range(SYMB_NUM):
                anim[j]+=1
                if SYMBOLS.index(self.val[j]) + anim[j] > 6:
                    anim[j] = -SYMBOLS.index(self.val[j])

            time.sleep(0.01 * i)

    def prize(self, bet_val):
        win_prize = 0
        for i in range(1, SYMB_NUM):
            if self.val[i-1] == self.val[i]:
                win_prize+=1
        if win_prize == SYMB_NUM-1:
            print("\nCongratulations! You just won "
            +str(bet_val * PRIZE_MULTIPLIERS[SYMBOLS.index(self.val[0])])+" credits!!")
            return bet_val * PRIZE_MULTIPLIERS[SYMBOLS.index(self.val[0])]
        else:
            print("\nNo prize! Try again!")
            return 0

P = player()
S = SlotMachine()
isRunning = True
print("Welcome to the HS Slot Machine!")
while P.credits > 0 and isRunning == True:
    #Verifica se o jogador ainda quer apostar
    print("You have "+str(P.credits)+" credits at this moment."
    +"\nDo you wish to bet? [press 'n' or 'N' to quit or any other key to continue] ",end="")

    bet_flag = input()
    if bet_flag == 'N' or bet_flag == 'n':
        isRunning = False
    else:
        print("Which amount will you bet?\nAmount [Credits]: ",end="")
        #Garantir que o jogador aposta um valor não negativo de créditos
        val = -1
        while val < 0:
            val = float(input())
        P.bet(val)
        S.roll()
        S.display()
        P.credits += S.prize(P.bet_val)
        time.sleep(0.01)

if P.credits == 0:
    print("Wow, that was some incredible bad luck. We wish you well.")
else:
    print("We hope to see you again!")