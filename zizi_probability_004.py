import random


As_originals = []

Bs_originals = []

Cs_originals = []

Ds_originals = []

#これらを配列に入れておく
originals = [As_originals, Bs_originals, Cs_originals, Ds_originals]

#シャッフル前のそれぞれのカードのありか
places_begin = [None] + [None, 1,2,3] + list(range(0,4)) * 12

marks = ["S", "H", "C", "D"]

#今回の実験で、ziziがblank出身だった場合に、加算されていく。
cnt = 0

#blankの数字が何個あるか。
blank_size = 0

#blank_sizeの和を取る。
blank_size_sum = 0

#今回の実験で、手札が配られた時に何個揃っていないカードがあるか。
blanklike_cards_size = 0

#全試行でblanklike_cards_sizeの和を取る
blanklike_cards_size_sum = 0



#blankを入れる配列
blanks = []

#blankの個数が0,1,2,,,,13個の時に、その中にziziがいる回数を代入する配列。ただし、第一項のみ、blanksに入ってなかった回数。
blanks_cnts = [0] * 14

#blanksが[]の時に、カウント
blanks_is_zero_cnt = 0

#試行回数
size = 100000

#実験のメイン関数
for i in range(20):
    print(" ")
print("実験を始めます。")

for main_i in range(size):

    #初期化
    originals[0] = []
    originals[1] = []
    originals[2] = []
    originals[3] = []
    blanks = []
    blank_size = 0
    blanklike_cards_size = 0

    #カードの場所をシャッフルして、それぞれのカードがどこにあるかを書いておく配列を初期化
    places = [None] + random.sample(places_begin[1:53], 52)   #random.sampleで指定した範囲の中の要素をシャッフルした新たな配列を作れる

    #この配列の２つ目のNoneがziziのインテックスがziziのカードのインデックス
    zizi_index = 1 + places[1:53].index(None)

    zizi_num = 0

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

    #一応、open_sourceと手札を表示する
    if main_i < 5: #初めの5回分は表示する。
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("試行第{}回".format(main_i+1))
        print(" ")
        print("hands are below")
        for i in range(4):
            print("player_{}\'s hand".format(i))
            print(" originals = {}".format(originals[i]))
        print(" ")
        print("open source is below")
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
        print(" ")
        print("zizi = {}".format(zizi_index))
        print("zizi_num = {}".format(zizi_index%13 if zizi_index%13 != 0 else 13))
        print(" ")

    #ここで、open_sourceのなかで、blankになっている数字を配列blanksに入れる。
    for i in range(1,14):
        blank_exist = True
        for j in range(0,4):
            if places[i + j * 13] == None and i+j*13 != zizi_index: #ziziとしてではなく、揃って捨てられている場合、blankではない。
                blank_exist = False
            if places[i + j * 13] != None or i + j * 13 == zizi_index:  #誰かの手札に入っているか、ziziなら。
                blanklike_cards_size += 1
        if blank_exist == True:
            blanks.append(i)

    blank_size = len(blanks)
    blank_size_sum += blank_size
    blanklike_cards_size_sum += blanklike_cards_size


    if main_i < 5:
        print("blanks = {}".format(blanks))
        print("blanklike_cards_size = {}".format(blanklike_cards_size))
        print("blank_size = {}".format(blank_size))

    #ziziの数字がblanksに入っているかどうか。入っていたら、cnt+1
    if zizi_index%13 == 0:
        zizi_num = 13
    else:
        zizi_num = zizi_index%13
    if zizi_num in blanks:
        cnt += 1
        blanks_cnts[len(blanks)] += 1
    else:
        blanks_cnts[0] += 1
    if blanks == []:
        blanks_is_zero_cnt += 1
    if main_i < 5:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print(" ")
print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
print("                                                                   試行全{}回のうち、ziziがblanksにあったのは、{}回でした。".format(size, cnt))
print("                                                                   そろっていなかったカードは、平均して、毎回{}枚ありました。".format(blanklike_cards_size_sum/size))
print("                                                                   blankの数字の個数は、平均して、毎回{}個ありました。".format(blank_size_sum/size))
print("                                                                   blanks_cnts(blanksがいくつあった時に、そこにziziが入っていた回数) = {}".format(blanks_cnts))
print("                                                                   blanks_is_zero_cnt(blanksがなかった時の回数) = {}".format(blanks_is_zero_cnt))
print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
for i in range(20):
    print(" ")
