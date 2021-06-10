from nltk.translate.bleu_score import sentence_bleu
reference = [['the', 'cat',"is","sitting","on","the","mat"]]
test = ["there",'is',"cat","sitting","cat"]
score = sentence_bleu(reference, test)
print(score)