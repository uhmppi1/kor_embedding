import khaiii

api = khaiii.KhaiiiApi()
api.open()

class Khaiii():
    def pos(self, phrase, flatten=True, join=False):
        """POS tagger.

        :param flatten: If False, preserves eojeols.
        :param join: If True, returns joined sets of morph and tag.

        """
        sentences = phrase.split('\n')
        morphemes = []
        if not sentences:
            return morphemes

        for sentence in sentences:
            for word in api.analyze(sentence):
                result = [(m.lex, m.tag) for m in word.morphs]
                if join:
                    result = ['{}/{}'.format(m.lex, m.tag) for m in word.morphs]

                morphemes.append(result)

        if flatten:
            return sum(morphemes, [])

        return morphemes

'''k = Khaiii()
sentence = '아버지가 방에 들어가신다.'
result = k.pos(sentence)
print(result)'''