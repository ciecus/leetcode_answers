import os
import ast

class Config:
    def __init__(self):
        self.path = os.getcwd()
        self.corpus_file = os.path.join(self.path, 'text.txt')
        self.vocab_file = os.path.join(self.path, 'vocab.txt')
        self.addconfusion_file = os.path.join(self.path, 'addconfusion.data')
        self.subconfusion_file = os.path.join(self.path, 'subconfusion.data')
        self.transconfusion_file = os.path.join(self.path, 'revconfusion.data')
        self.delconfusion_file = os.path.join(self.path, 'delconfusion.data')
        self.bigram_dic_file = os.path.join(self.path, 'BigramLM.txt')
        self.trigram_dic_file = os.path.join(self.path, 'TrigramLM.txt')
        self.addword = ["ltMC.T.", "s", "wasn't", "isn't", "aren't", "we're", "wouldn't", "doesn't", "don't", "ltMC", "ll",
                   "They've", "they've", "you're", "they're", "you'd"]
        self.test_file = os.path.join(self.path, 'testdata.txt')

    def readfile(self, filename):
        with open(filename, 'r') as f:
            return f.read()


    def load_data(self):
        print('loading...data')
        self.vocab = self.readfile(self.vocab_file).split('\n')+self.addword
        self.corpus = self.readfile(self.corpus_file).strip('\n')
        self.addconfusion = ast.literal_eval(self.readfile(self.addconfusion_file))
        self.subconfusion = ast.literal_eval(self.readfile(self.subconfusion_file))
        self.transconfusion = ast.literal_eval(self.readfile(self.transconfusion_file))
        self.delconfusion = ast.literal_eval(self.readfile(self.delconfusion_file))
        self.test = self.readfile(self.test_file).split('\n')
        self.sentence = [item.split("\t")[2] for item in self.test]
        self.wrongnum = [item.split("\t")[1] for item in self.test]

    def readngram(self,filename):
        ngram_dic = {}
        with open(filename, 'r', encoding= 'gbk') as f:
            ngram = []
            for line in f:
                lines = line.strip()
                line_seg = lines.split('\t')
                if len(line_seg)<2:
                    continue
                ngram.append(line_seg)
            for item in ngram:
                ngram_dic = {item[1]: pow(10, float(item[0]))}
            return ngram_dic

    def load_ngram(self):
        print("loading...ngram")
        self.bigram_dic = self.readngram(self.bigram_dic_file)
        self.trigram_dic = self.readngram(self.trigram_dic_file)

if __name__ == "__main__":
    con = Config()
    con.load_data()



