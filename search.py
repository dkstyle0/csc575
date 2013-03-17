import math
import json
import os
import pickle
import operator
import webbrowser
from lib.PorterStemmer import PorterStemmer 

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


dictfile = dictionaryFile = open('./dictionary', 'r')
myDict = pickle.load(dictfile)
end = False
p = PorterStemmer()

while(not end):
  respTable = {}
  colLength = 0
  simDict = {}
  print "What would you like to search for? (Ctrl-C to exit)"
  terms = raw_input().split(' ')
  for term in terms:
    term = p.stem(term, 0,len(term)-1)
    if term in myDict:
      #print myDict[term]
      #Go through postings for term
      for posting in myDict[term]["Postings"]:
        docId = posting[0]
        termWt = posting[2]
        if docId not in respTable:
          newList = [0]*colLength
          newList.append(termWt)
          respTable[docId] = newList
        else:
          respTable[docId].append(termWt)
    colLength += 1
    for key in respTable:
      #print respTable[key]
      docVector = respTable[key]
      if len(docVector) != colLength:
        docVector.append(0)
      cosSim = normCos([1]* colLength, docVector)
      simDict[key] = cosSim
    sortedDocs = sorted(simDict.iteritems(), key=operator.itemgetter(1), reverse=True)
  #print sortedDocs
  showDocs = 5 if len(sortedDocs) > 5 else len(sortedDocs)
  if showDocs > 0:
    print "Here's what was returned:"
    for x in range(showDocs):
      tmpDocId = sortedDocs[x][0]
      docFile = open('./' + str(tmpDocId) + '/postPickle', 'r')
      docObject = pickle.load(docFile)
      print str(x+1) + ': ' + unicode(docObject['title'])
    isInt = False
    while(not isInt):
      print 'Which article do you want to look at?'
      selected = raw_input()
      if (selected.isdigit()):
        isInt = True
        tmpDocId = sortedDocs[int(selected)-1][0]
        docFile = open('./' + str(tmpDocId) + '/postPickle', 'r')
        docObject = pickle.load(docFile)
        print unicode(docObject['content']) + '\n'
        outputFile = open('./selectedFile.html', 'w')
        outputFile.write('<html><body>' + docObject['content'].encode('utf-8') +  '</body></html>')
        outputFile.close()
        webbrowser.open_new_tab('file:///Users/dkuhn/classes/575/project/selectedFile.html')
  else:
    print 'No documents matched your query'    
