#! /usr/bin/env python3
import random
import numpy as np
import sys
sys.path.append('.')
import zizi_computers as cpu

marks = ["S", "H", "C", "D"]

games = 1
winnerList = np.zeros((4,4),dtype = int)  #縦軸が順位、横軸がプレイヤー

# cpu0 = cpu.puyo(0)
# cpu1 = cpu.puyo(1)
# cpu2 = cpu.cheat(3)
# cpu3 = cpu.puyo(2)

'''
def cpu1(dP,tP):    #完全ランダム
    index = 0
    od = 'o'
    card_number = len(originals[dP]) + len(drawns[dP])
    index = random.randrange(card_number)
    if(index > len(originals[dP]) - 1):
        od = 'd'
        index = index - len(originals[dP])
    return od,index

def cpu_completely_original(dP,tP): #完全にオリジナルから引く(危険)
    index = 0
    od = 'o'
    if(originals[dP] == []):
        od = 'd'
        index = random.randrange(len(drawns[dP]))
    else:
        index = random.randrange(len(originals[dP]))
    return od,index

def cpu_completely_drawns(dP,tP):   #完全に引札から引く(危険)
    index = 0
    od = 'd'
    if(drawns[dP] == []):
        od = 'o'
        index = random.randrange(len(originals[dP]))
    else:
        index = random.randrange(len(drawns[dP]))
    return od,index

def cpu_most_recent_card(dP,tP):    #一番最近のカードが揃ってなかったらそれを引き、揃っていてもなるべく引札を引く
    global turn
    if(history[turn-1][6] == 0):
        index = len(drawns[dP]) - 1
        od = 'd'
        return od,index
    else:
        return cpu3(dP,tP)

def cpu2(dP,tP):    #高確率でオリジナルから引く
    index = 0
    od = 'o'
    if(random.random() < 0.9):
        return cpu_completely_original(dP,tP)
    else:
        return cpu_completely_drawns(dP,tP)

def cpu3(dP,tP):    #高確率で引札から引く
    index = 0
    od = 'd'
    if(random.random() < 0.9):
        return cpu_completely_drawns(dP,tP)
    else:
        return cpu_completely_original(dP,tP)

def cpu4(dP,tP):
    if(len(originals[tP]) > 2):
        return cpu_completely_original(dP,tP)
    if(originals[tP] == []):
        return cpu_most_recent_card(dP,tP)
    else:
        return cpu1(dP,tP)

#def cpuManager(dP,tP):
    if(tP == 0):
        return cpu4(dP,tP)
    elif(tP == 1):
        return cpu4(dP,tP)
    elif(tP == 2):
        return cpu4(dP,tP)
    elif(tP == 3):
        return cpu4(dP,tP)
'''
def cpuManager(dP,tP):
    for player in player_list:
        player.get_my_data(turn,dP,opensource,originals,drawns,history)
        if player.tP == tP:
            od,index = player.draw()
    return od,index

def newInputCard(player_num,turn_player):  #player_numはひかれる人,turnPlayerは引く人、返り値は引いたカード
    od,index = cpuManager(player_num,turn_player)
    if od =='o':
        drawn_card = originals[player_num].pop(int(index))

        history[turn][3] = 0
        history[turn][4] = index
        history[turn][5] = drawn_card

        return drawn_card
    elif od == 'd':
        drawn_card = drawns[player_num].pop(int(index))
        history[turn][3] = 1
        history[turn][4] = index
        history[turn][5] = drawn_card

        return drawn_card

def newJudge(turn_player, drawn_card):
    global opensource
    drawn_card_num = drawn_card%13
    flug = False  #カードが揃ったら、Trueになる
    tmp = 0
    for i, x in enumerate(originals[turn_player]):
        if x%13 == drawn_card_num:  #もしオリジナルで揃ったら
            originals[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None
            ages[x] = None #agesに揃ったことを意味するNoneを代入
            ages[drawn_card] = None
            opensource = opensource + [x]+ [drawn_card]
            flug = True
    for i, x in enumerate(drawns[turn_player]):
        if x%13 == drawn_card_num:  #もし引き札で揃ったら
            drawns[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None
            ages[x] = None #agesに揃ったことを意味するNoneを代入
            ages[drawn_card] = None
            opensource = opensource + [x]+ [drawn_card]
            flug = True
    if flug == False:
        drawns[turn_player].append(drawn_card)
        places[drawn_card] = turn_player
    return flug

def draw(turn_player, drawn_player):
    drawn_card = newInputCard(drawn_player,turn_player)

    flag = newJudge(turn_player,drawn_card)
    history[turn][6] = int(flag)  #カードを引くための関数。毎ターン、多くても一回呼び出される。

players = [0,1,2,3]   #A,B,C,D
for game in range(games):

    #playershuffle = random.sample([0,1,2,3],4)
    start_rand = random.randrange(4)
    playershuffle = [start_rand,(start_rand + 1) % 4,(start_rand + 2) % 4,(start_rand + 3) % 4]

    cpu0 = cpu.prefer_drawn(playershuffle[0])
    cpu1 = cpu.cheat(playershuffle[1])
    cpu2 = cpu.prefer_drawn(playershuffle[2])
    cpu3 = cpu.cheat(playershuffle[3])

    #print(playershuffle)
    player_list = [cpu0,cpu1,cpu2,cpu3]

    As_originals = []
    As_drawns = []
    Bs_originals = []
    Bs_drawns = []
    Cs_originals = []
    Cs_drawns = []
    Ds_originals = []
    Ds_drawns = []
    #これらを配列に入れておく
    originals = [As_originals, Bs_originals, Cs_originals, Ds_originals]
    drawns = [As_drawns, Bs_drawns, Cs_drawns, Ds_drawns]

    history = [[None]*9 for i in range(1001)]  #100ターン分用意しとく。この配列のみ、関数の中で、globalに変更しないといけない。
    #中身の配列の意味は、[turn, turn_player, drawn_player, originals or drawns(0 or 1), index, drawn_card, そろったか(0 or 1), drawn_player_win(None or 1), turn_player_win(None or 1)]
    history_of_ages = [[None]*53 for i in range(1001)]
    history_of_places = [[None]*53 for i in range(1001)]

    global turn
    turn = 1
    zizi_index = 0
    zizi_num = 0
    orders = []   #１位から４位までの人を順に代入。
    ages = [None] + [0]*52 #カードの年齢を保持する配列

    #シャッフル前のそれぞれのカードのありか
    places_begin = [None] + [None, 1,2,3] + list(range(0,4)) * 12

    #カードの場所をシャッフルして、それぞれのカードがどこにあるかを書いておく配列を初期化
    places = [None] + random.sample(places_begin[1:53], 52)   #random.sampleで指定した範囲の中の要素をシャッフルした新たな配列を作れる

    #この配列の２つ目のNoneがziziのインテックスがziziのカードのインデックス
    zizi_index = 1 + places[1:53].index(None)

    #ziziの年齢をNoneに変更
    ages[zizi_index] = None

    #次に各プレイヤーのオリジナルにカードを入れる
    for card_num, player_num in enumerate(places[1:53],1):
        if player_num != None:
            originals[player_num] += [card_num]

    opensource = []
    #各プレイヤーの手札で、揃ってるのをopensource配列に入れる
    for card_num in range(1,14):  #１から１３まで順に、それぞれのカードのありかが同じ二枚があれば、そのありかをNoneに変更し、その人の手札から取り除く。
        for i in range(0,3):  #スペードからクローバーまで、３マーク
            for j in range(i+1,4):  #iのマークから、ダイヤまで。
                if places[card_num + 13 * i] == places[card_num + 13 * j] and places[card_num + 13 * i] != None and places[card_num + 13 * j] != None:
                    the_player = places[card_num + 13 * i]
                    originals[the_player].remove(card_num + 13 * i)
                    originals[the_player].remove(card_num + 13 * j)
                    #opensource.append(card_num + 13 * i).append(card_num + 13 * j)
                    opensource += [card_num + 13 * i]
                    opensource += [card_num + 13 * j]
                    places[card_num + 13 * i] = None
                    places[card_num + 13 * j] = None



    #各プレイヤーの手札をシャッフル
    for i in range(0,4):
        random.shuffle(originals[i])


    #ゲーム開始の時点で、places = Noneのカード、つまりそろっているカードのageをNoneにする。
    for i in range(1, len(places)):
        if places[i] == None:
            ages[i] = None



    #ゲーム開始前に、turn = 0のplacesとagesをhistoryに入れとく。
    history_of_places[0] = places[:]
    history_of_ages[0] = ages[:]
    history[0] = [None]*9








    turn_player_win = False #active win した人がいるかどうか
    drawn_player_win = False #passive win した人がいるかどうか
    loser_exist = False
    next_turn_player = 0
    previous_turn_num = 0
    #age_increase = False

    while loser_exist == False:

        turn_player = turn%4
        #print(turn)
        history[turn][0] = turn
        history[turn][1] = turn_player


        if turn_player_win == True:  #もし、先のターンの人が上がったら、次に順番が回ってくる人は、何もしない。
            turn_player_win = False


            history[turn][2] = None   #このターンは誰も引かないので、historyの[2] ~ [8]は変更しない。
            history[turn][3] = None
            history[turn][4] = None
            history[turn][5] = None
            history[turn][6] = None
            history[turn][7] = None
            history[turn][8] = None

            for i in range(0,len(ages)):
                if ages[i] == None or ages[i] == 0:   #ziziのカードや、すでに揃ったカード、まだ誕生していないカードには、何もしない。
                    pass
                else:
                    ages[i] = ages[i] + (turn - previous_turn_num)

            history_of_places[turn] = places[:]
            history_of_ages[turn] = ages[:]        #このターンの履歴を記入。
            previous_turn_num = turn

            for cnt in range(1,4):   #次のターンの人を探して、ターンをあげるだけ。
                if originals[(turn + cnt)%4] != [] or drawns[(turn + cnt)%4] != []:
                    loser_exist = False
                    turn = turn + cnt
                    break
                if cnt == 3 and originals[(turn + cnt)%4] == [] and drawns[(turn + cnt)%4] == []:
                    loser_exist = True
                    orders.append(turn_player)
    #                print("プレイヤー"+ str(turn_player) + "さんのビリが確定しました")
    #                print(" ")
                    break

        else:   #もし、先のターンの人が上がってなかったら、次に順番が回ってきた人は、先のターンの人から一枚引き抜き、
            drawn_player = turn%4
            for cnt in range(1,4):
                if originals[(turn - cnt)%4] != [] or drawns[(turn - cnt)%4] != []:
                    drawn_player = (turn -cnt)%4
                    break
            history[turn][2] = drawn_player




            draw(turn_player, drawn_player)





            if originals[drawn_player] == [] and drawns[drawn_player] == []:  #もし、引かれた人の手札が空になったら、その人は上がり。
                drawn_player_win == True
                orders.append(drawn_player)
    #            print("プレイヤー{}さんが上がりました".format(drawn_player))
    #            print(" ")
                history[turn][7] = 1
            if originals[turn_player] == [] and drawns[turn_player] == []:   #もし、引いた人の手札が空になったら、その人は上がり。
                turn_player_win = True
                orders.append(turn_player)
    #            print("プレイヤー{}さんが上がりました".format(turn_player))
    #            print(" ")
                history[turn][8] = 1

            for i in range(0,len(ages)):
                if ages[i] == None or ages[i] == 0:   #ziziのカードや、すでに揃ったカード、まだ誕生していないカードには、何もしない。
                    pass
                else:
                    ages[i] = ages[i] + (turn - previous_turn_num)   #それ以外の、すでに誕生していたカードには、先のターンから今のターンの差の分を加算。
            for i in range(0,len(places)):
                if places[i] != history_of_places[0][i] and ages[i] == 0:   #これまで0歳だったのに、このターンでplacesが変わったカードについて。
                    ages[i] = 1   #誕生したことを示す、1。


            previous_turn_num = turn
            history_of_places[turn] = places[:]
            history_of_ages[turn] = ages[:]         #このターンの履歴を記入。

            for cnt in range(1,4):   #続いて、次のターンの人を探す処理をする。
                if originals[(turn + cnt)%4] != [] or drawns[(turn + cnt)%4] != []:
                    loser_exist = False
                    turn = turn + cnt
                    #print("turnnnnnnn = {}".format(turn))
                    break
                if cnt == 3 and originals[(turn + cnt)%4] == [] and drawns[(turn + cnt)%4] == []:  #三人目まで調べてみて
                    loser_exist = True   #もし、自分以外のみんなの手札が空の場合、その人の負けが確定する。
                    orders.append(turn_player)
    #                print("プレイヤー"+ str(turn_player) + "さんのビリが確定しました")
                    break

    #        print(opensource)


    #ターンの最後


    if zizi_index %13 == 0:
        zizi_num = 13
    else:
        zizi_num = zizi_index%13
    #print("ziziは{}{:02d}でした。".format(marks[int((zizi_index-1)/13)], zizi_num))
    #print(" ")
    #print("順位は")
    for rank in range(1,5):
        #print("{}位がプレイヤー{}さんでした。".format(rank, orders[rank-1]))
        try:
            winnerList[rank-1][playershuffle.index(orders[rank-1])] += 1
            #winnerList[rank-1][orders[rank-1]] += 1
        except IndexError:
            pass
    #print('\n')
print(winnerList)
#print(" ")
