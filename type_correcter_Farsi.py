#problem: we are trying to choose the most likely spelling correction for words#
#By Bayes' Theorem we try to compute P(c|w)=P(w|c) P(c) / P(w)#
#from candidates we should choose one with highest probability#
#Since P(w) is the same for every possible c, we can ignore it#

import re, collections, codecs

#words function extract the individual words from the file#
def words(text):
    text = re.findall('[ا-ي&گ&پ&ژ&چ&ی&آ&ک]+', text)
    return text
    
#we count how many times each word occurs, using the function train (we train a probability model)#
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#here we use a big corpus to build a dictionary of words in a language, with the occurence number for the values#
fp = open('output.txt', 'r', encoding= 'utf-8')
txt = fp.read()
NWORDS = train(words(txt))
fp.close()

alphabet = 'ابپتثجچحخدذرزسشصضطظعغفقکگلمنوهي'
#here we will create the possible words occure with error in typing which need one edition to turn into correct word#

def edit_dist1(word):
    
   #splits: split the word into two parts (a and b)to define the location of changes#
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

#to create the words which have edit_distance=2 with the correct form we will apply edits1 to all the results of edits1#
#only keep the candidates that are actually known words#
def known_edit_dist2(word):
    return set(e2 for e1 in edit_dist1(word) for e2 in edit_dist1(e1) if e2 in NWORDS)

#for p(w|c): known words of edit distance 0 are probable than a known words of edit distance 1 which are #
# more probable than known words of edit distance 2# 
#"known word" means a word that we have seen in the language model training data#
def known(words): return set(w for w in words if w in NWORDS)

#words with the shortest edit distance to the original word have highest P(c) value#
def correct(word):
    candidates = known([word]) or known(edit_dist1(word)) or known_edit_dist2(word) or [word]
    return max(candidates, key=NWORDS.get)

#now we read a file which has errors, correct them, and save the corrected in a separate file#
fp1 = open('witherror.txt', 'r', encoding= 'utf-8')
txt = fp1.read()
txt = txt.replace('،',' ')
txt = txt.split()
s = ''
for word in txt:
    n = correct(word)
    s = s + n + ' '

fp2 = open('corrected.txt','w', encoding= 'utf-8')
fp2.write(s)
fp1.close()
fp2.close()

