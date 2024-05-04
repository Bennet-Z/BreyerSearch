from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

initialPage = urlopen("https://www.identifyyourbreyer.com/identify/traditional.htm").read()
pattern = r'^[^\/\\]*\.htm$'
soup = BeautifulSoup(initialPage, 'html.parser')
links = []
for link in soup.find_all('a', href=re.compile(pattern)):
    links.append(link.get('href'))
html_list = []
for l in links:
    page = urlopen('https://www.identifyyourbreyer.com/identify/' + l).read()
    soup = BeautifulSoup(page, 'html.parser')
    html_list.append(soup)




