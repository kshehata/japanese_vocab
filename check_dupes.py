import sys
import csv

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
            check_dupes(kana, all_kana, "kana", filename, r)
            check_dupes(kanji, all_kanji, "kanji", filename, r)
            check_dupes(english, all_english, "english", filename, r)
