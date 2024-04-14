import os, requests, newspaper
from newspaper import Article
from langchain_community.tools.tavily_search import TavilySearchResults
import getpass
import os


from dotenv import load_dotenv
load_dotenv()



tool = TavilySearchResults(max_results=10)

res = tool.invoke({"query": "TGT stock news"})
print(res)

article_url = 'https://finance.yahoo.com/topic/stock-market-news/'
session = requests.session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

try:
    response = session.get(article_url, headers=headers, timeout=10)
    if response.status_code == 200:
        article = Article(article_url)
        article.download()
        article.parse()

        print(f"Title: {article.title}")
        print(f"Text: {article.text}")
    else:
        print(f"Failed to fetch article at {article_url}")
except Exception as e:
    print(f"Error occurred while fetching article at {article_url}: {e}")



