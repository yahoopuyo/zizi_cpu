import random
import numpy as np
import pandas as pd

'''
はじめに
from zizi_record import Record
はじめのoriginal配列が作られたあと(ペア消去後)に
record = Record(originals)
揃った判定の関数の揃った場合のところに
record.update_record_paired(turn,drawn_card,x)
揃ってない場合のところに
record.update_record_unpaired(turn,drawn_card,turn_player,originals[turn_player] + drawns[turn_player])

を追加
'''

class Record:
    def __init__(self,originals):
        num_list = []
        for i in range(4):
            num_list += [len(originals[i])]
        num_list = np.array(num_list)
        dfs = [0,0,0,0]
        for i in range(4):
            temp = []
            for x in range(num_list[i]):
                temp.append(num_list[0:i].sum() + x)
            dfs[i] = pd.DataFrame(np.zeros((num_list[i],num_list[i]),dtype = int),columns = temp)
        record = pd.concat([dfs[0],dfs[1],dfs[2],dfs[3]],ignore_index = True)
        uniform = []
        for i in range(4):
            for card in originals[i]:
                uniform.append(card)
        uniform_exists = []
        for i in range(num_list.sum()):
            uniform_exists.append(i)
        self.uniform = uniform
        self.record_size = num_list.sum()
        self.record = record
        self.record_record =[]
        self.uniform_exists = uniform_exists
    def replace_df(self,x,y,value):
        if(str(self.record[x][y]) == 'nan'):
            self.record[x][y] = value

    def update_record_unpaired(self,turn,drawnCard,tP,tP_cards):     #tP_cards = originals[tP]+drawns[tP]
        #tP_cards = originals[tP] + drawns[tP]
        tP_uns = []
        drawn_un = self.uniform.index(drawnCard)
        for card in tP_cards:
            tP_uns.append(self.uniform.index(card))
        for i in tP_uns:
            self.replace_df(drawn_un,i,turn)
            self.replace_df(i,drawn_un,turn)

    def update_record_paired(self,turn,drawnCard,pairCard):
        drawn_un = self.uniform.index(drawnCard)
        pair_un = self.uniform.index(pairCard)
        self.uniform_exists.remove(drawn_un)
        self.uniform_exists.remove(pair_un)
        for i in range(self.record_size):
            self.replace_df(i,drawn_un,turn)
            self.replace_df(i,pair_un,turn)
            self.replace_df(pair_un,i,turn)
            self.replace_df(drawn_un,i,turn)

    def show(self):
        print(self.uniform_exists)
        print("\n")
        print(self.record)
        print("\n")
    def add_to_record(self):
        self.record_record.append(self.copy().record)
    def copy(self):
        originals_temp = [[0] * self.record_size] + [[]] + [[]] + [[]]
        copied = Record(originals_temp)
        copied.uniform = self.uniform
        copied.record = self.record

        return copied
