# Comparison of three Natural Language Processing Techniques to summarize text

I use three methods. The first method is to use TF-IDF matrices. It is a logarithmic approach to classifying frequency of different words in the corpus. 

The second is to use the relative frequency of words in the text. That is, if we see a sentence containing words which are repeatedly used, we infer that the sentence must be important.

The third approach is to employ graphs by using the TextRank algorithm.

Finally, I compare the efficiency of the three techniques by using the widely used ROUGE score as a metric. That is here, the overlap between 1-Grams (or words) between the original text and the generated summary.
