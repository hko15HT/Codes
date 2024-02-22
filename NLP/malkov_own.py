import random
import MeCab
import re
import readchar

def format(): # テキストファイルを整形して学習データを作成
    # txtファイルを開く
    with open(r"markov\sample.txt", "r", encoding="utf-8") as f:
        content = f.read().replace("\n", "")
        print(content)
        # 句読点(。)で区切る(。は含む)
        scripts = re.split("(?<=。)", content)
        
    return scripts


def model_init(): # 学習データからモデルを作成

    # それぞれの単語の二次元マルコフ辞書
    malkov_dict = {} # {"私":{"は":1.0}, "は":{"カレー":1.0}, "カレー":{"が":1.0}, "が":{"好き":1.0}, "好き":{"。":1.0}}

    sentences_ordinary = format() # ["私はカレーが好き。", "私は焼き肉が好き。"]

    # 除外文字
    ignore_chars = ["「", "」", "'", '"', " ", "(", ")", "（", "）", "[", "]", "※", "\n", " ", "　"]

    # MeCabの初期化(分かち書き)
    mecab = MeCab.Tagger("-Owakati")

    # 学習データの単語への分解
    for sentence in sentences_ordinary:

        # 一文字ずつのリスト
        uni_words = [] # ["私", "は", "カレー", "が", "好き", "。"]

        for word in mecab.parse(sentence).split():
            if not word in ignore_chars:
                uni_words.append(word) # "私"

        #n-gramの作成
        ngram = 2
        words =[]

        # n個ずつリストに格納
        for i in range(len(uni_words)//ngram):
            word = ""
            for j in range(ngram):
                    word += uni_words[i*ngram+j]
            words.append(word)

        # 単語が奇数だと最後の文字が入らないため
        lost_word = ""
        for i in range(len(uni_words)%ngram, 0, -1):
            lost_word += uni_words[len(uni_words)%ngram*-1]
        words.append(lost_word)


        # マルコフ辞書の作成

        # 最初の単語
        if not "first" in malkov_dict:
            malkov_dict["first"] = {} # {"first":{}}

        if len(words) > 0:
            if not words[0] == "":
                if not words[0] in malkov_dict["first"]:
                    malkov_dict["first"][words[0]] = 1 # {"first":{"私":1 ←出現回数}}
                else:
                    malkov_dict["first"][words[0]] += 1 # {"first":{"私":2}}

        # それ以降の単語
        for i in range(len(words)-1):
            # 一次単語が存在しなかった場合追加
            if not words[i] in malkov_dict:
                malkov_dict[words[i]] = {} # {"私":{}}
            # 二次単語が存在しなかった場合追加
            if not words[i+1] in malkov_dict[words[i]]:
                malkov_dict[words[i]][words[i+1]] = 1 # {"私":{"は":1 ←出現回数}}
            else:
                malkov_dict[words[i]][words[i+1]] += 1 # {"私":{"は":2}}

    # print(malkov_dict)
    return(malkov_dict)


def generate_sentence(): # マルコフ辞書をもとに文を生成

    global malkov_dict, seed

    try:
        malkov_dict= malkov_dict
    except Exception as e:
        print(e)
        # マルコフ辞書の取得
        malkov_dict = model_init()

    seed = [] # 生成された分のシード値

    output = ""
    # 確率変数にのっとって最初の語を取得
    first_word = random.choices(list(malkov_dict["first"].keys()), k=1, weights=list(malkov_dict["first"].values()))[0]
    n = first_word
    seed.append(n)
    output += n

    # 連鎖的に語を取得
    while not "。" in n:
        n = random.choices(list(malkov_dict[n].keys()), k=1, weights=list(malkov_dict[n].values()))[0]
        seed.append(n)
        output += n

    # 出力
    print(output)

def train():

    global malkov_dict

    assess = int(readchar.readchar())/2 # 1->0.5, 2->1, 3->1.5

    malkov_dict["first"][seed[0]] *= assess

    for i in range(len(seed)-1):
        malkov_dict[seed[i]][seed[i+1]] *= assess
        print(malkov_dict[seed[i]][seed[i+1]], end=" ")

    print("\n" , assess)

if __name__ == "__main__":
    malkov_dict = model_init()
    while True:
        generate_sentence()
        print(seed)
        train()