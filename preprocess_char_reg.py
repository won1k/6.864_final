import csv
import string
import re
import cPickle

datafiles = ['./processed_data/train.tsv','./processed_data/val.tsv',
             './processed_data/test.tsv']

def percent(score, sidx):
    if sidx == 1:
        return (float(score) - 2) / 10
    elif sidx == 2:
        return (float(score) - 1) / 5
    elif sidx in [3,4]:
        return float(score) / 3
    elif sidx in [5,6]:
        return float(score) / 4
    elif sidx == 7:
        return (float(score) - 2) / 22
    else:
        return (float(score) - 10) / 50

def clean_data(text, keep_period = False):
    text = text.lower()

    NER_pat = re.compile("(@[a-z]+)[1-9]+")
    text = NER_pat.sub('\\1', text)

    NUM_pat = re.compile("(\d+)\S*")
    text = NUM_pat.sub('@number', text)

    keep_period = True

    if keep_period:
        text = re.sub('[^a-zA-Z0-9,.!?$-@]', ' ', text)
    else:
        text = re.sub('[^a-zA-Z0-9@]', ' ', text)
    return text

# Clean data
print "Cleaning data"
for file in datafiles:
    print file
    word_list = []
    score_list = []
    set_list = []
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter = "\t")
        i = 0
        for line in reader:
            # essay = NER_pat.sub('\\1', line.rstrip().split('\t')[2])
            # essay = NUM_pat.sub('NUMBER', essay)
            # word_list += re.split('\W', essay.lower())
            # word_list += essay.lower().split()
            if i > 0:
                if file.split('/')[2] == 'train.tsv':
                    if int(line[1]) < 7:
                        word_list.append(clean_data(line[2]))
                        score_list.append(percent(line[5], int(line[1])))
                        set_list.append(int(line[1]))
                else:
                    if int(line[2]) < 7:
                        word_list.append(clean_data(line[3]))
                        score_list.append(percent(line[6], int(line[2])))
                        set_list.append(int(line[2]))
            i += 1
    #print (min(score_list))
    
    cleaned_file = file.split(".tsv")[0] + "_char_reg"
    with open(cleaned_file + ".tsv", "w") as f:
        for score, line in zip(score_list, word_list):
            f.write(str(score) + " " + line + "\n")

    cPickle.dump({'scores': score_list, 'essays': word_list, 'sets': set_list}, open(cleaned_file + ".p", "w"))






