from konlpy.tag import Mecab, Okt, Komoran, Hannanum, Kkma
from khaiii_pos.khaiii_pos import Khaiii
import json


tokenizers = {
    'Mecab':Mecab(),
    'Okt':Okt(),
    'Komoran':Komoran(),
    'Hannanum':Hannanum(),
    'Kkma':Kkma(),
    'Khaiii':Khaiii()
}

corpus_fname = 'raw/korquad/KorQuAD_v1.0_train.json'

with open(corpus_fname) as f_corpus:
    dataset_json = json.load(f_corpus)
    dataset = dataset_json['data']

    for i, article in enumerate(dataset):
        # w_lines = []
        if i > 10 :
            break

        for paragraph in article['paragraphs']:
            print('--------------------------------------')
            print('[ORIGINAL] ', paragraph['context'])

            for key, tokenizer in  tokenizers.items():
                print('[%8s] %s' % (key, tokenizer.pos(paragraph['context'])))
