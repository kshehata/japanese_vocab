import sys
import csv
import re
import string

kanji_re = re.compile(r"[\s\u3000-\u30ff\u4e00-\u9fff]+")
kana_re = re.compile(r"[\s\u3000-\u30ff]+")
english_re = re.compile(r"[\sa-zA-Z0-9\u3000-\u303f\u2000-\u206f"
                        + re.escape(string.punctuation)
                        + r"]+")

def is_kana(s):
    return kana_re.fullmatch(s) is not None

def is_kanji(s):
    return kanji_re.fullmatch(s) is not None

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
            kana = r[cols_map["kana"]]
            kanji = r[cols_map["kanji"]]
            english = r[cols_map["english"]]
            if not is_kana(kana):
                print(f"Invalid kana: {kana}, file: {filename}, row: {r}")
            if len(kanji) > 0 and not is_kanji(kanji):
                print(f"Invalid kanji: {kanji}, file: {filename}, row: {r}")
            if len(kanji) > 0 and is_kana(kanji):
                print(f"Kanji is kana: {kanji}, file: {filename}, row: {r}")
            if not is_english(english):
                print(f"Invalid english: {english}, file: {filename}, row: {r}")
            check_dupes(kana, all_kana, "kana", filename, r)
            check_dupes(kanji, all_kanji, "kanji", filename, r)
            check_dupes(english, all_english, "english", filename, r)
