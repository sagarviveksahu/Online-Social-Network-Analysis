from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pickle
import re
import json

def download_afin():

    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    file = ZipFile(BytesIO(url.read()))
    afin_f = file.open('AFINN/AFINN-111.txt')
    return afin_f

def read_data(file):

    afinn = {}
    for l in file:
        line = l.strip().split()
        if len(line) == 2:
            afinn[line[0].decode("utf-8")] = int(line[1])
    print('read %d AFINN terms.\nE.g.: %s' % (len(afinn),
                                          str(list(afinn.items())[:10])))
    return afinn


def afinn_sentiment2(terms, afinn, verbose=False):

    pos = 0
    neg = 0
    for t in terms:
        if t in afinn:
            if afinn[t] > 0:
                pos += afinn[t]
            else:
                neg += -1 * afinn[t]
    return pos, neg

def tokenize(text):

    tok = re.sub('\W+', ' ', text.lower()).split()
    return tok

def token_features(tokens, feats):

    c = Counter(tokens)
    for i in tokens:
        feats.update({"token="+i:c[i]})

def token_pair_features(tokens, feats, k=3):

    c = Counter()
    for i in range(len(tokens)-k+1):
        c.update(list(combinations(tokens[i:i + k], 2)))
    for j in sorted(c):
        feats["token_pair=" + j[0] + "__" + j[1]] = c[j]


def lexicon_features(tokens, feats):

    feats.update({'pos_words':0})
    feats.update({'neg_words':0})
    for i in tokens:
        if i.lower() in pos_words:
            feats.update({'pos_words':feats["pos_words"] + 1})
        elif i.lower() in neg_words:
            feats.update({'neg_words':feats["neg_words"] + 1})

def featurize(tokens, feature_fns):

    feats = defaultdict(lambda:0)
    for i in feature_fns:
        i(tokens, feats)
    return sorted(feats.items())

def pos_neg(tweets,tokens,afin):

    pstv, ngtv, mx = [],[],[]
    for tks, twt in zip(tokens, tweets):
        pos, neg = afinn_sentiment2(tks, afin)
        if neg > pos:
            ngtv.append((twt['text'], pos, neg))
        elif pos > neg:
            pstv.append((twt['text'], pos, neg))
        elif neg == pos:
            mx.append((twt['text'], pos, neg))
    return pstv, ngtv, mx

def main():

    tweets = json.load(open("tweets.txt"))
    afin = download_afin()
    read = read_data(afin)
    tokens = []
    for t in tweets:
        tokens.append(tokenize(t['text']))
    positives, negatives, mixed = pos_neg(tweets,tokens,read)
    print(len(positives),len(negatives),len(mixed))
    f = open("sentiments.txt","a")
    f.truncate(0)
    json.dump((positives,negatives,mixed),f)

if __name__ == '__main__':
    main()
