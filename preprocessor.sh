#!/bin/bash

# echo "BASELINE FILE GENERATION STARTED: $(date)"
# cat items/IT_[PA]*.TXT | iconv -f latin1 -t utf-8 > baseline.txt

# echo "BASE FILE GENERATION STARTED: $(date)"
# python a.py baseline baseline.txt

# echo "LiveCad4Build.txt and ItemRestrictions.txt PROCESSING STARTED: $(date)"
# python a.py other

# echo "MERGE LINE STARTED: $(date)"
# sort base.txt LiveCad4Build.txt ItemRestrictions.txt > merge_line.txt

echo "NEXLA FILE PROCESSING STARTED: $(date)"
python a.py postprocess

echo "SUCCESS"