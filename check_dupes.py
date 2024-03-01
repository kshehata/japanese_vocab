import sys
import csv
import re
import string

furigana_full_re = re.compile(r"(([\u3007\u4e00-\u9fff]+)\(([\u3000-\u30ff]+)\)|([\s_\u3000-\u30ff]+))*")
furigana_single_re = re.compile(r"([\s\u4e00-\u9fff]+)\(([\u3000-\u30ff]+)\)")
english_re = re.compile(r"[\sa-zA-Z0-9\u3000-\u303f\u2000-\u206f"
                        + re.escape(string.punctuation)
                        + r"]+")

def valid_furigana(s):
    return furigana_full_re.fullmatch(s) is not None

def furi2kanji(s):
    return re.sub(r"\([^\)]*\)", "", s)

def furi2kana(s):
    return furigana_single_re.sub(r"\2", s)

def is_english(s):
    return english_re.fullmatch(s) is not None

def check_dupes(item, all_items, name, filename, row):
    if len(item) > 0 and item in all_items:
        print(f"Duplicate {name}: {item}, file: {filename}, row: {row}")
    all_items.add(item)

if len(sys.argv) < 2:
    print("Usage: check_dupes filenames")
    sys.exit(1)

all_kana = set()
all_kanji = set()
all_english = set()

for filename in sys.argv[1:]:
    with open(filename) as file:
        csv_reader = csv.reader(file, delimiter=',')
        columns = next(csv_reader)
        cols_map = { col: i for i, col in enumerate(columns) }
        for r in csv_reader:
            japanese  = r[cols_map["japanese"]]
            english = r[cols_map["english"]]
            if not valid_furigana(japanese):
                print(f"Invalid furigana: {japanese}, file: {filename}, row: {r}")
            if not is_english(english):
                print(f"Invalid english: {english}, file: {filename}, row: {r}")
            check_dupes(furi2kana(japanese), all_kana, "kana", filename, r)
            check_dupes(furi2kanji(japanese), all_kanji, "kanji", filename, r)
            check_dupes(english, all_english, "english", filename, r)
