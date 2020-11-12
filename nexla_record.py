import time
import logging
import sys
import json
import re

LOG_FILENAME = 'stats.log'

logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

def record_creator(file_, output_file):
    entry_dict = dict()
    specification_key = ''
    crumb=''
    crumb_id=''
    rf_string=''
    prod_key = ''
    try:
        input_file = open(file_,"r")
        
        # with open(file_, "r", errors='replace') as input_file: 
       
        for line in input_file:
            try:
                line = line.replace("\n", "")

                if line == "":  # EMPTY LINE
                    continue

                if line == "REC$$":  # END OF PRODUCT RECORD
                    '''
                    There are cases where specifcation variables are not present hence making a check
                    '''
                    if specification_key !="":
                        entry_dict["specification"] = specification_key[:-2] # remove last two :: characters
                    if crumb != "":
                        entry_dict["crumb"] = crumb[:-1]
                    if crumb_id != "":
                        entry_dict["crumb_id"] = crumb_id[:-1]
                    
                    if rf_string != "":
                            #  Type:jacket,Container Size:4,Composition:widget
                            # split it at , amd :
                        rf_string_pair_arr = rf_string[:-1].split("^")
            
                        for pair in rf_string_pair_arr:
                            rf_key,rf_val = pair.split("$|$")
                            entry_dict[rf_key]=rf_val

                        del rf_string_pair_arr
                    output_file.write("{}\t{}\n".format(
                        prod_key, json.dumps(entry_dict)))

                    # CLEARING VARIABLES FOR NEXT RECORD
                    
                    prod_key = ""
                    specification_key = ""
                    crumb = ""
                    crumb_id = ""
                    rf_string=''
                    entry_dict.clear()
                    
                    
                else:

                    record_row_key = line.split("=", 1)[0]  # SPLITS AT FIRST =
                    record_row_value = line.split("=", 1)[1]

                    if record_row_key is "" or "_OV" in record_row_key or "_SV" in record_row_key:
                        
                        continue  # CASE WHERE THE VARIABLE IS EMPTY  OR CONTAINS _OV OR _SV -> case sensitive seach

                    if record_row_key == "part":
                        # HERE WE HAVE THE PRODUCT ID
                        prod_key = "{}".format(record_row_value)

                    else:
                        # CHECK FOR THE SPEC STRING

                        # if "_N" in record_row_key and "at":  # KEY
                        if re.search("^at[0-9]+_N", record_row_key) != None:
                            logging.info("SPECIFICATION ARRAY : {} -> {}".format(record_row_key,record_row_value))
                            specification_key += record_row_value.strip() + "|"
                            continue

                        # elif "_V" in record_row_key:  # VALUE
                        elif re.search("^at[0-9]+_V", record_row_key) != None:
                            logging.info("SPECIFICATION ARRAY : {} -> {}".format(record_row_key,record_row_value))
                            specification_key += record_row_value.strip() + "::"
                            continue

                        if re.search("^rf[0-9]+_N", record_row_key) != None:
                        
                            rf_string+=record_row_value+"$|$"
                            continue
                            
                        elif re.search("^rf[0-9]+_V", record_row_key) != None:
                            
                            rf_string+=record_row_value+"^"
                            continue
                            
                        if "cat" in record_row_key: # TO  SAVE MULTIPLE CHECKS

                            if re.search("^cat[0-9]+_img", record_row_key) != None or "PrntID" in record_row_key:
                                continue
                            
                            if re.search("^cat[0-9]+_N", record_row_key) != None:
                                crumb += record_row_value.strip() + "|"
                                continue
                            elif re.search("^cat[0-9]+_ID", record_row_key) != None:
                            
                                crumb_id += record_row_value.strip() + "|"
                                continue
                            
                            

                        if record_row_key in entry_dict:
                            entry_dict[record_row_key] = entry_dict[record_row_key] + \
                                "|" + record_row_value  # CONCAT DUPLICATE VALUES
                        #    logging.debug("Duplicate {} -> Value:{}".format(record_row_key,entry_dict[record_row_key]))
                        else:
                            entry_dict[record_row_key] = record_row_value

            except:
                logging.error("{}:{} -> LINE {} ".format(
                    time.time(), Exception.with_traceback, line))
        input_file.close()
    except AttributeError:
        logging.error("EXCEPTION ON : {}".format(AttributeError))
    except TypeError:
        logging.error("Type error-> {}".format(TypeError))

    return

# THIS IS FOR THE ItemRestrictions.txt AND LiveCad4Build.txt

def key_value_item_files(file_name, separator, seconday_key):

    record_file_dict = dict()
    input_file_item = open("./items/"+file_name,"r")
    output_file_item = open(file_name,"w")

    # with open("./items/"+file_name, "r") as input_file_item:

    for line in input_file_item:
        key, val = line.split(separator)
        val = val.replace("\n", "")

        if key not in record_file_dict:
            record_file_dict[key] = val.strip()
        else:
            record_file_dict[key] = record_file_dict[key]+"|"+val.strip()

    # with open(file_name, "w") as output_file_item:
    for key, val in record_file_dict.items():

        if key == "ItemNumber" or key == "part":
            continue    # HEADING SECTION
        out_string = key + "\t{\""+seconday_key+"\": \"" + val.strip() + "\"}\n"
        output_file_item.write(out_string)

    output_file_item.close()
    input_file_item.close()
    return

def aggregated_line_files(files_array, line_file_name):

    aggregated_line_output = open(line_file_name,"w")

    for file_ in files_array:
        print("File started:{}\t{}".format(time.ctime(), file_))

        # file_ = "./items/"+file_
        record_creator(file_, aggregated_line_output)

    aggregated_line_output.close()
    return

def nexla_file_generation():

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
    return

def main():

    operation_type = sys.argv[1]
    SOURCE_FILES = [sys.argv[value] for value in range(2,len(sys.argv))]

    if operation_type == "alternate":
        aggregated_line_files(SOURCE_FILES, "attribute.txt")

    elif operation_type == "product":
        aggregated_line_files(SOURCE_FILES, "prod.txt")
    elif operation_type == "baseline":
        aggregated_line_files(SOURCE_FILES, "base.txt")


    elif operation_type == "other":
        key_value_item_files("ItemRestrictions.txt", "|", "RestrictionGroup")
        key_value_item_files("LiveCad4Build.txt", ",", "hasLiveCADDrawing")
    
    elif operation_type == "postprocess":
        nexla_file_generation()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    # print("TOTAL EXECUTION:{} sec".format(end-start,))
