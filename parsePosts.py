import math
import json
import os
import pickle
import sys
from lib.PorterStemmer import PorterStemmer 

##
# Takes a path name and makes sure the directory exists, if not creates it
##
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(f):
        print "Creating dir"
        os.makedirs(f)

##
# Cosine Normalization Function.  Takes 2 vectors and returns the normalized cosine value for the two
##
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

##
# Pretty printing of list of Float objects
##
def printFloats(floatList):
  print ["%0.2f" % i for i in floatList]

##  
# Function that adds new terms to dictionary
# params: myDict : existing dictionary
# sortTerms: sorted list of terms from a new Document
# post_id: Id of the document being parsed
##
def addTermsToDict(myDict, sortTerms, post_id):
  tempVal = None
  total = myDict["TOTAL_DOCS"]
  # Keep track of the total number of documents
  myDict["TOTAL_DOCS"] = total + 1

  for x in sortTerms:
    if (x != tempVal):
      tempVal = x
      count = sortTerms.count(x)
      # If term exists in dictionary, update the list of postings and total count
      if (x in myDict):
        existingVal = myDict[x]
        existingVal["Postings"].append((post_id, count))
        newPosting = existingVal["Postings"]
        myDict[x] = {"docs" : existingVal["docs"] + 1, "TotalCount": existingVal["TotalCount"] + count, "Postings": newPosting}
      # Otherwise create a new record
      else:
        myDict[x] = {"docs" : 1, "TotalCount":  count, "Postings": [(post_id, count)]}
  return myDict

##
# Function to remove stop words and run the Porter Stemmer algorithm
##
def stopAndStem(testvar):
  p = PorterStemmer()

  output = ''
  word = ''

  print testvar["content"]
  
  # Filter out text that is found inside html tags
  openTag = False

  try:
    for c in testvar["content"]:
      if c.isalpha() and not openTag:
        word += c.lower()
      # Start of an html tag, ignore content after this
      elif c == '<' and not openTag:
        openTag = True
      # End of tag, accept content again
      elif c == '>' and openTag:
        openTag = False
      elif not openTag:
        if word:
          #print "Found word: " + unicode(word) + "\n"
          if (word not in stopList):
            # Output is the list of stemmed words
            output += p.stem(word, 0,len(word)-1)
            output += ' '
          word = ''
  except Exception, e:
    pass
  return output

##
# Function for calculating the tfidf weighting
##
def tfidf(termInfo, numDocs):
  nk = termInfo["docs"]
  # Caculate idf for the terms by diving total number of documents by number of terms with the term (log 2)
  idf = math.log( (float(numDocs) / float(nk)), 2)
  newPostingList = []
  for post in termInfo["Postings"]:
    x = post[1]
    newWt = float(x) * (idf)
    tup2 = post + (newWt,)
    newPostingList.append(tup2)
  termInfo["Postings"] = newPostingList





# Start script
doc1 = None
useSample = None
if (len(sys.argv) > 2):
  print len(sys.argv)
  useSample = sys.argv[2]

if (useSample == 'sample'):
  doc1 = open('./testPosts.json.sample', 'r')
else:
  doc1 = open('./testPosts.json', 'r')
testList = []
testvar = {}
myDict = {}
myDict["TOTAL_DOCS"] = 0

numPosts = int(sys.argv[1])

stopList = []

print str.encode('iso-8859-1')

# Create list of stopWords
stopWords = open('./stopWords.txt', 'r')
for i,x in enumerate(stopWords):
  if (not x.strip() == ''):
    stopList.append(x.strip())

#print stopList

i = 0
# Read in blog information, break at 50000 just for memory usage reasons
for rawline in doc1:
  testvar = dict(json.loads(rawline))
  testList.append(testvar)
  if i == numPosts:
    break
  else:
    i += 1

for testvar in testList:
  post_id = testvar["post_id"]
  print testvar["blogname"]
  # Create output 
  output = stopAndStem(testvar)
  if (post_id != '834770'):
    myDict = addTermsToDict(myDict, output.split(), post_id)
  print output + '\n'
  # If output is longer than 1 (some blogs are just anchor tags), create a directory and file that holds in information
  if (len(output) > 0):
    ensure_dir('./docDir/' + str(post_id))
    testvar["output"] = output
    pickleFile = open('./docDir/' + str(post_id) + '/postPickle', 'wb+')
    pickle.dump(testvar, pickleFile)

print '\n\n'

totalDocs = myDict['TOTAL_DOCS']


# Once dictionary is created, create tfidf weightings 
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

# Dump the dictionary to a file for searching later
dictionaryFile = open('./dictionary', 'wb+')
pickle.dump(myDict, dictionaryFile)