from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
from soyspacing.countbase import CountSpace
import math


corpus_fname = './cleaned_data/namuwiki/namuwiki_20190312.txt'
model_fname = 'soynlp/soyword.model'

def train_space_model(corpus_fname, model_fname):
    model = CountSpace()
    model.train(corpus_fname)
    model.save_model(model_fname, json_format=False)


def soy_tokenize(model_fname, input_sentence):
    word_extractor = WordExtractor(min_frequency=100,
                                   min_cohesion_forward=0.05,
                                   min_right_branching_entropy=0.0
                                   )
    word_extractor.load(model_fname)
    scores = word_extractor.word_scores()
    # https://github.com/lovit/soynlp/blob/master/tutorials/wordextractor_lecture.ipynb
    # (1) 주어진 글자가 유기적으로 연결되어 함께 자주 나타나고,
    # (2) 그 단어의 우측에 다양한 조사, 어미, 혹은 다른 단어가 등장하여 단어의 우측의 branching entropy가 높다
    scores = {key:(scores[key].cohesion_forward * math.exp(scores[key].right_branching_entropy)) for key in scores.keys()}
    tokenizer = LTokenizer(scores=scores)
    tokens = tokenizer.tokenize(input_sentence)
    tokenized_sent = ' '.join(tokens)

    return tokenized_sent



# train_space_model(corpus_fname, model_fname)
soy_tokenize(model_fname, '애비는 종이었다.')