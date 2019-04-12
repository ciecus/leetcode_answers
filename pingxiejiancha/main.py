from __future__ import division
from collections import Counter
from tqdm import tqdm
import re
import string
import math as calc
import numpy as np
import os
import ast
from config import Config

class correct():
    def __init__(self, corpus, vocab, addconfusion, subconfusion, transconfusion,delconfusion,
               bigram_dic, trigram_dic, sentence,wrongnum):
        self.corpus = corpus
        self.vocab = vocab
        self.addconfusion = addconfusion
        self.subconfusion = subconfusion
        self.transconfusion = transconfusion
        self.delconfusion = delconfusion
        self.bigram_dic = bigram_dic
        self.trigram_dic = trigram_dic
        self.letters = 'abcdefghijklmnopqrstuvwxyz'
        self.sentence = sentence
        self.wrongnum = wrongnum

    def trans(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        transword = []
        for l, r in splits[1:-1]:
            r_split = [(r[:i+1],r[i+1:]) for i in range(len(r))]
            for r_ in r_split:
                transword.append(l[:-1]+r_[0][-1]+r_[0][:-1]+l[-1]+r_[1])
        return transword



    def edits1(self, word):
        letters = self.letters
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]  # type: List[Tuple[Any, Any]]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = self.trans(word)
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def candidate1(self, word):
        candidate1 = []
        for k in self.edits1(word):
            if k in self.vocab:
                candidate1.append(k)
        return list(set(candidate1))


    def candidate2(self, word):
        candidate2 = []
        temp = (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
        for k in temp:
            if k in self.vocab:
                candidate2.append(k)
        return list(set(candidate2))


    def edittype(self, candi, cont):
        letters = self.letters
        candi, cont = candi.lower(), cont.lower()
        if len(candi) > len(cont):  # del
            for i in range(len(candi)):
                if candi[:i]+candi[i + 1:] == cont:
                    return candi[i - 1] + candi[i], 'del'
        elif len(candi) < len(cont):
            for i in range(len(cont)):
                if candi == cont[:i] + cont[i + 1:] or candi == cont[:-1]:
                    return cont[i - 1] + cont[i], 'ins'
        else:
            if candi in self.trans(cont):
                for i in range(len(candi)):
                    if candi[i] != cont[i]:
                     return candi[i] + cont[i], 'trans'
            else:
                for i in range(len(candi)):
                    if i < len(candi) - 1:
                        if candi in [cont[:i] + k + cont[i + 1:] for k in self.letters]:
                            return candi[i] + cont[i], 'sub'
                    if i == len(candi) -1:
                        return candi[i] + cont[i], 'sub'




    def channelmodel(self, x, y, edit):
        if edit == 'ins':
            if x == '#':
                return self.confusion[x + y] / self.corpus.count(' ' + y)
            else:
                return self.addconfusion[x + y] / self.corpus.count(x)
        if edit == 'sub':
            return self.subconfusion[(x + y)[0:2]] / self.corpus.count(y)
        if edit == 'trans':
            return self.transconfusion[x + y] / self.corpus.count(x + y)
        if edit == 'del':
            return self.delconfusion[x + y] / self.corpus.count(x + y)

con = Config()
con.load_data()
con.load_ngram()
c=correct(con.corpus, con.vocab, con.addconfusion, con.subconfusion,
          con.transconfusion, con.delconfusion, con.bigram_dic, con.trigram_dic,
          con.sentence, con.wrongnum)
#print(c.candidate1('Tkyo'))
punc=string.punctuation

# 逐句判断，输出结果
f = open('./result.txt','w')
findwr = []
for i in tqdm(range(0,1000)):
    count = 0
    newsent = c.sentence[i]
    words = c.sentence[i].split()
    for index,word in enumerate(words):
        if word not in c.vocab:
            #print(word)
            if word[-1] in punc: # 如果有标点符号，先去掉
                word = word[:-1]
            if word not in c.vocab: # 如果还不在，就小写
                word1 = word.lower()
                if word1 not in c.vocab: # 如果还不在，就取符号前的单词，可能是a's等形式
                    word2 = re.findall('\w+',word)[0]
                    if word2 not in c.vocab:  # 如果还不在，那基本就是错误词汇了
                        # print(word2)
                        candis = c.candidate1(word2)# 产生候选词
                        # print(candis)
                        p = np.zeros(len(candis))  # 储存候选词概率
                        #print(p)
                        if len(candis) == 1:
                            if index == 0:
                                newsent = newsent.replace(word2,candis[0].capitalize())
                                count += 1
                            else:
                                newsent = newsent.replace(word2, candis[0])
                                count += 1
                            #print(newsent)
                        elif len(candis) == 0:  # 如果没有候选词，应该是编辑距离为2的了
                            candis = c.candidate2(word2)
                            if len(candis) == 0:
                                continue
                            else:
                                p=np.zeros(len(candis))#储存候选词概率
                                for index1,candi in enumerate(candis):
                                    if 0 < index < len(words)-1:
                                        before = words[index-1]
                                        after = words[index+1]
                                    elif index == 0:
                                        before = '<s>'
                                        after = words[index+1]
                                        candi.capitalize()
                                    elif index == len(words)-1:
                                        before = words[index-1]
                                        after = '</s>'
                                    p2 = c.bigram_dic.get('%s %s' % (before,candi),0)
                                    p3 = c.bigram_dic.get('%s %s' % (candi,after),0)
                                    p[index1]=(p2+0.000001)*(p3+0.000001)*1000000+0.0001
                                newsent = newsent.replace(word2,candis[np.argmax(p)])
                                count += 1
                        else:
                            p=np.zeros(len(candis))  # 储存候选词概率
                            for index1,candi in enumerate(candis):
                                s = c.edittype(candi,word2)[0]
                                x = s[0]
                                y = s[1]
                                typ = c.edittype(candi,word2)[1]
                                p1 = c.channelmodel(x,y,edit=typ)
                                if 0 < index < len(words)-1:
                                    before = words[index-1]
                                    after = words[index+1]
                                elif index == 0:
                                    before = '<s>'
                                    after = words[index+1]
                                    candi.capitalize()
                                elif index == len(words)-1:
                                    before = words[index-1]
                                    after = '</s>'
                                p2= c.bigram_dic.get('%s %s'%(before,candi),0)
                                p3 = c.bigram_dic.get('%s %s'%(candi,after),0)
                                p[index1] = p1*(p2+0.000001)*(p3+0.000001)*1000000+0.0001
                            newsent = newsent.replace(word2,candis[np.argmax(p)])
                            count += 1

    if count < int(c.wrongnum[i]):
        cs, ps = [], []
        for index, word in enumerate(words):
            candidates = c.candidate1(word)
            #print(candidates)
            if len(candidates) == 0:
                candidates = c.candidate2(word)
            if len(candidates) == 0:
                continue
            else:
                p = np.zeros(len(candidates))
                for index1, candidate in enumerate(candidates):
                    if index == 0:
                        pass
                    elif index ==1:
                        before1 = '<s>'
                        before2 = words[index - 1]
                        after1 = words[index + 1]
                        after2 = words[index + 2]
                    elif 1<index<len(words) - 2:
                        before1 = words[index - 2]
                        before2 = words[index - 1]
                        after1 = words[index + 1]
                        after2 = words[index + 2]
                    elif index == len(words) - 2:
                        before1 = words[index - 2]
                        before2 = words[index - 1]
                        after1 = words[index + 1]
                        after1 = '</s>'
                    else:
                        pass
                    if index >= 1 and index <= len(words)-2:
                        p2 = c.trigram_dic.get('%s %s %s'%(before1,before2,candidate),0)
                        p3 = c.trigram_dic.get('%s %s %s'%(candidate,after1,after2),0)
                        p[index1] = (p2+0.000001)*(p3+0.000001)
                #cs.append(candidates[np.argmax(p)])
                #ps.append(p[np.argmax(p)])
            #candidate = sorted(zip(cs, ps), key=lambda x:x[1], reverse=True)[0][0]
                newsent = re.sub(r'%s' %word, r'%s' %candidates[np.argmax(p)], newsent, 1)
        #print(count);print(c.wrongnum[i]);print(newsent)
    f.writelines(['%s'%(i+1),'	','%s\n'%newsent])
# ,print(newsent)
f.close()