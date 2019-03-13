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


marks = ["♤", "♡", "♧", "♢"]

def Debug():
    for pn in range(4):
        showField(pn,originals,drawns)
    #print(zizi_index)
    init_opensource(places,zizi_index)
    for i in range(5):
        update_history('ゲームを開始します'+ str(i),4)

def next(player_number,i):
    return (player_number + i) % 4

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

def newInputCard(player_num,turn_player):  #player_numはひかれる人
    global loser_exist
    od = ''
    index = ''
    drawn_card = 0
    while (od == '' or index == ''):
        t_start = time.time()
        while(True):
            t_temp = time.time()
            if t_temp - t_start > 1:
                break
        cell_list = player[turn_player].range(19,4,20,4)
        od = cell_list[0].value
        index = cell_list[1].value

    if od =='o' or od == '0':
        try:
            drawn_card = originals[player_num].pop(int(index))

            history[turn][3] = 0
            history[turn][4] = index
            history[turn][5] = drawn_card

            his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
            his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
            update_history(his1,turn_player)
            update_history(his2,player_num)

            #ここに、odとindexを受け取ったら、そのセルを空白にする処理を書けば良さそう。
            cell_list[0].value = ''
            cell_list[1].value = ''
            player[turn_player].update_cells(cell_list)




            return drawn_card
        except:
            cell_list[0].value = ''
            cell_list[1].value = ''
            player[turn_player].update_cells(cell_list)
            return newInputCard(player_num,turn_player)

    elif od == 'd' or od == '1':
        try:
            drawn_card = drawns[player_num].pop(int(index))
            history[turn][3] = 1
            history[turn][4] = index
            history[turn][5] = drawn_card

            his1 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引きました"
            his2 = marks[int((drawn_card-1)/13)] + str(drawn_card%13 if drawn_card%13 != 0 else 13) + "を引かれました"
            update_history(his1,turn_player)
            update_history(his2,player_num)


            #ここに、odとindexを受け取ったら、そのセルを空白にする処理を書けば良さそう。
            cell_list[0].value = ''
            cell_list[1].value = ''
            player[turn_player].update_cells(cell_list)




            return drawn_card
        except:
            cell_list[0].value = ''
            cell_list[1].value = ''
            player[turn_player].update_cells(cell_list)
            return newInputCard(player_num,turn_player)

    elif od == 'quit':
        loser_exist = True
        print('quitされました')
        return newInputCard(player_num,turn_player)

    else:
        cell_list[0].value = ''
        cell_list[1].value = ''
        player[turn_player].update_cells(cell_list)
        return newInputCard(player_num,turn_player)



def newJudge(turn_player, drawn_card):
    drawn_card_num = drawn_card%13
    flug = False  #カードが揃ったら、Trueになる
    tmp = 0
    sorottatokoro = None
    sorottacard = None
    for i, x in enumerate(originals[turn_player]):
        if x%13 == drawn_card_num:  #もしオリジナルで揃ったら
            sorottatokoro = 'Originalsのindex ' + str(i) + ' '

            #ここで、全員に x%13　を表示させれば良い
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
    for i, x in enumerate(drawns[turn_player]):
        if x%13 == drawn_card_num:  #もし引き札で揃ったら
            sorottatokoro = 'Drawnsのindex ' + str(i) + ' '
            sorottacard = x%13 if x%13 != 0 else 13

            #ここで、全員に x%13　を表示させれば良い


            drawns[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None
            ages[x] = None #agesに揃ったことを意味するNoneを代入
            ages[drawn_card] = None
            for pn in range(4):
                tmp = player[pn].cell(x%13 if x%13 !=0 else 13,20).value
                player[pn].update_cell(x%13 if x%13 !=0 else 13,20,int(tmp)+2)
            flug = True
    if flug == False:
        drawns[turn_player].append(drawn_card)
        places[drawn_card] = turn_player
    print("そろったかどうか＝{}".format(flug))
    print(" ")
    return flug,sorottatokoro,sorottacard

def draw(turn_player, drawn_player):
    drawn_card = newInputCard(drawn_player,turn_player)

    flag,sorottatokoro,sorottacard = newJudge(turn_player,drawn_card)
    history[turn][6] = int(flag)  #カードを引くための関数。毎ターン、多くても一回呼び出される。

    return sorottatokoro,sorottacard

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

'''
cell_value = player[1].acell('A1').value
print(cell_value)
cell_value = player[2].acell('A1').value
print(cell_value)
cell_value = player[3].acell('B1').value
print(cell_value)
'''




import random


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


#numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

history = [[None]*9 for i in range(101)]  #100ターン分用意しとく。この配列のみ、関数の中で、globalに変更しないといけない。
#中身の配列の意味は、[turn, turn_player, drawn_player, originals or drawns(0 or 1), index, drawn_card, そろったか(0 or 1), drawn_player_win(None or 1), turn_player_win(None or 1)]
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
history[0] = [None]*9








turn_player_win = False #active win した人がいるかどうか
drawn_player_win = False #passive win した人がいるかどうか
global loser_exist
loser_exist = False
next_turn_player = 0
previous_turn_num = 0
#age_increase = False

#print("zizi_index = {}".format(zizi_index))   #ziziチェック用。
clear_log()

for pn in range(4):
    showField(pn,originals,drawns)
init_opensource(places,zizi_index)

update_history('シャッフル完了、ゲームを開始します',4)

while loser_exist == False:
    print_turn(turn%4)
    turn_player = turn%4

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
                print("ビリが確定しました")
                print(" ")
                break

    else:   #もし、先のターンの人が上がってなかったら、次に順番が回ってきた人は、先のターンの人から一枚引き抜き、
        drawn_player = turn%4
        for cnt in range(1,4):
            if originals[(turn - cnt)%4] != [] or drawns[(turn - cnt)%4] != []:
                drawn_player = (turn -cnt)%4
                break
        history[turn][2] = drawn_player




        sorottatokoro,sorottacard = draw(turn_player, drawn_player)
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
print("cards\' index is      =      ", end = "")
print("[", end = " ")
for i in range(1,5):
    for j in range(1,14):
        print("{}{:02d}".format(marks[i-1],  j), end = " ")
print("]")
for i in range(len(history_of_places)):
    if history_of_places[i] != [None]*53:
        print("at the {0:2d}th turn, places = ".format(i), end = " ")
        print("[", end = " ")
        for j in range(1,len(history_of_places[i])):  #placesの1から52までを表示。
            if history_of_places[i][j] == None:
                print("  ○", end = " ")
            elif history_of_places[i][j] != None:
                print("{0:3d}".format(history_of_places[i][j]), end = " ")
        print("]")
print(" ")


print(" ")
print("history_of_ages is below")
print("cards\' index is      =      ", end = "")
print("[", end = " ")
for i in range(1,5):
    for j in range(1,14):
        print("{}{:02d}".format(marks[i-1],  j), end = " ")
print("]")
for i in range(len(history_of_ages)):
    if history_of_ages[i] != [None] * 53:
        print("at the {0:2d}th turn, ages   = ".format(i), end = " ")
        print("[", end = " ")
        for j in range(1,len(history_of_places[i])):  #agesの1から52までを表示。
            if history_of_ages[i][j] == None:
                print("  ○", end = " ")
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
