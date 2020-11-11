
def main():

    final_outputfile_jsonline = open("NX_MSCDIRECT_PROD_20201110.json", "w")
    merge_line_input_file = open("merge_line.txt","r")

    temp_string = ""
    older_key = ''

    for count, line in enumerate(merge_line_input_file):
        key, val = line.split("\t")
        if count == 0:
            older_key = key

        if key == older_key:
            temp_string = (temp_string+val.replace("\n", "")
                            ).replace("}{", ", ")
        else:
            
            x = '"op":"add", "path": "/products/pid-{}", "attributes": {}'
            if line != '':
                
                final_outputfile_jsonline.write(
                    "{ "+x.format(older_key, temp_string)+"}\n")

            else:
                
                final_outputfile_jsonline.write(
                    "{ "+x.format(older_key, temp_string)+"}\n")

            temp_string = val.replace("\n", "")
            older_key = key

    # CLOSE THE STREAMS
    merge_line_input_file.close()
    final_outputfile_jsonline.close()

if __name__ == "__main__":
    main()
    pass