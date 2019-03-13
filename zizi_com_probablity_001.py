import random

#試行回数
size = 1000

#それぞれのプレイヤーの勝利回数。大きい方の配列のインデックスがプレイヤー番号、その中身がそれぞれの順位だった回数
com_player_wins = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]





players = [0,1,2,3]   #A,B,C,D
"""
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
drawns = [As_drawns, Bs_drawns, Cs_drawns, Ds_drawns]"""

marks = ["S", "H", "C", "D"]



com_player_nums = [0,1,2,3]  #毎回このファイルを実行するときに、comのプレイヤーが何番か記入すること。
com_player_pattern = [0,1,2,3 ]  #com_player_numsになってるインデックスに、そのcomのパターンを記入すること。
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
"""
turn = 1
zizi_index = 0
zizi_num = 0
orders = []   #１位から４位までの人を順に代入。


#シャッフル前のそれぞれのカードのありか
places_begin = [None] + [None, 1,2,3] + list(range(0,4)) * 12

#カードの場所をシャッフルして、それぞれのカードがどこにあるかを書いておく配列を初期化
places = [None] + random.sample(places_begin[1:53], 52)   #random.sampleで指定した範囲の中の要素をシャッフルした新たな配列を作れる

#この配列の２つ目のNoneがziziのインテックスがziziのカードのインデックス
zizi_index = 1 + places[1:53].index(None)



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
    random.shuffle(originals[i])"""



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



            elif originals[drawn_player] == []:
                input1 = "d"
                input2 = random.randint(0, len(drawns[drawn_player])-1)
                drawn_card = drawns[drawn_player].pop(input2)


            return drawn_card

        elif com_player_pattern[turn_player] == 1:  #とにかく引き札から引く
            if drawns[drawn_player] != []:
                input1 = "d"
                input2 = random.randint(0, len(drawns[drawn_player])-1)
                drawn_card = drawns[drawn_player].pop(input2)


            elif drawns[drawn_player] == []:
                input1 = "o"
                input2 = random.randint(0, len(originals[drawn_player])-1)
                drawn_card = originals[drawn_player].pop(input2)


            return drawn_card

        elif com_player_pattern[turn_player] == 2:   #完全ランダム
            temp_index = random.randint(0, len(originals[drawn_player])+len(drawns[drawn_player])-1)  #オリジナルと引き札を通したインデックス
            if temp_index < len(originals[drawn_player]):
                input1 = "o"
                input2 = temp_index
                drawn_card = originals[drawn_player].pop(input2)


            elif temp_index >= len(originals[drawn_player]):
                input1 = "d"
                input2 = temp_index - len(originals[drawn_player])
                drawn_card = drawns[drawn_player].pop(input2)


            return drawn_card

        elif com_player_pattern[turn_player] == 3:  #n:m
            temp_index = random.randint(0, len(originals[drawn_player])*pattern_3_n + len(drawns[drawn_player])*pattern_3_m -1)
            if temp_index < len(originals[drawn_player])*pattern_3_n:
                input1 = "o"
                input2 = int(temp_index / pattern_3_n)
                drawn_card = originals[drawn_player].pop(input2)


            elif temp_index >= len(originals[drawn_player])*pattern_3_n:
                input1 = "d"
                input2 = int((temp_index - len(originals[drawn_player])*pattern_3_n) / pattern_3_m)
                drawn_card = drawns[drawn_player].pop(input2)



            return drawn_card

#その人の手札と、今引いたカードが揃っているか判定。この関数の中で手札を変更する。
def judge(turn_player, drawn_card):
    drawn_card_num = drawn_card%13
    flug = False  #カードが揃ったら、Trueになる
    for i, x in enumerate(originals[turn_player]):
        if x%13 == drawn_card_num:  #もしオリジナルで揃ったら



            originals[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None

            flug = True
    for i, x in enumerate(drawns[turn_player]):
        if x%13 == drawn_card_num:  #もし引き札で揃ったら



            drawns[turn_player].pop(i)
            places[x] = None #placesに揃ったことを意味するNoneを代入
            places[drawn_card] = None

            flug = True
    if flug == False:
        drawns[turn_player].append(drawn_card)
        places[drawn_card] = turn_player

    return flug

#カードを引くための関数。毎ターン、多くても一回呼び出される。
def draw(turn_player, drawn_player):
    drawn_card = input_card_com_exist_ver(turn_player, drawn_player)
    #judge(turn_player, drawn_card)
    #global turn
    judge(turn_player, drawn_card)
    return drawn_card













#実験のメイン関数
for i in range(20):
    print(" ")
print("実験を始めます。")

for main_i in range(size):

    #初期化

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


    turn = 1
    zizi_index = 0
    zizi_num = 0
    orders = []   #１位から４位までの人を順に代入。



    #シャッフル前のそれぞれのカードのありか
    places_begin = [None] + [None, 1,2,3] + list(range(0,4)) * 12

    #カードの場所をシャッフルして、それぞれのカードがどこにあるかを書いておく配列を初期化
    places = [None] + random.sample(places_begin[1:53], 52)   #random.sampleで指定した範囲の中の要素をシャッフルした新たな配列を作れる

    #この配列の２つ目のNoneがziziのインテックスがziziのカードのインデックス
    zizi_index = 1 + places[1:53].index(None)



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






    #メイン関数
    turn_player_win = False #active win した人がいるかどうか
    drawn_player_win = False #passive win した人がいるかどうか
    loser_exist = False
    drawn_card = 0


    while loser_exist == False:

        turn_player = turn%4


        if main_i <5:
            print(" ")
            print("turn = {}".format(turn))
            print("turn_player = {}".format(turn%4))
            print(" ")
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



        if turn_player_win == True:  #もし、先のターンの人が上がったら、次に順番が回ってくる人は、何もしない。
            turn_player_win = False


            for cnt in range(1,4):   #次のターンの人を探して、ターンをあげるだけ。
                if originals[(turn + cnt)%4] != [] or drawns[(turn + cnt)%4] != []:
                    loser_exist = False
                    turn = turn + cnt
                    break
                if cnt == 3 and originals[(turn + cnt)%4] == [] and drawns[(turn + cnt)%4] == []:
                    loser_exist = True
                    orders.append(turn_player)

                    break

        else:   #もし、先のターンの人が上がってなかったら、次に順番が回ってきた人は、先のターンの人から一枚引き抜き、
            drawn_player = turn%4  #drawn_playerの初期化
            for cnt in range(1,4):
                if originals[(turn - cnt)%4] != [] or drawns[(turn - cnt)%4] != []:
                    drawn_player = (turn -cnt)%4
                    break


            drawn_card = draw(turn_player, drawn_player)

            if main_i<5:
                print("引いたのは{}{:02d}でした。".format(marks[int((drawn_card-1)/13)], drawn_card%13 if drawn_card%13 != 0 else 13))
                print(" ")



            if originals[drawn_player] == [] and drawns[drawn_player] == []:  #もし、引かれた人の手札が空になったら、その人は上がり。
                drawn_player_win == True
                orders.append(drawn_player)

            if originals[turn_player] == [] and drawns[turn_player] == []:   #もし、引いた人の手札が空になったら、その人は上がり。
                turn_player_win = True
                orders.append(turn_player)


            for cnt in range(1,4):   #続いて、次のターンの人を探す処理をする。
                if originals[(turn + cnt)%4] != [] or drawns[(turn + cnt)%4] != []:
                    loser_exist = False
                    turn = turn + cnt

                    break
                if cnt == 3 and originals[(turn + cnt)%4] == [] and drawns[(turn + cnt)%4] == []:  #三人目まで調べてみて
                    loser_exist = True   #もし、自分以外のみんなの手札が空の場合、その人の負けが確定する。
                    orders.append(turn_player)

                    break

        #ターンの最後


    for i, x in enumerate(orders):
        com_player_wins[x][i] += 1

    if main_i < 5:
        print("orders = {}".format(orders))
        print("第{}回目の試行を終わります".format(main_i+1))
        for i in range(20):
            print(" ")






    #main_iの最後



print("実験終了")


print("com_player_wins = {}".format(com_player_wins))

print("全{}回の試行の結果、以下のようになりました。".format(size))

for i in range(4):
    print("com_player{}はパターン{}で、１位 {} 回、２位 {} 回、３位 {} 回、 ４位 {} 回 ".format(i, com_player_pattern[i], com_player_wins[i][0], \
com_player_wins[i][1], com_player_wins[i][2], com_player_wins[i][3]))
