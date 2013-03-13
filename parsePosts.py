import math
import json
import os
import pickle
from lib.PorterStemmer import PorterStemmer 

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(f):
        print "Creating dir"
        os.makedirs(f)

def normCos(centroid, termList):
  normx = 0.0
  normy = 0.0
  dot = 0.0
  #print termList
  for i,x in enumerate(centroid):
    dot += (float(x) * float(termList[i]) )

    normx += math.pow(x, 2)
    normy += math.pow(float(termList[i]) , 2)
  #print "Normx: {0} Normy: {1} Dot: {2}".format(math.sqrt(normx), math.sqrt(normy), dot)
  return (dot / (math.sqrt(normx) * math.sqrt(normy)))

def printFloats(floatList):
  print ["%0.2f" % i for i in floatList]

def addTermsToDict(myDict, sortTerms, post_id):
  tempVal = None
  total = myDict["TOTAL_DOCS"]
  myDict["TOTAL_DOCS"] = total + 1

  for x in sortTerms:
    if (x != tempVal):
      tempVal = x
      count = sortTerms.count(x)
      if (x in myDict):
        existingVal = myDict[x]
        existingVal["Postings"].append((post_id, count))
        newPosting = existingVal["Postings"]
        myDict[x] = {"docs" : existingVal["docs"] + 1, "TotalCount": existingVal["TotalCount"] + count, "Postings": newPosting}
      else:
        myDict[x] = {"docs" : 1, "TotalCount":  count, "Postings": [(post_id, count)]}
  return myDict


def stopAndStem(testvar):
  p = PorterStemmer()

  output = ''
  word = ''

  print testvar["content"]

  openTag = False

  for c in testvar["content"]:
    if c.isalpha() and not openTag:
      word += c.lower()
    elif c == '<' and not openTag:
      openTag = True
    elif c == '>' and openTag:
      openTag = False
    elif not openTag:
      if word:
        #print "Found word: " + unicode(word) + "\n"
        if (word not in stopList):
          if (p.stem(word, 0,len(word)-1) == 'yang'):
            doc1 = open('./takewords.json', 'a')
            doc1.write(word + '\n')
          output += p.stem(word, 0,len(word)-1)
          output += ' '
        word = ''
  return output


def tfidf(termInfo, numDocs):
  nk = termInfo["docs"]
  idf = math.log( (float(numDocs) / float(nk)), 2)
  newPostingList = []
  for post in termInfo["Postings"]:
    x = post[1]
    newWt = float(x) * (idf)
    tup2 = post + (newWt,)
    newPostingList.append(tup2)
  termInfo["Postings"] = newPostingList





# Start script

doc1 = open('./testPosts.json', 'r')
testList = []
testvar = {}
myDict = {}
myDict["TOTAL_DOCS"] = 0

stopList = []

print str.encode('iso-8859-1')

stopWords = open('./stopWords.txt', 'r')
for i,x in enumerate(stopWords):
  if (not x.strip() == ''):
    stopList.append(x.strip())

#print stopList

i = 0
for rawline in doc1:
  testvar = dict(json.loads(rawline))
  testList.append(testvar)
  i += 1
  if i == 90:
    break

for testvar in testList:
  post_id = testvar["post_id"]
  print testvar["blogname"]
  output = stopAndStem(testvar)
  if (post_id != '834770'):
    myDict = addTermsToDict(myDict, output.split(), post_id)
  print output + '\n'
  if (len(output) > 0):
    ensure_dir('./' + str(post_id))
    testvar["output"] = output
    pickleFile = open('./' + str(post_id) + '/postPickle', 'wb+')
    pickle.dump(testvar, pickleFile)

print '\n\n'

totalDocs = myDict['TOTAL_DOCS']

for term in sorted(myDict):
  if (term != 'TOTAL_DOCS'):
    s = ''
    dictTerm = myDict[term]
    tfidf(dictTerm, totalDocs)
    s += "Term: " + unicode(term) + ": N Docs: " + unicode(dictTerm["docs"]) + ", Tot Freq: " + unicode(dictTerm["TotalCount"]) + ", Postings:\n\t\t"
    for post in dictTerm["Postings"]:
      s += "Doc#: " + unicode(post[0]) + ", Freq: " + unicode(post[1]) + ", Wt: " + unicode(post[2]) + " -> "
    s += "null"
    print s

