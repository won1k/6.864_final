import csv

reader = csv.reader(open("processed_data/train.tsv","r"), delimiter = "\t")

max_score_7 = 0
max_score_8 = 0
min_score_7 = 10
min_score_8 = 10
num_essays_7 = 0
num_essays_8 = 0

for item in reader:
	try:
		if int(item[1]) == 5:
			num_essays_7 += 1
			if int(item[5]) > max_score_7:
				max_score_7 = int(item[5])
			if int(item[5]) < min_score_7:
				min_score_7 = int(item[5])
		if int(item[1]) == 6:
			num_essays_8 += 1
			if int(item[5]) > max_score_8:
				max_score_8 = int(item[5])
			if int(item[5]) < min_score_8:
				min_score_8 = int(item[5])
	except:
		continue

print min_score_7
print max_score_7
print num_essays_7
print min_score_8
print max_score_8
print num_essays_8