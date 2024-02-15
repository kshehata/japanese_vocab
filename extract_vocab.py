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
    kanji = ""
    kana = ""
    for r in s.find_all('ruby'):
        rt = r.find('rt')
        new_kana = ""
        if rt:
            new_kana = rt.get_text(strip=True)
            rt.decompose()
        if len(new_kana) < 1:
            new_kana = r.get_text(strip=True)
        kana += new_kana
        kanji += r.get_text(strip=True)
    japanese.append((kana, kanji))

for (kana, kanji), e in zip(japanese, english):
    if len(kana) < 1:
        kana = kanji
        kanji = ""
    print(kana + "\t" + kanji + "\t" + e)
