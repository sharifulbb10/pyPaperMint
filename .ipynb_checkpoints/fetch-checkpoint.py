#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
FIRST RUN THE DEFAULT CODE GIVEN

THEN OPEN 'Terminal'

CHANGE YOUR DIRECTORY TO 'pyPaperMint' FOLDER:
    cd pyPaperMint

IN THE TERMINAL, RUN THIS SCRIPT:
    python3 fetch.py --search 'textile' --maximum 50 --db arxiv --file_name yourFileName.xlsx
    
    (change 'textile' to what you want to search,
    you can omit --start 0
    '--db arxiv' or '--db others' command is mandatory)

    (you can also use short form of command in this way:
    python3 fetch.py -s 'textile' -m 50 --db arxiv -f yourFileName.xlsx)

    (while searching from ArXiv database, you can use --start 5 command, to specify that you want to extract result from 5th search result. Use the number instead of 5 that you want.)

IF YOU NEED HELP, TYPE:
    python3 fetch.py -h
'''

# !pip install -r requirements.txt

import feedparser
import argparse
import pandas as pd
import requests

def lowercase(value):
    return value.lower()
def prepare_search(value):
    txt = ''
    n = len(value.split(' '))
    for i, word in enumerate(value.split(' ')):
        if i != n-1:
            txt+=f"all:{word}+AND+"
        elif i == n-1:
            txt+=f"all:{word}"
    return txt

def prepare_search_others(value):
    txt = ''
    n = len(value.split(" "))
    for i, word in enumerate(value.split(" ")):
        if i != n-1:
            txt += "\"" + word + "\""+ " AND "
        elif i == n-1:
            txt += "\"" + word + "\""
    return txt

def to_text(list_):
    text = ''
    for i in list_:
        if list_[-1]!=i:
            i = i + ', '
            text +=i
    return text 

parser = argparse.ArgumentParser(description="YOU SHOULD SEARCH IN THIS FORMAT: \npython3 fetch.py --search 'your keywords' --maximum 10 --db arxiv --as 'file-name.xlsx' \n\nYOU CAN LOOK FOR HELP BY TYPING:\nfetch.py -h")

parser.add_argument("-s","--search", required = True, help = "the keyword or verbose you want to search\nExample: --search 'artificial intelligence in textile production'")
parser.add_argument("--start", default = 0, help = "first paper that you want accept from the search result. Let's say it is 5, this means, you want to accept result from 5th instance from your search.")
parser.add_argument("-m", "--maximum", default = 10, help = "maximum number of search result you want to accept. Let's say it is 10, that means, you want to accept 10 papers from your search. Default value is 10")
parser.add_argument("--db", choices=['arxiv', 'others'], type=lowercase, help="select your database, where you want to run your query. Choose either arXiv, or PubMed.")
parser.add_argument("-f", "--file_name", default="search-result.xlsx", help="your file name")

# args = parser.parse_args(['--search', 'ai', '--start', '0', '--maximum', '450', '--db', 'arxiv'])
args = parser.parse_args()

def arxiv_search():
    url = f"http://export.arxiv.org/api/query?search_query={prepare_search(args.search)}&start={args.start}&max_results={args.maximum}"
    feed = feedparser.parse(url)

    published_date = list()
    title = list()
    abstract = list()
    authors = list()
    doi = list()

    for index, entry in enumerate(feed.entries):
        published_date.append(entry.updated.split('T')[0])
        title.append((entry.title).replace('\n', ' '))
        abstract.append((entry.summary).replace('\n', ' '))
        names = list()
        for author in entry['authors']:
            names.append(author.name)
        authors.append((to_text(names).strip()))
        doi.append(entry.links[0]['href'])

    df = pd.DataFrame([
        published_date, title, abstract, authors, doi
    ], index = ['Published_Date', 'Title', 'Abstract', 'Authors', 'DOI'])

    df = df.T
    print(df)
    df.to_excel(f"{(args.file_name).split('.')[0]}_arXiv.xlsx", index = False)

def openAlex_search():

    published_date = list()
    title = list()
    abstract = list()
    authors_list = list()
    doi = list()

    url: str = None
    data: dict = None
    max_: int = None
    cursor: str = None

    def prepare_abstract(dict_found):
        word_list = list()
        try:
            for pair in dict_found:
                word = pair
                positions = dict_found[pair]
                for pos in positions:
                    last_pos = len(word_list)-1 if len(word_list)!=0 else 0
                    if pos > last_pos:
                        for i in range(last_pos, pos-1):
                            word_list.insert(i+1, '$')
                        word_list.insert(pos, word)
                    if pos <= last_pos:
                        if len(word_list)!=0: 
                            word_list[pos] = word
                        else: 
                            word_list.insert(0, word)
        except:
            pass
        text = " ".join(word_list)
        return text

    for i in range(1, int(args.maximum)//200+2):
        if i == int(args.maximum)//200+1:
            max_ = int(args.maximum)%200
            print('max_', max_)
        else:
            max_ = 200
            print(i, 'max_', max_)

        if i == 1:
            cursor = '*'
            url = f"https://api.openalex.org/works?search=({prepare_search_others(args.search)})&per-page={max_}&cursor={cursor}"
            print(url,'\n')
            data = requests.get(url).json()
            cursor = (data['meta'])['next_cursor']
            print('cursor', cursor)
        else:
            print('got here')
            url = f"https://api.openalex.org/works?search=({prepare_search_others(args.search)})&per-page={max_}&cursor={cursor}"
            print(url,'\n')
            data = requests.get(url).json()
            cursor = (data['meta'])['next_cursor']
            print('cursor', cursor)

        for index, entry in enumerate(data['results']):
            published_date.append(entry['publication_date'])
            title.append(entry['title'])
            abstract.append(prepare_abstract(entry['abstract_inverted_index']))
            authors_of_paper = list()
            for authors in entry['authorships']:
                institution = None
                try:
                    institution = "- "+(authors['institutions'][0])['display_name']
                except:
                    institution = ""
                authors_of_paper.append(f"{authors['author']['display_name']} {institution}")
            authors_list.append((to_text(authors_of_paper)).replace('\n',' '))
            doi.append(entry['doi'])

    df = pd.DataFrame([
        published_date, title, abstract, authors_list, doi
    ], index = ['Published_Date', 'Title', 'Abstract', 'Authors', 'DOI'])
    df = df.T

    df.to_excel(f"{(args.file_name).split('.')[0]}_openAlex.xlsx", index = False)

if args.db=='arxiv':
    arxiv_search()
    print('\nSearch result has been extracted successfully. Find your excel file on the project folder.\n')
elif args.db=='others':
    openAlex_search()
    print('\nSearch result has been extracted successfully. Find your excel file on the project folder.\n')

