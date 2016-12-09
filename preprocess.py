import re
import string
import csv
import numpy as np
import cPickle

datafiles = ['./processed_data/train.tsv','./processed_data/val.tsv',
             './processed_data/test.tsv']
vdim = 300

'''
Schema:
essay_id essay_set essay rater1_domain1 rater2_domain1 domain1_score

The entitities identified by NER are:
    "PERSON", "ORGANIZATION", "LOCATION", "DATE", "TIME", "MONEY", "PERCENT"
'''
def clean_data(text, keep_period = False):
    text = text.lower()

    NER_pat = re.compile("(@[a-z]+)[1-9]+")
    text = NER_pat.sub('\\1', text)

    NUM_pat = re.compile("(\d+)\S*")
    text = NUM_pat.sub('@number', text)

    if keep_period:
        text = re.sub('[^a-zA-Z0-9.@]', ' ', text)
    else:
        text = re.sub('[^a-zA-Z0-9@]', ' ', text)
    return text

# Get word2idx from glove
print "GloVe vectors"
word2idx = {}
idx2word = {}
emb_matrix = []
i = 0
with open("rcnn/code/glove.txt", "r") as f:
    reader = csv.reader(f, delimiter = ' ')
    for line in reader:
        word = line[0]
        vec = line[1:]
        word2idx[word] = i
        idx2word[i] = word
        emb_matrix.append(vec)
        i += 1
m = np.array(emb_matrix, dtype = np.float)
emb_matrix.append(list(np.mean(m, axis = 0)))
word2idx["unk"] = i
idx2word[i] = "unk"
cPickle.dump(word2idx, open("./processed_data/word2idx.p", "w"))
cPickle.dump(idx2word, open("./processed_data/idx2word.p", "w"))
cPickle.dump(np.array(emb_matrix, dtype = np.float), open("./processed_data/glove.p", "w"))

# Clean data
print "Cleaning data"
for file in datafiles:
    word_list = []
    score_list = []
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter = "\t")
        for line in reader:
            # essay = NER_pat.sub('\\1', line.rstrip().split('\t')[2])
            # essay = NUM_pat.sub('NUMBER', essay)
            # word_list += re.split('\W', essay.lower())
            # word_list += essay.lower().split()
            word_list.append(clean_data(line[2]).split())
            score_list.append(line[5])
    #print (min(score_list))
    
    cleaned_file = file.split(".tsv")[0] + "_clean.tsv"
    with open(cleaned_file, "w") as f:
        i = 0
        for score, line in zip(score_list, word_list):
            if i > 0:
                f.write(str(score) + " " + string.join(line) + "\n")
            i += 1

    idx_file = file.split(".tsv")[0] + "_idx.tsv"
    with open(idx_file, "w") as f:
        writer = csv.writer(f)
        idxs = []
        for line in word_list:
            line_idx = []
            for word in line:
                try:
                    line_idx.append(word2idx[word])
                except:
                    line_idx.append(word2idx["unk"])
            idxs.append(line_idx)
        writer.writerows(idxs)


#words = sorted(list(set(word_list)))
#for word in words: print(word)
#print('total words:', len(words))
#word2idx = dict((w, i) for i, w in enumerate(words))
#idx2word = dict((i, w) for i, w in enumerate(words))

