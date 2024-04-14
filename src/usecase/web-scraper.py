import requests
from bs4 import BeautifulSoup

my_url = 'https://finance.yahoo.com/topic/stock-market-news/'
response = requests.get(my_url)

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
r = requests.get(my_url,headers=headers)
soup = BeautifulSoup(r.content,'lxml')

print("response.ok : {} , response.status_code : {}".format(response.ok , response.status_code))

def get_page(url):
    """Download a webpage and return a beautiful soup doc"""
    response = requests.get(url)
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')
    return doc

doc = get_page(url=my_url)

# print(doc.find('title'))

div_tags = soup.find_all('div', {'id': "Fin-Stream"})
uls = div_tags[0].find('ul')
lis = list(uls.descendants)
li_tags = soup.find_all('li', {'class': "js-stream-content Pos(r)"})

# news-stream  svelte-17l7f4i
# print(len(div_tags))
print(len(lis))
# print(uls['class'])
# print(lis[0].find('a').text)
# print(lis[0].find('p').text)
divs = lis[0].find('div', {'class': 'C(#959595) Fz(11px) D(ib) Mb(6px)'})
print(divs)
# sp = [x.text for x in divs.descendants]

# print(sp)
# for div in divs:
#     # print(div.text)
#     # want the second span in the div
#     span = div.find_next('span').find_next('span')
#     print(span.string)
# print(lis[0].find_all('span'))