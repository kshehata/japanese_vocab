from bs4 import BeautifulSoup
import sys

html_content = sys.stdin.read()
soup = BeautifulSoup(html_content, 'html.parser')

english = []
japanese = []

for s in soup.find_all('span', class_='css-11g2wvj'):
    if s.string:
        if s.string != 'Japanese' and s.string != 'English':
            english.append(s.string)
        continue
    for r in s.find_all('ruby'):
        for rt in r.find_all('rt'):
            f = rt.get_text(strip=True)
            if len(f) > 0:
                rt.insert_before('(' + rt.get_text(strip=True) + ')')
            rt.decompose()
    japanese.append(s.get_text(strip=True))

for j, e in zip(japanese, english):
    print(j + "\t" + e)
