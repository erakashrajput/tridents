#!/bin/bash

echo $(date)
cat items/IT_[PA]*.TXT | iconv -f latin1 -t utf-8 > baseline.txt
echo $(date)
python nexla_record.py baseline baseline.txt
echo "Baseline file is created with encording"
echo $(date)

python nexla_record.py other
echo "LiveCad4Build.txt and ItemRestrictions.txt created "
sort base.txt LiveCad4Build.txt ItemRestrictions.txt > merge_line.txt
python nexla_record.py postprocess

echo "file Nexla file generateion completed"