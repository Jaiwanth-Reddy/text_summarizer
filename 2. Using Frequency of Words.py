text = ''
intensity = 1.5

text = text.replace('"','')
text = text.replace("'",'')

words = text.split(' ')

word_rank = {i:0 for i in set(words)}

for i in words:
    word_rank[i] += 1

sentences = text.split('.')

sentence_rank= {i:0 for i in set(sentences)}

for i in sentences:
    for j in word_rank.keys():
        if j in i:
            sentence_rank[i] += word_rank(j)

# we create a sentence rank by indirectly using the importance or frequency of each word in a given sentence

sum_of_sentences = sum([i for i in sentence_rank.values()])

average_frequency = sum_of_sentence_ranks/len(sentences)
        
threshold = int(average_frequency * intensity )

# only the sentences with the most important words will now be in the summary

summary = ''

for i in sentences:
    if sentence_rank[i] > threshold:
        summary += (i + ' ')

print(summary)