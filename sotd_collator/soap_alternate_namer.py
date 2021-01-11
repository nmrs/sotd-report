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

    @cached_property
    def tts_soaps(self):
        return [x.lower() for x in TtsScraper.get_tts_soaps()]

    def _get_tts_subset_match(self, soap):
        soap_tokens = set(soap.lower().split())
        for tts_soap in self.tts_soaps:
            tts_tokens = set(tts_soap.lower().split())
            if soap_tokens.issubset(tts_tokens):
                return tts_soap

    @cached_property
    def lookups(self):
        with open(self.COSIM_FILE, 'rb') as fin:
            return pickle.load(fin)

    def _get_cosim_subset_match(self, soap):
        soap_tokens = set(soap.lower().split())
        for user_soap in self.lookups:
            user_tokens = set(user_soap.lower().split())
            if soap_tokens.issubset(user_tokens):
                return user_soap

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
        corpus = list(set(self.tts_soaps + soaps))

        # create the transform
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
        df_tts.loc[:, 'key'] = 0
        df_user.loc[:, 'key'] = 0

        df_tts.columns = ['tts_soap', 'tts_idf', 'key']

        df_cart = df_tts.merge(
            df_user,
            how='outer',
            on='key',
        )

        df_cart.loc[:, 'cosim'] = df_cart.apply(lambda x: cosim(x['idf'], x['tts_idf']), axis=1)
        df_cart = df_cart[df_cart['cosim'] > 0.7]

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

        pprint(mapper)
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
            return tts_subset_match

        # fall down to pregenerated TFIDF cosim matches
        if name in self.lookups:
            return self.lookups[name].title()

        # fall down to token match on TFIDF cosim matches
        cosim_subset_match = self._get_cosim_subset_match(name)
        if cosim_subset_match:
            return cosim_subset_match

        print('No match found for {0}'.format(name))
        return None









if __name__ == '__main__':
    srn = SoapAlternateNamer()

    print(srn.tts_soaps)