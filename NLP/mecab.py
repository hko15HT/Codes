import MeCab #MeCabのインポート

splitter = MeCab.Tagger()
result = splitter.parse("探究論文は楽しいな") #品詞分解処理

print(result) #結果の出力

#出力結果
"""
探究　　タンキュー　　　タンキュウ　　　探究　　　名詞-普通名詞-サ変可能
論文　　ロンブン　　　　ロンブン　　　　論文　　　名詞-普通名詞-一般
は　　　ワ　　　　　　　ハ　　　　　　　は　　　　助詞-係助詞
楽しい　タノシー　　　　タノシイ　　　　楽しい　　形容詞-一般　形容詞  終止形-一般
な　　　ナ　　　　　　　ナ　　　　　　　な　　　　助詞-終助詞
EOS
"""
