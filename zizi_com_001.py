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

marks = ["S", "H", "C", "D"]
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
com_player_pattern = [3,1,1,2 ]  #com_player_numsになってるインデックスに、そのcomのパターンを記入すること。
#パターン０がとにかくオリジナルから引く。
#パターン１がとにかく引き札から引く。
#パターン２が完全ランダムで引く。
#パターン３がオリジナルから：引き札から＝n:mの確率でランダムで引く。より詳しく言えば、オリジナルのカードにn倍、引き札のカードにm倍の重みをつけてランダムに選ぶ。
global pattern_3_n
global pattern_3_m
pattern_3_n = 5
pattern_3_m = 5
#整数値にして下さい




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


#引くカードの入力＆引かれた側の配列操作
def input_card(player_num): #引数は引かれる人の番号。返り値は引いたカード。この関数の中で、選択されたカードをポップする。
    flug = False #この関数の目的が達成されれば、Trueとなり、この関数を抜ける
    drawn_card = 0
    while flug == False:
        print("引くカードを入力してください。")
        input1 = input("originals　or drawns?   o or d:   ")
        print(" ")
        if input1 == "o" and originals[player_num] != []:
            try:
                input2 = int(input("インデックスを入力してください。:   "))
                print(" ")
                if input2 >= 0 and input2 <len(originals[player_num]):#originals[player_num][input2] != None:
                    input3 = input("それでいいですか y or n:   ")
                    print(" ")
                    if input3 == "y":
                        drawn_card = originals[player_num].pop(input2)
                        flug = True

                        history[turn][3] = 0
                        history[turn][4] = input2
                        history[turn][5] = drawn_card


                    else:
                        print("正しく入力してください。")
                        print(" ")
                        continue
            except ValueError:
                print("半角で正しく入力してください。")
                print(" ")
                continue
        elif input1 == "d" and drawns[player_num] != []:
            try:
                input2 = int(input("インデックスを入力してください。:   "))
                print(" ")
                if input2 >= 0 and input2 < len(drawns[player_num]):#drawns[player_num][input2] != None:
                    input3 = input("それでいいですか y or n:   ")
                    print(" ")
                    if input3 == "y":
                        drawn_card = drawns[player_num].pop(input2)
                        flug = True

                        history[turn][3] = 1
                        history[turn][4] = input2
                        history[turn][5] = drawn_card


                    else:
                        print("正しく入力してください。")
                        print(" ")
                        continue
            except ValueError:
                print("半角で正しく入力してください。")
                print(" ")
                continue
        else:
            print("正しく入力してください。")
            print(" ")
            continue
    print("引いたのは{}{:02d}でした。".format(marks[int((drawn_card-1)/13)], drawn_card%13 if drawn_card%13 != 0 else 13))
    print(" ")
    return drawn_card


def input_card_com_exist_ver(turn_player, drawn_player):
    drawn_card = 0
    if turn_player not in com_player_nums:
        flug = False #この関数の目的が達成されれば、Trueとなり、この関数を抜ける
        while flug == False:
            print("引くカードを入力してください。")
            input1 = input("originals　or drawns?   o or d:   ")
            print(" ")
            if input1 == "o" and originals[drawn_player] != []:
                try:
                    input2 = int(input("インデックスを入力してください。:   "))
                    print(" ")
                    if input2 >= 0 and input2 <len(originals[drawn_player]):#originals[drawn_player][input2] != None:
                        input3 = input("それでいいですか y or n:   ")
                        print(" ")
                        if input3 == "y":
                            drawn_card = originals[drawn_player].pop(input2)
                            flug = True

                            history[turn][3] = 0
                            history[turn][4] = input2
                            history[turn][5] = drawn_card


                        else:
                            print("正しく入力してください。")
                            print(" ")
                            continue
                except ValueError:
                    print("半角で正しく入力してください。")
                    print(" ")
                    continue
            elif input1 == "d" and drawns[drawn_player] != []:
                try:
                    input2 = int(input("インデックスを入力してください。:   "))
                    print(" ")
                    if input2 >= 0 and input2 < len(drawns[drawn_player]):#drawns[drawn_player][input2] != None:
                        input3 = input("それでいいですか y or n:   ")
                        print(" ")
                        if input3 == "y":
                            drawn_card = drawns[drawn_player].pop(input2)
                            flug = True

                            history[turn][3] = 1
                            history[turn][4] = input2
                            history[turn][5] = drawn_card


                        else:
                            print("正しく入力してください。")
                            print(" ")
                            continue
                except ValueError:
                    print("半角で正しく入力してください。")
                    print(" ")
                    continue
            else:
                print("正しく入力してください。")
                print(" ")
                continue
        print("引いたのは{}{:02d}でした。".format(marks[int((drawn_card-1)/13)], drawn_card%13 if drawn_card%13 != 0 else 13))
        print(" ")
        return drawn_card

    elif turn_player in com_player_nums:  #もしターンプレイヤーがcomなら
        if com_player_pattern[turn_player] == 0:  #comのパターンが０なら、とにかくオリジナルから引く
            if originals[drawn_player] != []: #もしdrawn_playerのオリジナルがまだあるなら、ランダムで引く
                input1 = "o"
                input2 = random.randint(0, len(originals[drawn_player])-1)
                drawn_card = originals[drawn_player].pop(input2)

                history[turn][3] = 0
                history[turn][4] = input2
                history[turn][5] = drawn_card

            elif originals[drawn_player] == []:
                input1 = "d"
                input2 = random.randint(0, len(drawns[drawn_player])-1)
                drawn_card = drawns[drawn_player].pop(input2)

                history[turn][3] = 1
                history[turn][4] = input2
                history[turn][5] = drawn_card

            print("引いたのは{}{:02d}でした。".format(marks[int((drawn_card-1)/13)], drawn_card%13 if drawn_card%13 != 0 else 13))
            print(" ")
            return drawn_card

        elif com_player_pattern[turn_player] == 1:  #とにかく引き札から引く
            if drawns[drawn_player] != []:
                input1 = "d"
                input2 = random.randint(0, len(drawns[drawn_player])-1)
                drawn_card = drawns[drawn_player].pop(input2)

                history[turn][3] = 1
                history[turn][4] = input2
                history[turn][5] = drawn_card

            elif drawns[drawn_player] == []:
                input1 = "o"
                input2 = random.randint(0, len(originals[drawn_player])-1)
                drawn_card = originals[drawn_player].pop(input2)

                history[turn][3] = 0
                history[turn][4] = input2
                history[turn][5] = drawn_card

            print("引いたのは{}{:02d}でした。".format(marks[int((drawn_card-1)/13)], drawn_card%13 if drawn_card%13 != 0 else 13))
            print(" ")
            return drawn_card

        elif com_player_pattern[turn_player] == 2:   #完全ランダム
            temp_index = random.randint(0, len(originals[drawn_player])+len(drawns[drawn_player])-1)  #オリジナルと引き札を通したインデックス
            if temp_index < len(originals[drawn_player]):
                input1 = "o"
                input2 = temp_index
                drawn_card = originals[drawn_player].pop(input2)

                history[turn][3] = 0
                history[turn][4] = input2
                history[turn][5] = drawn_card

            elif temp_index >= len(originals[drawn_player]):
                input1 = "d"
                input2 = temp_index - len(originals[drawn_player])
                drawn_card = drawns[drawn_player].pop(input2)

                history[turn][3] = 1
                history[turn][4] = input2
                history[turn][5] = drawn_card

            print("引いたのは{}{:02d}でした。".format(marks[int((drawn_card-1)/13)], drawn_card%13 if drawn_card%13 != 0 else 13))
            print(" ")
            return drawn_card

        elif com_player_pattern[turn_player] == 3:  #n:m
            temp_index = random.randint(0, len(originals[drawn_player])*pattern_3_n + len(drawns[drawn_player])*pattern_3_m -1)
            if temp_index < len(originals[drawn_player])*pattern_3_n:
                input1 = "o"
                input2 = int(temp_index / pattern_3_n)
                drawn_card = originals[drawn_player].pop(input2)

                history[turn][3] = 0
                history[turn][4] = input2
                history[turn][5] = drawn_card

            elif temp_index >= len(originals[drawn_player])*pattern_3_n:
                input1 = "d"
                input2 = int((temp_index - len(originals[drawn_player])*pattern_3_n) / pattern_3_m)
                drawn_card = drawns[drawn_player].pop(input2)

                history[turn][3] = 1
                history[turn][4] = input2
                history[turn][5] = drawn_card

            print("引いたのは{}{:02d}でした。".format(marks[int((drawn_card-1)/13)], drawn_card%13 if drawn_card%13 != 0 else 13))
            print(" ")
            return drawn_card






#その人の手札と、今引いたカードが揃っているか判定。この関数の中で手札を変更する。
def judge(turn_player, drawn_card):
    drawn_card_num = drawn_card%13
    flug = False  #カードが揃ったら、Trueになる
    for i, x in enumerate(originals[turn_player]):
        if x%13 == drawn_card_num:  #もしオリジナルで揃ったら

            history[turn][9] = 0
            history[turn][10] = i

            originals[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None
            ages[x] = None #agesに揃ったことを意味するNoneを代入
            ages[drawn_card] = None
            flug = True
    for i, x in enumerate(drawns[turn_player]):
        if x%13 == drawn_card_num:  #もし引き札で揃ったら

            history[turn][9] = 1
            history[turn][10] = i

            drawns[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None
            ages[x] = None #agesに揃ったことを意味するNoneを代入
            ages[drawn_card] = None
            flug = True
    if flug == False:
        drawns[turn_player].append(drawn_card)
        places[drawn_card] = turn_player
    print("そろったかどうか＝{}".format(flug))
    print(" ")
    return flug


#カードを引くための関数。毎ターン、多くても一回呼び出される。
def draw(turn_player, drawn_player):
    drawn_card = input_card_com_exist_ver(turn_player, drawn_player)
    #judge(turn_player, drawn_card)
    #global turn
    history[turn][6] = int(judge(turn_player, drawn_card))

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








#メイン関数
turn_player_win = False #active win した人がいるかどうか
drawn_player_win = False #passive win した人がいるかどうか
loser_exist = False
#next_turn_player = 0
previous_turn_num = 0
turn_end_ok =False
#age_increase = False

#print("zizi_index = {}".format(zizi_index))   #ziziチェック用。
print(" ")
print("ゲームを開始します")
print(" ")
for k in range(46):
    print(" ")
print("初めはプレイヤー{}さんのターンです。".format(turn%4))
while turn_end_ok == False:
    input0 = input("準備はいいですか？　y or n: ")
    if input0 == "y":
        turn_end_ok = True
    else:
        turn_end_ok = False
while loser_exist == False:

    turn_player = turn%4

    history[turn][0] = turn
    history[turn][1] = turn_player

    for k in range(46):
        print(" ")
    print("turn = {}".format(turn))
    print("turn_player = {}".format(turn%4))
    print(" ")
    #print("places = {}".format(places))   #placesをプリントして、チェックする用。
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for i in range(4):
        print(" ")
        print("player_{}\'s hand".format(i))
        if i == turn%4:
            #print(" my originals={}".format(originals[i]))  #my のプリントが正しいか、チェックする用。
            #print(" my drawns={}".format(drawns[i]))
            print("                                                                      my originals = [", end = "")
            for j in range(len(originals[i])):
                print(" {}{:02d}".format(marks[int((originals[i][j]-1)/13)], originals[i][j]%13 if originals[i][j]%13 != 0 else 13), end = "")
            print("]")
            print("                                                                      my drawns = [", end = "")
            for j in range(len(drawns[i])):
                print(" {}{:02d}".format(marks[int((drawns[i][j]-1)/13)], drawns[i][j]%13 if drawns[i][j]%13 != 0 else 13), end = "")
            print("]")
        else:
            #print(" originals={}".format(originals[i])) #□の数が正しいかの、チェック用。
            #print(" drawns={}".format(drawns[i]))
            print(" originals = [", end = "")
            for j in range(len(originals[i])):
                print(" □{}".format(j), end = " ")
            print("]")
            print(" drawns = [", end = "")
            for j in range(len(drawns[i])):
                print(" □{}".format(j), end = " ")
            print("]")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print(" ")
    print(" ")
    print(" ")

    print("open source is below")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for i in range(1,14):
        print(" {0:2d} ".format(i), end = "")   #桁合わせの為に、0:2dを加えた
    print(" ")
    for i in range(0,4):
        for j in range(1,14):
            if places[j + 13 * i] == None and (j + 13 * i) != zizi_index:  #ziziもNoneなので、注意。
                print("  {} ".format(marks[i]), end = "")
            else:
                print("    ", end = "")
        print(" ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(" ")
    print(" ")
    print(" ")


    if turn >= 5:
        print("前回の自分のターン以降の履歴を表示します")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for i in range(turn-4, turn):
            if history[i][2] != None:   #飛ばされたターンについては表示しない
                print("turn{:02d}はプレイヤー{}さんが、プレイヤー{}さんの".format(history[i][0], history[i][1], history[i][2]), end = "")
                if history[i][3] == 0:
                    print("オリジナルの", end = "")
                elif history[i][3] == 1:
                    print("  引き札の　", end = "")
                #print("インデックス{}から{:02d}を引き,".format(history[i][4], history[i][5]), end = "")
                print("インデックス{}から ".format(history[i][4]), end = "")
                if i == turn-4:
                    print("{}{:02d}を引き、".format(marks[int((history[i][5]-1)/13)], history[i][5]%13 if history[i][5]%13 != 0 else 13), end ="")
                else:
                    print("● ●を引き、", end = "")
                if history[i][6] == 0:
                    print("そろいませんでした。", end = "")
                elif history[i][6] == 1:
                    print("{}インデックス{:02d}とそろいました。".format("オリジナルの" if history[i][9] == 0 else "引き札の", history[i][10]), end = "")
                if history[i][7] == 1:
                    print("引かれたプレイヤーが上がりました。", end = "")
                if history[i][8] == 1:
                    print("ターンプレイヤーが上がりました。", end = "")
            print(" ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(" ")
    elif turn < 5 and turn > 1:
        print("ゲーム開始からこれまでの履歴を表示します")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for i in range(1, turn):
            if history[i][2] != None:   #飛ばされたターンについては表示しない
                print("turn{:02d}はプレイヤー{}さんが、プレイヤー{}さんの".format(history[i][0], history[i][1], history[i][2]), end = "")
                if history[i][3] == 0:
                    print("オリジナルの", end = "")
                elif history[i][3] == 1:
                    print("  引き札の  ", end = "")
                #print("インデックス{}から{:02d}を引き,".format(history[i][4], history[i][5]), end = "")
                print("インデックス{}から ".format(history[i][4]), end = "")
                #print("{}{:02d}を引き、".format(marks[int((history[i][5]-1)/13)], history[i][5]%13 if history[i][5]%13 != 0 else 13), end ="")  #何を引いたか、チェックする用。
                print("● ●を引き、", end = "")
                if history[i][6] == 0:
                    print("そろいませんでした。", end = "")
                elif history[i][6] == 1:
                    print("{}インデックス{:02d}とそろいました。".format("オリジナルの" if history[i][9] == 0 else "引き札の", history[i][10]), end = "")
                if history[i][7] == 1:
                    print("引かれたプレイヤーが上がりました。", end = "")
                if history[i][8] == 1:
                    print("ターンプレイヤーが上がりました。", end = "")
            print(" ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(" ")
    elif turn == 1:
        pass
    print(" ")
    print(" ")
    print(" ")


    if turn_player_win == True:  #もし、先のターンの人が上がったら、次に順番が回ってくる人は、何もしない。
        turn_player_win = False

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
                    print("正しく入力してください。")


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
        drawn_player = turn%4  #drawn_playerの初期化
        for cnt in range(1,4):
            if originals[(turn - cnt)%4] != [] or drawns[(turn - cnt)%4] != []:
                drawn_player = (turn -cnt)%4
                break
        history[turn][2] = drawn_player

        draw(turn_player, drawn_player)

        print("ここでもう一度皆さんの手札を表示します。")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for i in range(4):
            print(" ")
            print("player_{}\'s hand".format(i))
            if i == turn%4:
                #print(" my originals={}".format(originals[i]))  #my のプリントが正しいか、チェックする用。
                #print(" my drawns={}".format(drawns[i]))
                print("                                                                      my originals = [", end = "")
                for j in range(len(originals[i])):
                    print(" {}{:02d}".format(marks[int((originals[i][j]-1)/13)], originals[i][j]%13 if originals[i][j]%13 != 0 else 13), end = "")
                print("]")
                print("                                                                      my drawns = [", end = "")
                for j in range(len(drawns[i])):
                    print(" {}{:02d}".format(marks[int((drawns[i][j]-1)/13)], drawns[i][j]%13 if drawns[i][j]%13 != 0 else 13), end = "")
                print("]")
            else:
                #print(" originals={}".format(originals[i])) #□の数が正しいかの、チェック用。
                #print(" drawns={}".format(drawns[i]))
                print(" originals = [", end = "")
                for j in range(len(originals[i])):
                    print(" □{}".format(j), end = " ")
                print("]")
                print(" drawns = [", end = "")
                for j in range(len(drawns[i])):
                    print(" □{}".format(j), end = " ")
                print("]")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(" ")
        print(" ")


        if originals[drawn_player] == [] and drawns[drawn_player] == []:  #もし、引かれた人の手札が空になったら、その人は上がり。
            drawn_player_win == True
            orders.append(drawn_player)
            print("プレイヤー{}さんが上がりました".format(drawn_player))
            print(" ")
            history[turn][7] = 1
        if originals[turn_player] == [] and drawns[turn_player] == []:   #もし、引いた人の手札が空になったら、その人は上がり。
            turn_player_win = True
            orders.append(turn_player)
            print("プレイヤー{}さんが上がりました".format(turn_player))
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


        previous_turn_num = turn
        history_of_places[turn] = places[:]
        history_of_ages[turn] = ages[:]         #このターンの履歴を記入。

        """for turnnnnnnn in range(0, turn+1):   #history_of_配列にちゃんと代入できているかチェック用。
            print("turn =              {}".format(turnnnnnnn))
            #print("places =            {}".format(places))
            print("history_of_places = {}".format(history_of_places[turnnnnnnn]))
        print(" ")
        for turnnnnnnn in range(0, turn+1):   #history_of_配列にちゃんと代入できているかチェック用。
            print("turn =              {}".format(turnnnnnnn))
            #print("ages =              {}".format(ages))
            print("history_of_ages =   {}".format(history_of_ages[turnnnnnnn]))"""

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
    for k in range(70):
        print(" ")
    turn_end_ok = False
    while turn_end_ok == False and loser_exist == False:
        if turn%4 in com_player_nums:
            turn_end_ok = True
        else:
            print("次はプレイヤー{}さんのターンです。".format(turn%4))
            input_ok = input("プレイヤー交代しましたか？ y or n: ")
            if input_ok == "y":
                turn_end_ok = True
            elif input_ok == "quit":
                turn_end_ok = True
                loser_exist = True  #ゲーム終了後の動作チェック用。
            else:
                turn_end_ok = False


    #ターンの最後


print(" ")
print("ゲーム終了")
print(" ")
if zizi_index %13 == 0:
    zizi_num = 13
else:
    zizi_num = zizi_index%13
print("ziziは{}{:02d}でした。".format(marks[int((zizi_index-1)/13)], zizi_num))
print(" ")
print("順位は")
for i in range(len(orders)):
    print("{}位がプレイヤー{}さんでした。".format(i+1, orders[i]))
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
            print("{}インデックス{:02d}とそろいました。".format("オリジナルの" if history[i][9] == 0 else "引き札の", history[i][10]), end = "")
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
