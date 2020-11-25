#!/bin/bash

echo "BASELINE FILE GENERATION STARTED: $(date)"
cat items/IT_[PA]*.TXT | iconv -f latin1 -t utf-8 > baseline.txt

echo "BASE FILE GENERATION STARTED: $(date)"

# python nexla_record.py alternate $(ls ./items/IT_[A]*.TXT)

# echo "BASE FILE GENERATION STARTED: $(date)"
# python nexla_record.py product $(ls ./items/IT_[P]*.TXT)

echo "BASE FILE GENERATION STARTED: $(date)"
python a.py baseline baseline.txt

echo "LiveCad4Build.txt and ItemRestrictions.txt PROCESSING STARTED: $(date)"
python a.py other

echo "MERGE LINE STARTED: $(date)"
sort base.txt LiveCad4Build.txt ItemRestrictions.txt > merge_line.txt
# sort prod.txt attribute.txt LiveCad4Build.txt ItemRestrictions.txt > merge_line.txt

echo "NEXLA FILE PROCESSING STARTED: $(date)"
# python nexla_record.py postprocess
python a.py postprocess

echo "SUCCESS"