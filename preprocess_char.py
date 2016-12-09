import csv
import string
import re

datafiles = ['./processed_data/train.tsv','./processed_data/val.tsv',
             './processed_data/test.tsv']

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
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter = "\t")
        for line in reader:
            # essay = NER_pat.sub('\\1', line.rstrip().split('\t')[2])
            # essay = NUM_pat.sub('NUMBER', essay)
            # word_list += re.split('\W', essay.lower())
            # word_list += essay.lower().split()
            if file.split('/')[2] == 'train.tsv':
                word_list.append(clean_data(line[2]))
                score_list.append(line[5])
            else:
                word_list.append(clean_data(line[3]))
                score_list.append(line[6])
    #print (min(score_list))
    
    cleaned_file = file.split(".tsv")[0] + "_char.tsv"
    with open(cleaned_file, "w") as f:
        i = 0
        for score, line in zip(score_list, word_list):
            if i > 0:
                f.write(str(score) + " " + line + "\n")
            i += 1