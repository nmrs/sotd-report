import re
from functools import cached_property
from pprint import pprint
import pickle

from sotd_collator.tts_scraper import TtsScraper
import pandas as pd
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer


def cosim(X, Y):
    return 1 - cosine(X[0].toarray(), Y[0].toarray())


class SoapAlternateNamer(object):

    COSIM_FILE = '/tmp/san_tmp.pickle'
    MIN_COSIM = 0.8
    TOKEN_STOP_WORDS = [
        'and',
        '&',
        '/',
        'x',
    ]

    @cached_property
    def tts_soaps(self):
        return [x.lower() for x in TtsScraper.get_tts_soaps()]

    def _get_tts_subset_match(self, soap):
        # remove punctuation etc
        soap = re.sub(r'[^\w\s]', '', soap)
        soap_tokens = set([x for x in soap.lower().split() if x not in self.TOKEN_STOP_WORDS])
        for tts_soap in self.tts_soaps:
            tts_tokens = set([x for x in re.sub(r'[^\w\s]', '', tts_soap).lower().split() if x not in self.TOKEN_STOP_WORDS])
            if soap_tokens.issubset(tts_tokens):
                return tts_soap

    @cached_property
    def lookups(self):
        with open(self.COSIM_FILE, 'rb') as fin:
            return pickle.load(fin)

    def _get_cosim_subset_match(self, soap):
        soap = re.sub(r'[^\w\s]', '', soap)
        soap_tokens = set([x for x in soap.lower().split() if x not in self.TOKEN_STOP_WORDS])
        for user_soap, tts_soap in self.lookups.items():
            user_soap = re.sub(r'[^\w\s]', '', user_soap)
            user_tokens = set([x for x in user_soap.lower().split() if x not in self.TOKEN_STOP_WORDS])
            if soap_tokens.issubset(user_tokens):
                return tts_soap

    def prime_lookups(self, soaps):
        # get the distinct set of soaps for this month which are not exact matches with TTS
        # then build TF IDF
        soaps = [
            x.lower() for x in soaps if x and x.lower() not in self.tts_soaps
        ]
        # remove soaps that are subset matches of tts
        soaps = [
            x for x in soaps if not self._get_tts_subset_match(x)
        ]
        print('num soaps to cosim: {0}'.format(len(soaps)))
        pprint(sorted(soaps))
        corpus = list(set(self.tts_soaps + soaps))

        # create the transform -
        # hits 64, misses 151 with char ngram_range=(1,3)
        # hits 72, misses 142 with char ngram_range=(2,2) -- but false positives
        # hits 57, misses 158 with char ngram_range=(2,3)
        # hits 66, misses 149 with char_wb ngram_range=(2,3) <---
        # hits 58, misses 157 with char_wb ngram_range=(2,4)
        # hits 71, misses 145 with char_wb ngram_range=(1,3) - but false positives
        # hits 30, misses 186 with word
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2,3))
        # tokenize and build vocab
        vectorizer.fit(corpus)

        user_pre = [[x, 'user'] for x in soaps]
        tts_pre = [[x, 'tts'] for x in self.tts_soaps]
        df = pd.DataFrame(data=user_pre + tts_pre, columns=['soap', 'source'])

        def _get_tfidf(row):
            return vectorizer.transform([row['soap']])

        df.loc[:, 'idf'] = df.apply(_get_tfidf, axis=1)

        df_tts = df[df['source'] == 'tts'].drop('source', axis=1)
        df_user = df[df['source'] == 'user'].drop('source', axis=1)

        # add a column to allow a cartesian join
        df_tts.loc[:, 'key'] = 0
        df_user.loc[:, 'key'] = 0

        # rename tts columns so we can diffferentiate them post join
        df_tts.columns = ['tts_soap', 'tts_idf', 'key']

        df_cart = df_tts.merge(
            df_user,
            how='outer',
            on='key',
        )

        df_cart.loc[:, 'cosim'] = df_cart.apply(lambda x: cosim(x['idf'], x['tts_idf']), axis=1)
        df_cart = df_cart[df_cart['cosim'] > self.MIN_COSIM]

        # get best matches
        df_best = df_cart[['soap', 'cosim']].groupby('soap').max().reset_index()

        df_cart = pd.merge(
            left=df_cart,
            right=df_best,
            how='inner',
            on=['soap', 'cosim']
        )

        mapper = {
            x[0]: x[1] for x in df_cart[['soap', 'tts_soap']].to_dict('split')['data']
        }

        print('number of hits: {0}'.format(len(mapper)))

        with open(self.COSIM_FILE, 'wb') as fout:
            pickle.dump(mapper, fout)

    def get_principal_name(self, name):
        if not name:
            return None

        name = name.lower()
        if name in self.tts_soaps:
            return name.title()

        # fall down to token match on TTS soaps
        tts_subset_match = self._get_tts_subset_match(name)
        if tts_subset_match:
            return tts_subset_match.title()

        # fall down to pregenerated TFIDF cosim matches
        if name in self.lookups:
            return self.lookups[name].title()

        # fall down to token match on TFIDF cosim matches
        cosim_subset_match = self._get_cosim_subset_match(name)
        if cosim_subset_match:
            return cosim_subset_match.title()

        print('No match found for {0}'.format(name))
        return None









if __name__ == '__main__':
    srn = SoapAlternateNamer()

    print(srn.tts_soaps)