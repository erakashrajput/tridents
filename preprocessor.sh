alternate_list=$(ls ./items/IT_A*.TXT)
product_list=$(ls ./items/IT_P*.TXT)
other=$(ls ./items/Live*.txt ./items/Item*.txt)


python nexla_record.py alternate $alternate_list
python nexla_record.py product $product_list
python nexla_record.py other

sort prod.txt attribute.txt LiveCad4Build.txt ItemRestrictions.txt > merge_line.txt
python nexla_record.py postprocess