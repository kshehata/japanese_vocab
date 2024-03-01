#! /bin/bash

SRC="Japanese Vocab.xlsx"
if [ -r "$HOME/Downloads/$SRC" ]; then
    mv "$HOME/Downloads/$SRC" .
fi

python xls2csv.py "$SRC"
python check_dupes.py *.csv
