#! /usr/bin/env python3
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import gspread
import sys,shutil
import subprocess as sb
import time

scopes = ['https://www.googleapis.com/auth/spreadsheets']
json_file = 'Auto upload-afd352d2577f.json'#OAuth用クライアントIDの作成でダウンロードしたjsonファイル
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
http_auth = credentials.authorize(Http())

doc_id1 = '1ZXzcpp8UMT5kYiK7wlQ603nylg6V3tQpbz8RcNosPUE'
doc_id2 = '1cK_zdcbjOQAS5ORzKdL4V4DKcHHitonlDBCww2ZKMDs'
doc_id3 = '1tja1oO6Ijlmn9UwM8A7-MAMH4sK0A238RwwtloNBUh8'
doc_id4 = '1vjGDu8PM8Z_VGv5xzJ7ZRIkUtjeXwp7rWAPY32bCR-o'

client = gspread.authorize(credentials)
gfile1   = client.open_by_key(doc_id1)#読み書きするgoogle spreadsheet
gfile2   = client.open_by_key(doc_id2)
gfile3   = client.open_by_key(doc_id3)
gfile4 = client.open_by_key(doc_id4)

player = [0,0,0,0]
player[0] = gfile1.sheet1
player[1] = gfile2.sheet1
player[2] = gfile3.sheet1
player[3] = gfile4.sheet1


import random
import pprint


players = [0,1,2,3]   #A,B,C,D
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

#marks = ["S", "H", "C", "D"]
marks = ["♤", "♡", "♧", "♢"]
#numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

history = [[None]*11 for i in range(101)]  #100ターン分用意しとく。この配列のみ、関数の中で、globalに変更しないといけない。
#中身の配列の意味は、[turn, turn_player, drawn_player, originals or drawns(0 or 1), index, drawn_card, そろったか(0 or 1), drawn_player_win(None or 1), turn_player_win(None or 1), ターンプレイヤーのオリジナル、引き札のどちらから揃ったか(o or d : 0 or 1), be_set_card_index(揃ったカードのインデックス)]
history_of_ages = [[None]*53 for i in range(101)]
history_of_places = [[None]*53 for i in range(101)]

#cards = [0, S1, S2, ,,, S13, H1, H2, ,,, H13, C1, C2, ,,, C13, D1, D2, ,,, D13]で
#インデックスは0~52、サイズは53。


#zizi確関数1用の配列。内側の配列の第1項がターン。第2項が予想した数字。
zizikaku1_lst = [[None, None], [None, None], [None, None], [None, None]]
#zizi確関数2用の配列。内側の配列の第1項がターン。第2項が予想した数字候補１。第3項が予想した数字候補２。第4項が予想した数字候補３。
zizikaku2_lst = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
#zizi確ボタンを使ったかどうか
zizikaku_used = [0,0,0,0]


com_player_nums = [0,1,2,3]  #毎回このファイルを実行するときに、comのプレイヤーが何番か記入すること。
com_player_pattern = [2,0,1,2 ]  #com_player_numsになってるインデックスに、そのcomのパターンを記入すること。
#パターン０がとにかくオリジナルから引く。
#パターン１がとにかく引き札から引く。
#パターン２が完全ランダムで引く。
#パターン３がオリジナルから：引き札から＝n:mの確率でランダムで引く。より詳しく言えば、オリジナルのカードにn倍、引き札のカードにm倍の重みをつけてランダムに選ぶ。
global pattern_3_n
global pattern_3_m
pattern_3_n = 5
pattern_3_m = 5
#整数値にして下さい


#棋譜の表を用意
kihu = [[None]]
cards_at_field_num_at_first = 0





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


#各プレイヤーの手札で、揃ってるのをopen_source配列に入れる
for card_num in range(1,14):  #１から１３まで順に、それぞれのカードのありかが同じ二枚があれば、そのありかをNoneに変更し、その人の手札から取り除く。
    for i in range(0,3):  #スペードからクローバーまで、３マーク
        for j in range(i+1,4):  #iのマークから、ダイヤまで。
            if places[card_num + 13 * i] == places[card_num + 13 * j] and places[card_num + 13 * i] != None and places[card_num + 13 * j] != None:
                the_player = places[card_num + 13 * i]
                originals[the_player].remove(card_num + 13 * i)
                originals[the_player].remove(card_num + 13 * j)
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
history[0] = [None]*11



def Debug():
    for pn in range(4):
        showField(pn,originals,drawns)
    #print(zizi_index)
    init_opensource(places,zizi_index)
    for i in range(5):
        update_history('ゲームを開始します'+ str(i),4)


def showField(player_number,originals,drawns):
    next1 = (player_number + 1) % 4
    next2 = (player_number + 2) % 4
    next3 = (player_number + 3) % 4
    temp = []
    for i in range(15):     #initialize temp
        temp.append([])
        for j in range(15):
            temp[i].append('')


    for i in range(len(originals[player_number])):
        temp[14][i] = marks[int((originals[player_number][i]-1)/13)] + str(originals[player_number][i]%13 if originals[player_number][i]%13 != 0 else 13)
    for i in range(len(drawns[player_number])):
        temp[13][1+i] = marks[int((drawns[player_number][i]-1)/13)] +  str(drawns[player_number][i]%13 if drawns[player_number][i]%13 != 0 else 13)

    for i in range(len(originals[next1])):
        temp[i][0] = '◯'+ str(i)
    for i in range(len(drawns[next1])):
        temp[1+i][1] = '□'+ str(i)

    for i in range(len(originals[next2])):
        temp[0][14-i] = '◯'+ str(i)
    for i in range(len(drawns[next2])):
        temp[1][13-i] = '□'+ str(i)

    for i in range(len(originals[next3])):
        temp[14-i][14] = '◯'+ str(i)
    for i in range(len(drawns[next3])):
        temp[13-i][13] = '□'+ str(i)

    cell_list = player[player_number].range(3,3,17,17)
    for i in range(15):
        for j in range(15):
            cell_list[i*15 + j].value = temp[i][j]
    player[player_number].update_cells(cell_list)


def init_opensource(places,zizi_index):
    temp = []
    for i in range(13):
        temp.append(0)

    for i in range(1,14):
        number =0
        for j in range(4):
            if(places[i+13*j]==None and i+13*j != zizi_index):
                number += 1
        temp[i-1] = number

    for pn in range(4):
        cell_list = player[pn].range(1,20,13,20)
        for i in range(13):
            cell_list[i].value = temp[i]
        player[pn].update_cells(cell_list)


def newInputCard_with_com(drawn_player,turn_player):  #drawn_playerはひかれる人
    global loser_exist
    od = ''
    index = ''
    drawn_card = 0

    if turn_player not in com_player_nums:   #turn_playerがcomではないならば
        flug = False #この関数の目的が達成されれば、Trueとなり、この関数を抜ける
        while flug == False:
            while (od == '' or index == ''):
                t_start = time.time()
                while(True):
                    t_temp = time.time()
                    if t_temp - t_start > 4:
                        break
                cell_list = player[turn_player].range(19,4,20,4)
                od = cell_list[0].value
                index = cell_list[1].value

            if od =='o' or od == '0':
                try:
                    drawn_card = originals[drawn_player].pop(int(index))

                    history[turn][3] = 0
                    history[turn][4] = index
                    history[turn][5] = drawn_card

                    his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                    his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                    update_history(his1,turn_player)
                    update_history(his2,drawn_player)

                    #ここに、odとindexを受け取ったら、そのセルを空白にする処理を書けば良さそう。
                    cell_list[0].value = ''
                    cell_list[1].value = ''
                    player[turn_player].update_cells(cell_list)
                    flug = True


                except:
                    cell_list[0].value = ''
                    cell_list[1].value = ''
                    player[turn_player].update_cells(cell_list)
                    flug = False

            elif od == 'd' or od == '1':
                try:
                    drawn_card = drawns[drawn_player].pop(int(index))
                    history[turn][3] = 1
                    history[turn][4] = index
                    history[turn][5] = drawn_card

                    his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                    his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                    update_history(his1,turn_player)
                    update_history(his2,drawn_player)


                    #ここに、odとindexを受け取ったら、そのセルを空白にする処理を書けば良さそう。
                    cell_list[0].value = ''
                    cell_list[1].value = ''
                    player[turn_player].update_cells(cell_list)
                    flug = True


                except:
                    cell_list[0].value = ''
                    cell_list[1].value = ''
                    player[turn_player].update_cells(cell_list)
                    flug = False

            elif od == 'quit':
                loser_exist = True
                print('quitされました')
                flug = True

            else:
                cell_list[0].value = ''
                cell_list[1].value = ''
                player[turn_player].update_cells(cell_list)
                flug = False
        return drawn_card

    elif turn_player in com_player_nums:  #もしターンプレイヤーがcomなら
        if com_player_pattern[turn_player] == 0:  #comのパターンが０なら、とにかくオリジナルから引く
            if originals[drawn_player] != []: #もしdrawn_playerのオリジナルがまだあるなら、ランダムで引く
                od = "o"
                index = random.randint(0, len(originals[drawn_player])-1)
                drawn_card = originals[drawn_player].pop(index)

                history[turn][3] = 0
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)


            elif originals[drawn_player] == []:
                od = "d"
                index = random.randint(0, len(drawns[drawn_player])-1)
                drawn_card = drawns[drawn_player].pop(index)

                history[turn][3] = 1
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)

            return drawn_card

        elif com_player_pattern[turn_player] == 1:  #とにかく引き札から引く
            if drawns[drawn_player] != []:
                od = "d"
                index = random.randint(0, len(drawns[drawn_player])-1)
                drawn_card = drawns[drawn_player].pop(index)

                history[turn][3] = 1
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)

            elif drawns[drawn_player] == []:
                od = "o"
                index = random.randint(0, len(originals[drawn_player])-1)
                drawn_card = originals[drawn_player].pop(index)

                history[turn][3] = 0
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)

            return drawn_card

        elif com_player_pattern[turn_player] == 2:   #完全ランダム
            temp_index = random.randint(0, len(originals[drawn_player])+len(drawns[drawn_player])-1)  #オリジナルと引き札を通したインデックス
            if temp_index < len(originals[drawn_player]):
                od = "o"
                index = temp_index
                drawn_card = originals[drawn_player].pop(index)

                history[turn][3] = 0
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)

            elif temp_index >= len(originals[drawn_player]):
                od = "d"
                index = temp_index - len(originals[drawn_player])
                drawn_card = drawns[drawn_player].pop(index)

                history[turn][3] = 1
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)

            return drawn_card

        elif com_player_pattern[turn_player] == 3:  #n:m
            temp_index = random.randint(0, len(originals[drawn_player])*pattern_3_n + len(drawns[drawn_player])*pattern_3_m -1)
            if temp_index < len(originals[drawn_player])*pattern_3_n:
                od = "o"
                index = int(temp_index / pattern_3_n)
                drawn_card = originals[drawn_player].pop(index)

                history[turn][3] = 0
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)

            elif temp_index >= len(originals[drawn_player])*pattern_3_n:
                od = "d"
                index = int((temp_index - len(originals[drawn_player])*pattern_3_n) / pattern_3_m)
                drawn_card = drawns[drawn_player].pop(index)

                history[turn][3] = 1
                history[turn][4] = index
                history[turn][5] = drawn_card

                his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
                his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
                update_history(his1,turn_player)
                update_history(his2,drawn_player)

            return drawn_card




def newJudge_with_com(turn_player, drawn_card):
    drawn_card_num = drawn_card%13
    flug = False  #カードが揃ったら、Trueになる
    tmp = 0
    sorottatokoro = None
    sorottacard = None   #success_cardの数字のことだ！
    success_card = 0
    for i, x in enumerate(originals[turn_player]):
        if x%13 == drawn_card_num:  #もしオリジナルで揃ったら
            sorottatokoro = 'Originalsのindex ' + str(i) + ' '

            history[turn][9] = 0
            history[turn][10] = i

            sorottacard = x%13 if x%13 != 0 else 13

            originals[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None
            ages[x] = None #agesに揃ったことを意味するNoneを代入
            ages[drawn_card] = None
            for pn in range(4):
                tmp = player[pn].cell(x%13 if x%13 !=0 else 13,20).value
                player[pn].update_cell(x%13 if x%13 !=0 else 13,20,int(tmp)+2)
            flug = True
            success_card = x
    for i, x in enumerate(drawns[turn_player]):
        if x%13 == drawn_card_num:  #もし引き札で揃ったら
            sorottatokoro = 'Drawnsのindex ' + str(i) + ' '

            history[turn][9] = 1
            history[turn][10] = i

            sorottacard = x%13 if x%13 != 0 else 13

            drawns[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None
            ages[x] = None #agesに揃ったことを意味するNoneを代入
            ages[drawn_card] = None
            for pn in range(4):
                tmp = player[pn].cell(x%13 if x%13 !=0 else 13,20).value
                player[pn].update_cell(x%13 if x%13 !=0 else 13,20,int(tmp)+2)
            flug = True
            success_card = x
    if flug == False:
        drawns[turn_player].append(drawn_card)
        places[drawn_card] = turn_player
    #print("そろったかどうか＝{}".format(flug))
    return flug,sorottatokoro,sorottacard, success_card


def newdraw_with_com(turn_player, drawn_player):
    drawn_card = newInputCard_with_com(drawn_player,turn_player)

    flug_of_judge,sorottatokoro,sorottacard,success_card = newJudge_with_com(turn_player,drawn_card)
    history[turn][6] = int(flug_of_judge)  #カードを引くための関数。毎ターン、多くても一回呼び出される。

    return sorottatokoro,sorottacard,drawn_card, flug_of_judge, success_card


def update_history(rireki,player_index):
    temp = ['','','','']
    if player_index == 4:
        for pn in range(4):
            cell_list = player[pn].range(23,3,26,3)
            temp[0] = rireki
            temp[1] = cell_list[0].value
            temp[2] = cell_list[1].value
            temp[3] = cell_list[2].value
            for i in range(4):
                cell_list[i].value = temp[i]

            player[pn].update_cells(cell_list)
    else:
        pn = player_index
        cell_list = player[pn].range(23,3,26,3)
        temp[0] = rireki
        temp[1] = cell_list[0].value
        temp[2] = cell_list[1].value
        temp[3] = cell_list[2].value
        for i in range(4):
            cell_list[i].value = temp[i]

        player[pn].update_cells(cell_list)

def print_turn(turn):
    for pn in range(4):
        player[pn].update_acell('C21','現在はプレイヤー' + str(turn) + 'のターン')

def clear_log():
    temp = ['','log','','','','']
    for pn in range(4):
        cell_list = player[pn].range(21,3,26,3)
        for i in range(6):
            cell_list[i].value = temp[i]
        player[pn].update_cells(cell_list)


#zizi確関数１。任意のinputの段階で、zizikakuと入力されたら、起動。
#ziziの数字を答えてもらう。最大1入力。
#引数はターンとターンプレイヤー。
def zizikaku1(turn, turn_player):
    if zizikaku_used[turn_player] != 1:
        estimated_zizi_num = 0
        flug = False
        while flug == False:
            try:
                estimated_zizi_num = int(input("あなたが予想する、ziziの数字を入力してください。"))
                if estimated_zizi_num > 0 and estimated_zizi_num <= 13:
                    flug = True
                else:
                    print("正しく入力してください。")
            except ValueError:
                print("整数値で答えてください。")
        zizikaku1_lst[turn_player][0] = turn
        zizikaku1_lst[turn_player][1] = estimated_zizi_num
        zizikaku_used[turn_player] = 1
    elif zizikaku_used[turn_player] == 1:
        print("あなたはすでにzizi確ボタンを使っています。")


#zizi確関数２。任意のinputの段階で、zizikakuと入力されたら、起動。
#ziziの場所を答えてもらう。最大3入力。
def zizikaku2(turn, turn_player):
    if zizikaku_used[turn_player] != 1:
        candidates_num = 0
        flug1 = False  #候補数のinput
        while flug1 == False:
            try:
                candidates_num = int(input("あなたの予想するziziのありかの候補数を入力してください。"))
                if candidates_num > 0 and candidates_num < 4:   #候補数は1~3
                    flug1 = True
                else:
                    print("正しく入力してください。")
            except ValueError:
                print("整数値で答えてください。")
        for i in range(0, candidates_num):
            estimated_zizi_belonging_to_player = 0
            estimated_o_or_d = ""
            estimated_index = 0
            flug2 = False  #playerのinput
            flug3 = False  #indexのinput
            flug4 = False  #o or dのinput
            print(" ")
            print("第{}候補について入力してください。".format(i+1))
            while flug2 == False:
                try:
                    estimated_zizi_belonging_to_player = int(input("ziziを持っていると思われるプレイヤーの番号を入力してください。"))
                    if estimated_zizi_belonging_to_player >=0 and estimated_zizi_belonging_to_player <4 and (originals[estimated_zizi_belonging_to_player] != [] or drawns[estimated_zizi_belonging_to_player] != []):   #player番号は0~3
                        flug2 = True
                    else:
                        print("正しく入力してください。")
                except ValueError:
                    print("整数値で答えてください。")
            #print(drawns[estimated_zizi_belonging_to_player])
            while flug4 == False:
                estimated_o_or_d = input("originals or drawns?   o or d:   ")
                if estimated_o_or_d == "o" and originals[estimated_zizi_belonging_to_player] != []:
                    flug4 = True
                    while flug3 == False:
                        try:
                            estimated_index = int(input("インデックスを入力してください。"))
                            if estimated_index >=0 and estimated_index < len(originals[estimated_zizi_belonging_to_player]):  #index out of rangeにならないように。
                                flug3 = True
                            else:
                                print("正しく入力してください。")
                        except ValueError:
                            print("整数値で答えてください。")
                    zizikaku2_lst[turn_player][0] = turn
                    zizikaku2_lst[turn_player][i+1] = originals[estimated_zizi_belonging_to_player][estimated_index]
                elif estimated_o_or_d == "d" and drawns[estimated_zizi_belonging_to_player] != []:
                    flug4 = True
                    while flug3 == False:
                        try:
                            estimated_index = int(input("インデックスを入力してください。"))
                            if estimated_index >=0 and estimated_index < len(drawns[estimated_zizi_belonging_to_player]):   #index out of rangeにならないように。
                                flug3 = True
                            else:
                                print("正しく入力してください。")
                        except ValueError:
                            print("整数値で答えてください。")
                    zizikaku2_lst[turn_player][0] = turn
                    zizikaku2_lst[turn_player][i+1] = drawns[estimated_zizi_belonging_to_player][estimated_index]
                else:
                    print("正しく入力してください。")
        zizikaku_used[turn_player] = 1
    elif zizikaku_used[turn_player] == 1:
        print("あなたはすでにzizi確ボタンを使っています。")


#初めに棋譜を作成する関数。pythonのコードは、配列はグローバルに渡せるので、特に引数にはしていません。返り値は初めのカードの枚数。
def kihu_init(kihu):
    #まず、場に何枚あるか数える
    cards_at_field_num_at_first = 0
    for i in range(1,len(places)):
        if places[i] != None:
            cards_at_field_num_at_first += 1

    #print(cards_at_field_num_at_first)

    #次に、表を作成する
    kihu = [[None] * ( cards_at_field_num_at_first + 5 ) for i in range(0, cards_at_field_num_at_first)]

    #プレイヤー0のカードから順に背番号を振っていく
    start = 0
    for player_num in range(0,4):
        for i in range(start, start + len(originals[player_num])):
            kihu[i][cards_at_field_num_at_first] = originals[player_num][i - start]
        start += len(originals[player_num])

    #それぞれのプレイヤーの手札で共存しているカードに0を記入
    start = 0
    for player_num in range(0,4):
        for i in range(start, start + len(originals[player_num])):
            for j in range(start, start + len(originals[player_num])):
                kihu[i][j] = 0
        start += len(originals[player_num])

    #それぞれのプレイヤーが見ているカードを記入
    start = 0
    for player_num in range(0,4):
        for i in range(start, start + len(originals[player_num])):
            kihu[i][cards_at_field_num_at_first + 1 + player_num] = kihu[i][cards_at_field_num_at_first]
        start += len(originals[player_num])

    return cards_at_field_num_at_first, kihu


#棋譜にそのターンの成果を記入する関数。draw関数を実行した後に呼び出すこと。
def kihu_write(turn, turn_player, drawn_card, flug_of_judge, success_card, cards_at_field_num_at_first):
    if flug_of_judge == True:
        for i in range(0, cards_at_field_num_at_first):
            if kihu[i][cards_at_field_num_at_first] == drawn_card: #もし、背番号iのカードの表の番号（リアルナンバー）が揃ったカードの引き札の番号なら
                for j in range(0, cards_at_field_num_at_first): #タテに回す
                    if kihu[i][j] == None:
                        kihu[i][j] = turn
                for j in range(0, cards_at_field_num_at_first): #ヨコに回す
                    if kihu[j][i] == None:
                        kihu[j][i] = turn
                for j in range(cards_at_field_num_at_first + 1, cards_at_field_num_at_first + 5):
                    kihu[i][j] = kihu[i][cards_at_field_num_at_first] #みんなに揃ったカードの数字がわかる
            elif kihu[i][cards_at_field_num_at_first] == success_card: #もし、背番号iのカードの表の番号（リアルナンバー）が揃った引き札のカードの相手の番号なら
                for j in range(0, cards_at_field_num_at_first): #タテに回す
                    if kihu[i][j] == None:
                        kihu[i][j] = turn
                for j in range(0, cards_at_field_num_at_first): #ヨコに回す
                    if kihu[j][i] == None:
                        kihu[j][i] = turn
                for j in range(cards_at_field_num_at_first + 1, cards_at_field_num_at_first + 5):
                    kihu[i][j] = kihu[i][cards_at_field_num_at_first] #みんなに揃ったカードの数字がわかる
    elif flug_of_judge == False:
        #まず、引いたカードの背番号を取得
        back_num_of_drawn_card = 0
        for i in range(0, cards_at_field_num_at_first):
            if kihu[i][cards_at_field_num_at_first] == drawn_card:
                back_num_of_drawn_card = i
        for i in range(0, cards_at_field_num_at_first):
            if places[kihu[i][cards_at_field_num_at_first]] == turn_player: #それぞれのカードの背番号をみて、その持ち主がターンプレイヤーであるカードについて処理をする
                if kihu[i][back_num_of_drawn_card] == None:
                    kihu[i][back_num_of_drawn_card] = turn
                if kihu[back_num_of_drawn_card][i] == None: #対称的に
                    kihu[back_num_of_drawn_card][i] = turn
        kihu[back_num_of_drawn_card][cards_at_field_num_at_first + 1 + turn_player] = kihu[back_num_of_drawn_card][cards_at_field_num_at_first] #今のターンプレイヤーには引いたカードの情報がわかる
        #kihu[back_num_of_drawn_card][cards_at_field_num_at_first + 1 + turn_player] = drawn_cardでも良い。

def countN(lst):
    cnt = 0
    for i in range(len(lst)):
        if lst[i] == None:
            cnt += 1
    return cnt


def public_zizikaku(kihu, cards_at_field_num_at_first):
    zizi_num = None
    cnt = 0
    for i in range(cards_at_field_num_at_first):
        if places[kihu[i][cards_at_field_num_at_first]] != None:  #背番号iのカードがまだ場にあるとき。
            if countN(kihu[i][0:cards_at_field_num_at_first]) == 0:
                print("ziziの数字は{}とわかりました！！！！！".format(kihu[i][cards_at_field_num_at_first]%13 if kihu[i][cards_at_field_num_at_first]%13 =! 13 else 13 ))
                zizi_num = kihu[i][cards_at_field_num_at_first]%13 if kihu[i][cards_at_field_num_at_first]%13 =! 13 else 13
                #zizi_back_num = i
                cnt += 1
    if cnt == 1:
        return zizi_num#, zizi_back_num
    elif cnt == 0:
        print("まだパブリックジジ確はしていません。")
    else:
        print("ジジの数字が２つ以上あります。エラーです。")

def find_pair(kihu, cards_at_field_num_at_first, player_number):
    tmp_pair_candidates = [[] for i in range(cards_at_field_num_at_first)]  #その背番号のカードの、ペア候補が入っている
    pairs = []
    for i in range(cards_at_field_num_at_first):
        if places[kihu[i][cards_at_field_num_at_first]) != None:  #背番号iのカードがまだ場にあるとき。
            if countN(kihu[i][0:cards_at_field_num_at_first]) == 1:  #背番号iのカードのペアとなる候補が１つに絞られている時
                tmp_pair_candidates[i].append(kihu[i][0:cards_at_field_num_at_first].index(None))  #相手の札の背番号を入れる
    for i in range(0, cards_at_field_num_at_first):
        for j in range(0, len(tmp_pair_candidates[i])):
            if i < tmp_pair_candidates[i][j]:
                if len(tmp_pair_candidates[i]) == 1 and len(tmp_pair_candidates[tmp_pair_candidates[i][j]]) == 1 and i in tmp_pair_candidates[tmp_pair_candidates[i][j]] and :
                    pairs.append((i, j))
    return pairs

def blank_nums_init(places, zizi_index):   #どの数字がターン０でblankかをだす
    blank_nums = [None] * 14 #初めのインデックスは使わない
    for i in range(1,14):
        tmp_number = 0
        for j in range(4):
            if places[i+13*j] == None and i+13*j != zizi_index:
                tmp_number += 1
        if tmp_number == 0:
            blank_nums[i] = i
    return  blank_nums

def field_cards_init(kihu, cards_at_field_num_at_first):  #ターン0で、どの背番号のカードがどのプレイヤーにあるかを書き出す。
    field_cards_at_first = [[], [], [], []]
    for i in range(0,4):
        for j in range(cards_at_field_num_at_first):
            if kihu[j][j] == 0 and kihu[j][cards_at_field_num_at_first + 1+i] != None:
                field_cards_at_first[i].append(j)  #各プレイヤーの手札の背番号を代入
    print(field_cards_at_first)
    return field_cards_at_first


#field_cards_with_each_players_knowledge。　場にあるカードを、自分のもつ知識と共に、絞る
#そのプレイヤー目線の、blankのありかを入れた配列を作る。背番号で。
def blank_list(kihu, cards_at_field_num_at_first, field_cards_at_first, blank_number, player_number):
    blank_list = [[], [], [], []]
    for i in range(0,4):
        flag_known_blank_exist = False
        strage_of_tmp_back_number = None
        for j in range(0, len(field_cards_at_first[i])):
            tmp_back_number = field_cards_at_first[i][j]
            tmp_card_number = kihu[tmp_back_number][cards_at_field_num_at_first +1+player_number] #これがNoneでないときは、そのカードを知っているってこと。
            if tmp_card_number == blank_number or tmp_card_number == blank_number +13 or tmp_card_number == blank_number +26 or tmp_card_number == blank_number + 39:  #そのカードをそのプレイヤーが知っていて、しかもそれが、今考えているblank_numberなら
                flag_known_blank_exist = True
                strage_of_tmp_back_number = tmp_back_number
        if flag_known_blank_exist == True:  #プレイヤーiの手札の中に、自分が知っているblankカードがあるとき、
            blank_list[i].append(strage_of_tmp_back_number)
        else:  #プレイヤーiの手札の中に、自分が知っているblankカードがないとき、
            for j in range(0, len(field_cards_at_first[i])):
                tmp_back_number = field_cards_at_first[i][j]
                tmp_card_number = kihu[tmp_back_number][cards_at_field_num_at_first +1+player_number]
                if tmp_card_number == None: #そのカードを知らないとき
                    blank_list[i].append(tmp_back_number)
                else:  #そのカードを知っているとき。それはblankカードではないってことになっているので、
                    pass
    return blank_list







turn_player_win = False #active win した人がいるかどうか
drawn_player_win = False #passive win した人がいるかどうか
global loser_exist
loser_exist = False
next_turn_player = 0
previous_turn_num = 0
#age_increase = False

cards_at_field_num_at_first, kihu = kihu_init(kihu)


#print("zizi_index = {}".format(zizi_index))   #ziziチェック用。
clear_log()

for pn in range(4):
    showField(pn,originals,drawns)
init_opensource(places,zizi_index)

update_history('シャッフル完了、ゲームを開始します',4)

while loser_exist == False:
    print_turn(turn%4)
    turn_player = turn%4

    print("turn = {}".format(turn))

    history[turn][0] = turn
    history[turn][1] = turn_player

    time.sleep(2)




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
                print("ビリが確定しました")
                print(" ")
                break
        time.sleep(2)

    else:   #もし、先のターンの人が上がってなかったら、次に順番が回ってきた人は、先のターンの人から一枚引き抜き、
        drawn_player = turn%4
        for cnt in range(1,4):
            if originals[(turn - cnt)%4] != [] or drawns[(turn - cnt)%4] != []:
                drawn_player = (turn -cnt)%4
                break
        history[turn][2] = drawn_player




        sorottatokoro,sorottacard, drawn_card, flug_of_judge, success_card = newdraw_with_com(turn_player, drawn_player)

        kihu_write(turn, turn_player, drawn_card, flug_of_judge, success_card, cards_at_field_num_at_first)

        for pn in range(4):
            showField(pn,originals,drawns)
        result = 'プレイヤー' + str(turn_player) + 'が、プレイヤー' + str(drawn_player) + 'の'
        if history[turn][3] == 0:
            result += 'Originals から'
        else:
            result += 'Drawns から'

        result = result + 'index {} のカードをひき、'.format(history[turn][4])

        if sorottatokoro == None:
            result += 'そろいませんでした'
        else:
            result = result +  'プレイヤー' + str(turn_player) + 'の' + sorottatokoro + 'とそろいました。' + 'カードは' + str(sorottacard)

        update_history(result,4)




        if originals[drawn_player] == [] and drawns[drawn_player] == []:  #もし、引かれた人の手札が空になったら、その人は上がり。
            drawn_player_win == True
            orders.append(drawn_player)
            print("プレイヤー{}さんが上がりました".format(drawn_player))
            update_history("プレイヤー{}さんが上がりました".format(drawn_player),4)
            print(" ")
            history[turn][7] = 1
        if originals[turn_player] == [] and drawns[turn_player] == []:   #もし、引いた人の手札が空になったら、その人は上がり。
            turn_player_win = True
            orders.append(turn_player)
            print("プレイヤー{}さんが上がりました".format(turn_player))
            update_history("プレイヤー{}さんが上がりました".format(turn_player),4)
            print(" ")
            history[turn][8] = 1

        for i in range(0,len(ages)):
            if ages[i] == None or ages[i] == 0:   #ziziのカードや、すでに揃ったカード、まだ誕生していないカードには、何もしない。
                pass
            else:
                ages[i] = ages[i] + (turn - previous_turn_num)   #それ以外の、すでに誕生していたカードには、先のターンから今のターンの差の分を加算。
        for i in range(0,len(places)):
            if places[i] != history_of_places[0][i] and ages[i] == 0:   #これまで0歳だったのに、このターンでplacesが変わったカードについて。
                ages[i] = 1   #誕生したことを示す、1。

        time.sleep(2)

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
                print("ビリが確定しました。")
                print(" ")
                break

    if turn_player not in com_player_nums:   #turn_playerがcomではないならば
        #zizi確関数呼び出し
        zizikaku_input_flug1 = False
        if turn%4 in com_player_nums:
            zizikaku_input_flug1 = True
        else:
            while zizikaku_input_flug1 == False:
                zizikaku_exist = input("zizi確ボタンを使いますか？ y or n:  ")
                if zizikaku_exist == "y":
                    zizikaku_func_num = input("どちらのzizi確関数を使いますか？　1 or 2:  ")
                    if zizikaku_func_num == "1":
                        zizikaku1(turn, turn%4)
                        zizikaku_input_flug1 = True
                    elif zizikaku_func_num == "2":
                        zizikaku2(turn, turn%4)
                        zizikaku_input_flug1 = True
                    else:
                        print("正しく入力してください。")
                elif zizikaku_exist == "n":
                    zizikaku_input_flug1 = True
                else:
                    print("正しく入力してください。。")


    print("kihu is below")
    for i in range(0, cards_at_field_num_at_first):
        for j in range(0, cards_at_field_num_at_first):
            if kihu[i][j] == None:
                print("None", end = "  ")
            elif kihu[i][j] == 0:
                print("\033[40m" + "  0 " + "\033[0m", end = "  ")
            elif kihu[i][j] == 1:
                print("\033[41m" + "  1 " + "\033[0m", end = "  ")
            elif kihu[i][j] == 2:
                print("\033[44m" + "  2 " + "\033[0m", end = "  ")
            elif kihu[i][j] == 3:
                print("\033[43m" + "  3 " + "\033[0m", end = "  ")
            elif kihu[i][j] == 4:
                print("\033[42m" + "  4 " + "\033[0m", end = "  ")
            elif kihu[i][j] == 5:
                print("\033[47m" + " " + "\033[0m" + "\033[41m" + " 5" + "\033[0m" + "\033[47m" + " " + "\033[0m", end = "  ")
            elif kihu[i][j] == 6:
                print("\033[47m" + " " + "\033[0m" + "\033[44m" + " 6" + "\033[0m" + "\033[47m" + " " + "\033[0m", end = "  ")
            elif kihu[i][j] == 7:
                print("\033[47m" + " " + "\033[0m" + "\033[43m" + " 7" + "\033[0m" + "\033[47m" + " " + "\033[0m", end = "  ")
            elif kihu[i][j] == 8:
                print("\033[47m" + " " + "\033[0m" + "\033[42m" + " 8" + "\033[0m" + "\033[47m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 9:
            #    print("\033[40m" + " " + "\033[0m" + "\033[41m" + " 9" + "\033[0m" + "\033[40m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 10:
            #    print("\033[40m" + " " + "\033[0m" + "\033[44m" + "10" + "\033[0m" + "\033[40m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 11:
            #    print("\033[40m" + " " + "\033[0m" + "\033[43m" + "11" + "\033[0m" + "\033[40m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 12:
            #    print("\033[40m" + " " + "\033[0m" + "\033[42m" + "12" + "\033[0m" + "\033[40m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 13:
            #    print("\033[46m" + " " + "\033[0m" + "\033[41m" + "13" + "\033[0m" + "\033[46m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 14:
            #    print("\033[46m" + " " + "\033[0m" + "\033[44m" + "14" + "\033[0m" + "\033[46m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 15:
            #    print("\033[46m" + " " + "\033[0m" + "\033[43m" + "15" + "\033[0m" + "\033[46m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 16:
            #    print("\033[46m" + " " + "\033[0m" + "\033[42m" + "16" + "\033[0m" + "\033[46m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 17:
            #    print("\033[45m" + " " + "\033[0m" + "\033[41m" + "17" + "\033[0m" + "\033[45m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 18:
            #    print("\033[45m" + " " + "\033[0m" + "\033[44m" + "18" + "\033[0m" + "\033[45m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 19:
            #    print("\033[45m" + " " + "\033[0m" + "\033[43m" + "19" + "\033[0m" + "\033[45m" + " " + "\033[0m", end = "  ")
            #elif kihu[i][j] == 20:
            #    print("\033[45m" + " " + "\033[0m" + "\033[42m" + "20" + "\033[0m" + "\033[45m" + " " + "\033[0m", end = "  ")
            else:
                print(" " + "{:>2}".format(kihu[i][j]) + " ", end = "  ")
        print("    ", end  = "")
        for j in range(cards_at_field_num_at_first, cards_at_field_num_at_first + 5):
            if kihu[i][j] == None:
                print("None", end = "  ")
            else:
                print("{:>4}".format(kihu[i][j]), end = "  ")
        print("\n")
    print("")
    print("")
    print("")




#ターンの最後


print(" ")
update_history('ゲーム終了',4)

if zizi_index %13 == 0:
    zizi_num = 13
else:
    zizi_num = zizi_index%13
print("ziziは{}{:02d}でした。".format(marks[int((zizi_index-1)/13)], zizi_num))
print(" ")
print("順位は")
for i in range(len(orders)):
    print("{}位がプレイヤー{}さんでした。".format(i+1, orders[i]))
for i in range(len(orders)):
    update_history("{}位がプレイヤー{}さんでした。".format(i+1, orders[i]),4)
print(" ")
print("以下に、このゲームの履歴を表示します。")
print(" ")


print("history_of_places is below")
print("cards\' index is         =  ", end = "")
print("[", end = " ")
for i in range(1,5):
    for j in range(1,14):
        print("{}{:02d}".format(marks[i-1],  j), end = " ")
print("]")
for i in range(len(history_of_places)):
    if history_of_places[i] != [None]*53:
        print("at the {0:2d}th turn, places =".format(i), end = " ")
        print("[", end = " ")
        for j in range(1,len(history_of_places[i])):  #placesの1から52までを表示。
            if history_of_places[i][j] == None:
                print("   ", end = " ")
            elif history_of_places[i][j] != None:
                print("{0:3d}".format(history_of_places[i][j]), end = " ")
        print("]")
print(" ")


print(" ")
print("history_of_ages is below")
print("cards\' index is         =  ", end = "")
print("[", end = " ")
for i in range(1,5):
    for j in range(1,14):
        print("{}{:02d}".format(marks[i-1],  j), end = " ")
print("]")
for i in range(len(history_of_ages)):
    if history_of_ages[i] != [None] * 53:
        print("at the {0:2d}th turn, ages   =".format(i), end = " ")
        print("[", end = " ")
        for j in range(1,len(history_of_places[i])):  #agesの1から52までを表示。
            if history_of_ages[i][j] == None:
                print("   ", end = " ")
            elif history_of_ages[i][j] != None:
                print("{0:3d}".format(history_of_ages[i][j]), end = " ")
        print("]")
print(" ")


print("history is below")
for i in range(1, turn):
    if history[i][2] != None:   #飛ばされたターンについては表示しない
        print("turn{:02d}はプレイヤー{}さんが、プレイヤー{}さんの".format(history[i][0], history[i][1], history[i][2]), end = "")
        if history[i][3] == 0:
            print("オリジナルの", end = "")
        elif history[i][3] == 1:
            print("  引き札の  ", end = "")
        #print("インデックス{}から{:02d}を引き,".format(history[i][4], history[i][5]), end = "")
        print("インデックス{}から ".format(history[i][4]), end = "")
        print("{}{:02d}を引き、".format(marks[int((history[i][5]-1)/13)], history[i][5]%13 if history[i][5]%13 != 0 else 13), end ="")
        if history[i][6] == 0:
            print("そろいませんでした。", end = "")
        elif history[i][6] == 1:
            print("そろいました。", end = "")
        if history[i][7] == 1:
            print("引かれたプレイヤーが上がりました。", end = "")
        if history[i][8] == 1:
            print("ターンプレイヤーが上がりました。", end = "")
    print(" ")
print(" ")

print("以下に、zizi確の結果を表示します。")
"""for i in range(0,4):
    print("zizikaku1_lst = {}".format(zizikaku1_lst))
    print("zizikaku2_lst = {}".format(zizikaku2_lst))
    print("zizikaku_used = {}".format(zizikaku_used))  #zizikaku関数による代入のチェック用。"""
zizikaku2_correct = False
for player in range(0,4):
    used_zizikaku_func = 0
    if zizikaku1_lst[player] != [None, None]:
        used_zizikaku_func = 1
        print("プレイヤー{}さんは、zizi確関数{}を使用し、".format(player, used_zizikaku_func), end ="")
        print("turn = {}の時に、予想した数字は{}でした。".format(zizikaku1_lst[player][0], zizikaku1_lst[player][1]), end = "")
        if zizikaku1_lst[player][1] == zizi_num:
            print("その結果は正解でした。")
        else:
            print("その結果は不正解でした。")
    elif zizikaku2_lst[player] != [None, None, None, None]:
        used_zizikaku_func = 2
        print("プレイヤー{}さんは、zizi確関数{}を使用し、".format(player, used_zizikaku_func), end ="")
        print("turn = {}の時に、".format(zizikaku2_lst[player][0]), end = "")
        for candidates in range(1,4):
            if zizikaku2_lst[player][candidates] != None:
                print("第{}候補として予想したカードの数字は{}でした。".format(candidates, zizikaku2_lst[player][candidates]), end = "")
                if zizikaku2_lst[player][candidates] == zizi_num:
                    print("これが正解でした。", end ="")
                    zizikaku2_correct = True
        if zizikaku2_correct == False:
            print("全て不正解でした。")
    else:
        print("プレイヤー{}さんは、zizi確関数を使用していません。".format(player))
print(" ")
print(" ")
print("以上で、全て終了です。お疲れ様でした。")
print(" ")
