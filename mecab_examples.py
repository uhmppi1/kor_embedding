from konlpy.tag import Mecab, Okt, Komoran, Hannanum, Kkma
from khaiii_pos.khaiii_pos import Khaiii
import json

tokenizer = Mecab()
tokens = tokenizer.morphs("아버지가방에들어가신다.")
print(tokens)

poses = tokenizer.pos("아버지가방에들어가신다.")
print(poses)

tokens = tokenizer.morphs("가우스전자 텔레비전 정말 좋네요.")
print(tokens)