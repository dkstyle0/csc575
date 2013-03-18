575 Final Project

I created a basic search program that uses a number of annotated blog posts provided by a company called Kaggle.  They offer a number of such data sets for competition purposes, and I found this one that had a lot of general topic posts as well as a number of political posts, along with information on which users have marked that they liked.  My original idea was to be able to categorize groups of users into various groups along political lines and then to be able to offer suggestions for articles that are something they would probably like as well as articles from other groups of users.  I wasn't able to find a great data set to really accomplish this well, and due to time constraints I instead implemented just a basic document search.  

I implemented my project using the python language, since I did a lot of the homeworks with it and could reuse some code.  To get the resources, unzip the file included or get it from my github:

git clone https://github.com/dkstyle0/csc575.git

The data file I used can be downloaded with this link:

http://www.kaggle.com/c/predict-wordpress-likes/download/testPosts.zip

This is about 1GB after being unzipped and contains about 200,000 lines of json for each blog post, so I couldn't include it in the zipped resources.  

To start, I implemented a search of the documents by creating an inverse document matrix with raw term weights.  I made use of a python version of Porter's Stemmer algorithm that I found here:

http://tartarus.org/~martin/PorterStemmer/python.txt

Once I made this, I used the TFxIDF calculation to change the weights.  As the file is parsed, the program creates a directory using the postID as the name, and serializes the information about that blog post and places the file in that directory to be looked up later.  Lastly, the dictionary file is serialized to be used for later.  

The file that does this is parsePosts.py.  After unzipping the source documents and downloading the testPosts file to the same directory, run:

python parsePosts.py 5000

This will run for a longish time for all the records, so I limited it to the first 5,000 documents for my example, but changing the command line variable will change the number parsed.  Once this is done, you can run the search program:

python search.py

The dictionary file will load eventually depending on the size of it.  Once it does, you can enter a number of search terms to look for.  Using the terms (and taking out stop words), it will create a list of matching documents and create vectors for each document of the terms listed.  Then it will compare the vectors using cosine normalization and will list the top 5 matching documents.  The user can choose one that looks best (based on the blog post title) after which the text will be displayed in the terminal and in a Firefox tab since all the content includes the html markup.  The content in between the html tags is not included in the search terms, but included in order to show the content better for the user when opened in a browser. 

Example Output:

What would you like to search for? (Ctrl-C to exit)
obama
Here's what was returned:
1: Obama admits bio is fabricated
2: May Day Occupy Wall Street Epic Fail
3: Fox and Friends Ignores the 1st Anniversary of the Killing of Osama bin Laden
4: Gary Johnson Libertarian
5: Racially Motivated Attack In Norfolk?
Which article do you want to look at?
4
From his speech today.

1)  People in his home state wave at him with all five fingers, not just one.

2)  He climbed Mt Everest with a broken leg.

3)  He vetoed more legislation than all 49 governors combined.

4)  Talks of gun rights and gay rights in the same sentence.

5)  Says "make no bones about it"   Odd idiomatic expression.

6)  Ron Paul's support group, will vote for Johnson.

7)  Did NPR interview yesterday.

8)  Would die before voting for Mitt Romney or Barack Obama.

&nbsp;

&nbsp;

&nbsp;


---------

After this I made the script open up Firefox and open the contents of this wrapped in <html> and <body> tags so that the links and images show up somewhat accurately.  