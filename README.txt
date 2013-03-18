575 Final Project

I created a basic search program that uses a number of annotated blog posts provided by a company called Kaggle.  They offer a number of such data sets for competition purposes, and I found this one that had a lot of general topic posts as well as a number of political posts, along with information on which users have marked that they liked.  My original idea was to be able to categorize groups of users into various groups along political lines and then to be able to offer suggestions for articles that are something they would probably like as well as articles from other groups of users.  I wasn't able to find a great data set to really accomplish this well, and due to time constraints I instead implemented just a basic document search.  

I implemented my project using the python language, since I did a lot of the homeworks with it and could reuse some code.  To get the resources, unzip the file included or get it from my github:

git clone https://github.com/dkstyle0/csc575.git

The data file I used can be downloaded with this link:

http://www.kaggle.com/c/predict-wordpress-likes/download/testPosts.zip

This is about 1GB after being unzipped and contains about 200,000 lines of json for each blog post, so I couldn't include it in the zipped resources.  I did include a sample file that can be called using the 'sample' runtime argument (see below).  The sample contains the first 5000 lines of the collection.  

To start, I implemented a search of the documents by creating an inverse document matrix with raw term weights.  I made use of a python version of Porter's Stemmer algorithm that I found here:

http://tartarus.org/~martin/PorterStemmer/python.txt

Once I made this, I used the TFxIDF calculation to change the weights.  As the file is parsed, the program creates a directory using the postID as the name, and serializes the information about that blog post and places the file in that directory to be looked up later.  Lastly, the dictionary file is serialized to be used for later.  

The file that does this is parsePosts.py.  After unzipping the source documents and downloading the testPosts file to the same directory, run:

## TO RUN WITH THE NORMAL TESTPOSTS FILE
python parsePosts.py 5000

## TO RUN WITH THE INCLUDED SAMPLE POSTS FILE
python parsePosts.py 5000 sample

This will run for a longish time for all the records, so I limited it to the first 5,000 documents for my example, but changing the command line variable will change the number parsed.  For example, here it is being run with just the first two documents:



> python parsePosts.py 2 sample
3
iso-8859-1
Matt on Not-WordPress
I took part in the <a href="http://en.blog.wordpress.com/2012/04/10/automattics-worldwide-wp-5k/">Automattic Wordwide WordPress 5k</a>, in what is becoming a yearly tradition. To switch it up I ran it barefoot along the soft white sand beach near Seaside, FL. Here's how the route ended up, ended up about 5.7k:

<a href="http://runkeeper.com/user/photomatt/activity/84752773"><img alt="" src="http://f.cl.ly/items/2F183y0d361n1S35091C/Screen%20Shot%202012-04-29%20at%205.59.40%20PM.png" class="alignnone" width="723" height="482" /></a>

Took some cool pictures along the way that I'll post now.
automatt wordwid wordpress becom yearli tradit switch ran barefoot soft white sand beach near seasid fl rout cool pictur ll post 

Matt on Not-WordPress
<a href="http://matt.files.wordpress.com/2012/04/photo31.jpg"><img src="http://matt.files.wordpress.com/2012/04/photo31.jpg" alt="" title="photo31" width="1000" height="750" class="alignnone size-full wp-image-3930" /></a>


Matt on Not-WordPress
<a href="http://matt.files.wordpress.com/2012/04/photo32.jpg"><img src="http://matt.files.wordpress.com/2012/04/photo32.jpg" alt="" title="photo32" width="1000" height="750" class="alignnone size-full wp-image-3932" /></a>





Term: automatt: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: barefoot: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: beach: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: becom: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: cool: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: fl: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: ll: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: near: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: pictur: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: post: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: ran: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: rout: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: sand: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: seasid: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: soft: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: switch: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: tradit: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: white: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: wordpress: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: wordwid: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null
Term: yearli: N Docs: 1, Tot Freq: 1, Postings:
                Doc#: 24766, Freq: 1, Wt: 1.58496250072 -> null



Once this is done, you can run the search program:

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