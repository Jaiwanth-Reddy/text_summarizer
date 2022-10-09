import gensim
import rouge

text = 'Your government is running with help of advertisements and speeches: L-G wrote to Arvind Kejriwal. Through the L-G, BJP destroying lives of Delhiites: Kejriwal shot back. The Delhi L-G and the chief minister have been embroiled in a long-drawn fight over several issues. By Amit Bhardwaj: In a scathing and unrestrained letter to Delhi Chief Minister Arvind Kejriwal, Lieutenant Governor (L-G) VK Saxena accused him and his ministers of running away from their constitutional duties and responsibilities of governance in the national capital. Your government is running with the help of advertisements and speeches, the L-G said in his letter to the AAP dispensation. The L-G, who has been embroiled in a long-drawn fight with Kejriwal, wrote that the AAP governments rule, based on "speeches and advertisements", was alienated from the works of basic public interest, reported news agency PTI. The letter comes days after Kejriwals deputy Manish Sisodia accused the L-G of interfering in the governments functioning and unconstitutionally setting up probes into its works and policies. Another love letter has come, Kejriwal tweeted today, referring to the L-Gs letter. Through the L-G, the BJP is hell bent on destroying the lives of Delhiites. Every day, they create controversy/brew trouble, the chief minister said in response to the letter. I assure all Delhiites that as long as this son of yours is alive, you dont have to worry, Kejriwal tweeted. According to the LG, his letters and instructions are meant to caution the government against errors and shortcomings. In his letter, Saxena flagged instructions about a probe into the now-scrapped excise policy, the absence of Kejriwal and his ministers at an event attended by President Droupadi Murmu, the power subsidy, the recruitment of teachers. Saxena also accused Kejriwal and his associates of levelling and spreading false charges against ministers and political opponents, causing "irreparable losses" to those they targetted.'


def gensim_textrank(text,summary_size = 0.25):
  text = [text]
  summary = [gensim.summarization.summarize(i,ratio=summary_size) for i in text]
  return(summary)

def get_rogue_score(original,generated):
  rouge_score = rouge.Rouge()
  score = rouge_score.get_scores(str(original), str(generated), avg=True)       
  return(score['rouge-1']['f'], 2)

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
