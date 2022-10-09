text = ''
intensity = 1.5 # the higher this number, the shorter the summary.

text = text.replace('"','')
text = text.replace("'",'')

words = text.split(' ')

word_rank = {i:0 for i in set(words)}

for i in words:
    word_rank[i] += 1

# we get the frequency of every word of the text.

tf = {i:word_rank[i]/len(words) for i in word_rank.keys()}

sentences = text.split('.')

pre_idf = {i:1 for i in set(words)}

for i in pre_idf.keys():
    for j in sentences:
        if i in j:
            pre_idf[i] += 1

from math import log

idf = {i:log(len(sentences)/pre_idf[i]) for i in pre_idf.keys()}

tf_idf_matrix = {}

# multiplying the tf and idf matrices

for word,rank in tf.items():
    tf_idf_matrix[word] = rank*idf[word]

sentence_scores = {i:0 for i in sentences}

for i in sentences:
    score = 0
    for j in i:
        if j in tf.keys():
            score += tf[j]
    if len(i) != 0:
	    score /= len(i)

    sentence_scores[i] = score

sum_of_scores = sum([i for i in sentence_scores.values()])

average_score = sum_of_scores/len(sentences)

threshold = average_score * intensity

summary = ''

for i in sentences:
    if sentence_scores[i] > threshold:
        summary += (i + ' ')

print(summary)
