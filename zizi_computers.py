import random
import numpy as np

class computer:
    def __init__(self,turn_player):
        self.tP = turn_player

    def get_my_data(self,turn,drawn_player,opensource,originals,drawns,history):
        self.turn = turn
        self.original = originals[self.tP]
        self.drawn = drawns[self.tP]
        self.dP = drawn_player
        self.history = history
        self.opensources = opensource
        original_num = [0,0,0,0]
        drawn_num = [0,0,0,0]
        for i in range(4):
            original_num[i] = len(originals[i])
            drawn_num[i] = len(drawns[i])
        self.original_num = original_num
        self.drawn_num = drawn_num


    def cpu_completely_original(self): #完全にオリジナルから引く(危険)
        index = 0
        od = 'o'
        if(self.original_num[self.dP] == 0):
            od = 'd'
            index = random.randrange(self.drawn_num[self.dP])
        else:
            index = random.randrange(self.original_num[self.dP])
        return od,index

    def cpu_completely_drawns(self): #完全に引札から引く(危険)
        index = 0
        od = 'o'
        if(self.drawn_num[self.dP] != 0):
            od = 'd'
            index = random.randrange(self.drawn_num[self.dP])
        else:
            index = random.randrange(self.original_num[self.dP])
        return od,index

    def cpu_completely_random(self):    #完全ランダム
        index = 0
        od = 'o'
        card_number = self.drawn_num[self.dP] + self.original_num[self.dP]
        index = random.randrange(card_number)
        if(index > self.original_num[self.dP] - 1):
            od = 'd'
            index = index - self.original_num[self.dP]
        return od,index

    def cpu_most_recent_card(self):
        if(self.history[self.turn - 1][6] == 0):
            index = self.drawn_num[self.dP] - 1
            od = 'd'
            return od,index
        elif random.random() < 0.9:
            return self.cpu_completely_drawns()
        else:
            return self.cpu_completely_original()

class completely_random(computer):
    def draw(self):
        return self.cpu_completely_random()

class prefer_original(computer):
    def draw(self):
        index = 0
        od = 'o'
        if(random.random() < 0.9):
            return self.cpu_completely_original()
        else:
            return self.cpu_completely_drawns()
class prefer_drawn(computer):
    def draw(self):
        index = 0
        od = 'd'
        if(random.random() < 0.9):
            return self.cpu_completely_drawns()
        else:
            return self.cpu_completely_original()

class puyo(computer):
    def draw(self):
        if(self.original_num[self.dP] > 2):
            return self.cpu_completely_original()
        if(self.original_num[self.dP] == 0):
            return self.cpu_most_recent_card()
        else:
            return self.cpu_completely_random()

class puyopuyo(computer):
    def was_paired(self,turn,history):   #all after update
        if(histry[turn - 1][6] != 1):    #didn't pair
            return False
        else:
            return True
    def compare_after_drawed(self,origials,drawns):   #if now_turn > 1  and history[now_turn-1][2] == self.tP
        pre_o = self.original   #before update
        pre_d = self.drawn
        if(pre_o == originals[self.tP]):
            for card in drawns[self.tP]:
                pre_d.remove(card)
            return pre_d[0]
        else:
            for card in originals[self.tP]:
                pre_o.remove(card)
            return pre_o[0]

    def get_my_data(self,turn,drawn_player,opensource,originals,drawns,history):
        self.turn = turn
        self.original = originals[self.tP]
        self.drawn = drawns[self.tP]
        self.dP = drawn_player
        self.history = history
        self.opensources = opensource
        original_num = [0,0,0,0]
        drawn_num = [0,0,0,0]
        for i in range(4):
            original_num[i] = len(originals[i])
            drawn_num[i] = len(drawns[i])
        self.original_num = original_num
        self.drawn_num = drawn_num


class cheat(computer):
    def get_my_data(self,turn,drawn_player,opensource,originals,drawns,history):
        self.turn = turn
        self.original = originals[self.tP]
        self.drawn = drawns[self.tP]
        self.dP = drawn_player
        self.history = history
        self.opensources = opensource
        original_num = [0,0,0,0]
        drawn_num = [0,0,0,0]
        for i in range(4):
            original_num[i] = len(originals[i])
            drawn_num[i] = len(drawns[i])
        self.original_num = original_num
        self.drawn_num = drawn_num
        hand = []
        hand = originals[drawn_player] + drawns[drawn_player]
        self.hand = hand
        all_cards = opensource
        for i in range(4):
            all_cards = all_cards + originals[i] + drawns[i]
        self.all = all_cards
        self.originals = originals
        self.drawns = drawns

    def draw(self):
        for i in range(52):
            if (i not in self.all):
                zizi = i
        zizi = zizi % 13
        zizilist = [zizi,zizi+13,zizi+26,zizi+39]
        myhand = self.original + self.drawn
        kouho = []
        for i in range(len(myhand)):
            myhand[i] = myhand[i] % 13
        for card in self.hand:
            if(card % 13 in myhand):
                kouho += [card]
        if kouho == []:
            if len(self.hand) == 1:
                return self.cpu_completely_original()
            else:
                for zizis in zizilist:
                    if(zizis in self.hand):
                        od,index = self.cpu_completely_random()
                        while((od == 'o' and self.originals[self.dP][index] == zizis) or (od == 'd' and self.drawns[self.dP][index] == zizis)):
                            od,index = self.cpu_completely_random()
                        return od,index
                return self.cpu_completely_random()

        else:
            if(len(kouho) == 1):
                temp = random.randrange(len(kouho))
                index = self.hand.index(kouho[temp])
                if index > self.original_num[self.dP] - 1:
                    index = index - self.original_num[self.dP]
                    od = 'd'
                else:
                    od = 'o'
                return od,index
            else:
                temp = random.randrange(len(kouho))
                index = self.hand.index(kouho[temp])
                if index > self.original_num[self.dP] - 1:
                    index = index - self.original_num[self.dP]
                    od = 'd'
                else:
                    od = 'o'
                while(kouho[temp] in zizilist):
                    temp = random.randrange(len(kouho))
                    index = self.hand.index(kouho[temp])
                    if index > self.original_num[self.dP] - 1:
                        index = index - self.original_num[self.dP]
                        od = 'd'
                    else:
                        od = 'o'
                return od,index
