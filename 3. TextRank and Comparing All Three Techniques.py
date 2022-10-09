import gensim
import rouge

def gensim_textrank(text,summary_size = 0.25):
  text = [text]
  summary = [gensim.summarization.summarize(i,ratio=summary_size) for i in text]
  return(summary)

def get_rogue_score(original,generated):
  rouge_score = rouge.Rouge()
  score = rouge_score.get_scores(str(original), str(generated), avg=True)       
  return(score['rouge-1']['f'], 2)

text = ''
text = text.replace(",","")
text = text.replace('"','')

intensity = 1.5

words = text.split(' ')

word_rank = {i:0 for i in set(words)}

for i in words:
    word_rank[i] += 1

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

tf_idf_summary = ''

for i in sentences:
    if sentence_scores[i] > threshold:
        tf_idf_summary += (i + ' ')


sentence_rank= {i:0 for i in set(sentences)}

for i in sentences:
    for j in word_rank.keys():
        if j in i:
            sentence_rank[i] += word_rank[j]

sum_of_sentence_ranks = sum([i for i in sentence_rank.values()])

average_frequency = sum_of_sentence_ranks/len(sentences)
        
threshold = int(average_frequency * intensity )

frequency_summary = ''

for i in sentences:
    if sentence_rank[i] > threshold:
        frequency_summary += (i + ' ')

gensim_summary = gensim_textrank(text)

tf_idf_rouge = get_rogue_score(text,gensim_summary)[0]

frequency_rouge = get_rogue_score(text,frequency_summary)[0]

gensim_rouge = get_rogue_score(text,gensim_summary)[0]

print('Performance of three techniques\nTF-IDF: ' + str(tf_idf_rouge) + '\nFrequency Method: ' + str(frequency_rouge) + '\nTextRank Method: ' + str(gensim_rouge)) 
