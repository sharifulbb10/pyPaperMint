# pyPaperMint
Terminal-based Python tool to fetch scholarly articles from arXiv and OpenAlex.

## Project Overview
This project is to easily collect scholarly articles from <b>arXiv</b> and <b>OpenAlex</b> api. Users can run a terminal based python command and scholarly papers' data will get organised in an excel file.

![Excel Interface](https://raw.githubusercontent.com/sharifulbb10/pyPaperMint/refs/heads/main/images/Screenshot_2025-10-25_22-34-08.png)

## How to use it
You can use the project in two ways:</p>
- [Using Google Colab](#using-google-colab)</li>
- [Using Terminal](#using-terminal)
### Using Google Colab
1. Go to this pre-built [Google Colab](https://colab.research.google.com/drive/1JviqD38lrQosq4MX9bJsXWGgMpSt8cLd?usp=sharing#scrollTo=aIB329hWMNLN) directory. There you will find necessary directions, but useful instructions and explanations are also shared here in the next steps.
2. Run the script by simply clicking on <code>Run All</code> option just beneath the menu bar in the interface.
3. Open <code>Terminal</code> from the bottom-right corner and run this command:<br/>
<pre>cd pyPaperMint</pre>
4. To extract some papers from <i>arXiv</i> based on <i>AI in Agriculture</i> search-key, you can run this command:<br/>
<pre>python3 fetch.py --search 'AI in Agriculture' --maximum 100 --db arxiv --file_name AI-in-Agriculture.xlsx</pre>
<b>NB:</b> You can replace <i>`AI in Agriculture`</i> to whatever your search-key is. Replace <i>`100`</i> with how many maximum number of searches you want to extract. Additionally, you can add <code>--start 50</code> command to extract results from 50th instance to your maximum range. You can replace <i>`AI-in-Agriculture.xlsx`</i> with whatever name of your file you want to keep. You can omit <code>--file_name AI-in-Agriculture.xlsx</code> part as well, this will generate a default name based on your search-kyes, so no worries!<br/>If you want to make a generalized search of papers from other databases except <i>arXiv</i>, you can replace <code>arxiv</code> with <code>others</code>, it will use <i>Open Alex API</i> to search results from empirical scholarly databases.<br/>
If you want, you can use a shorter version of the previous terminal command as well:
<pre>python3 fetch.py -s 'AI in Agriculture' -m 100 --db arxiv -f AI-in-Agriculture.xlsx</pre>
4. Now, open `Files` from left-hand side and navigate to `pyPaperMint` folder to see your intended `.xlsx` file.
### Using Terminal
(This instructions are meant for `Linux` operating system, so you have to modify these instructions accordingly to use it on any `Windows` operating system e.g. Window OS does not has in-built terminal, but you can set-up shell or similar things. Take a look over internet to know how to set up a terminal on Windows OS.)
1. Make a directory or folder first.
2. Open your terminal from that directory, otherwise, open terminal and go to your directory: <br/>
<pre>cd ./your-folder-path</pre>
3. Clone this github project:<br/>
<pre>git clone https://github.com/sharifulbb10/pyPaperMint.git</pre>
4. Go to the project folder:<br/>
<pre>cd ./pyPaperMint</pre>
5. To extract some papers from <i>arXiv</i> based on <i>AI in Agriculture</i> search-key, you can run this command:<br/>
<pre>python3 fetch.py --search 'AI in Agriculture' --maximum 100 --db arxiv --file_name AI-in-Agriculture.xlsx</pre>
<b>NB:</b> You can replace <i>`AI in Agriculture`</i> to whatever your search-key is. Replace <i>`100`</i> with how many maximum number of searches you want to extract. Additionally, you can add <code>--start 50</code> command to extract results from 50th instance to your maximum range. You can replace <i>`AI-in-Agriculture.xlsx`</i> with whatever name of your file you want to keep. You can omit <code>--file_name AI-in-Agriculture.xlsx</code> part as well, this will generate a default name based on your search-keys, so no worries!<br/>If you want to make a generalized search of papers from other databases except <i>arXiv</i>, you can replace <code>arxiv</code> with <code>others</code>, it will use <i>Open Alex API</i> to search results from empirical scholarly databases.<br/>
If you want, you can use a shorter version of the previous terminal command as well:
<pre>python3 fetch.py -s 'AI in Agriculture' -m 100 --db arxiv -f AI-in-Agriculture.xlsx</pre>
6. Now, you can see your excel file inside your pyPaperMint folder.
