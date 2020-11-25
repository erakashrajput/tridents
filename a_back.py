import time
import sys
import re
import json
import logging
from datetime import date

today = str(date.today())
LOG_FILENAME = "stats-{}.log".format(today)

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=FORMAT)

# BASE RECORD  GENERATOR
def record_creator(file_, output_file):

    entry_dict = dict()
    specification_key = ''
    crumbs = ''
    crumbs_id = ''
    rf_string = ''
    prod_key = ''

    try:
        
        input_file = open(file_, "r")

        for line_count, line in enumerate(input_file):
            try:

                line = line.replace("\n", "").replace("\r", "") # REMOVEING \n AND\r from line read, IF python3 IS USED ONLY \n NEEDS TO BE REMOVED

                if line == "":  # SKIPPING EMPTY LINES
                    continue

                if line == "REC$$":  # END OF PRODUCT RECORD -> REC$$ IS THE IDENTIFIER
                    
                    # THERE ARE CASES WHERE SPECIFCATION/crumbs/crumbs_ID VARIABLES ARE NOT PRESENT HENCE MAKING A CHECK
                    if specification_key != "":
                        # REMOVE LAST TWO :: CHARACTERS
                        entry_dict["specification"] = specification_key[:-2]

                    if crumbs != "":
                        # REMOVE LAST '|' CHARACTER
                        entry_dict["crumbs"] = crumbs[:-1]

                    if crumbs_id != "":
                        # REMOVE LAST '|' CHARACTER
                        entry_dict["crumbs_id"] = crumbs_id[:-1]

                    if rf_string != "":
                        # Type:jacket,Container Size:4,Composition:widget
                        # SPLIT AT ^ amd AND '$|$' -> REASON: THESE NEW SPECIAL CHARACTERS ARE ADDED BECAUSE OF THE DATA QUALITY AND ALL COMMON CHARACTER WERE PRSENT IN THE VALUES
                        rf_string_pair_arr = rf_string[:-1].split("^")

                        for pair in rf_string_pair_arr:
                            rf_key, rf_val = pair.split("$|$")
                            entry_dict[rf_key] = rf_val

                        del rf_string_pair_arr
                    output_file.write("{}\t{}\n".format(
                        prod_key, json.dumps(entry_dict)))

                    # CLEARING VARIABLES FOR NEXT RECORD

                    prod_key = ""
                    specification_key = ""
                    crumbs = ""
                    crumbs_id = ""
                    rf_string = ''
                    entry_dict.clear()

                else:

                    # SPLITS AT FIRST '=' 
                    try:
                        record_row_key = line.split("=", 1)[0]  
                        record_row_value = line.split("=", 1)[1]

                    except AttributeError:
                        print(prod_key)
                        logging.cretical("{} -> {}".format(record_row_key,record_row_value))
                    

                    if record_row_key is "" or "_OV" in record_row_key or "_SV" in record_row_key:
                        continue  # CASE WHERE THE VARIABLE IS EMPTY  OR CONTAINS _OV OR _SV -> case sensitive seach

                    if record_row_key == "part":
                        # PRODUCT ID ASSIGNMENT
                        prod_key = "{}".format(record_row_value)

                    else:
                        # CHECK FOR THE SPECIFICATION STRING
                        if re.search("^at[0-9]+_N", record_row_key) != None:
                            specification_key += record_row_value.strip() + "|"
                            continue

                        elif re.search("^at[0-9]+_V", record_row_key) != None:
                            specification_key += record_row_value.strip() + "::"
                            continue

                        if re.search("^rf[0-9]+_N", record_row_key) != None:
                            rf_string += record_row_value+"$|$"
                            continue

                        elif re.search("^rf[0-9]+_V", record_row_key) != None:
                            rf_string += record_row_value+"^"
                            continue

                        # CHECK FOR crumbs AND crumbs_ID
                        if "cat" in record_row_key:  # TO SAVE MULTIPLE CHECKS

                            if re.search("^cat[0-9]+_img", record_row_key) != None or "PrntID" in record_row_key:
                                continue    # CASE WHERE THE VARIABLE CONTAINS _img OR PrntID -> case sensitive seach

                            if re.search("^cat[0-9]+_N", record_row_key) != None:
                                crumbs += record_row_value.strip() + "|"
                                continue

                            elif re.search("^cat[0-9]+_ID", record_row_key) != None:
                                crumbs_id += record_row_value.strip() + "|"
                                continue

                        # CONCAT FOR DUPLICATE VALUES AND APPEND THE VALUES WITH |
                        if record_row_key in entry_dict:
                            entry_dict[record_row_key] = entry_dict[record_row_key] + \
                                "|" + record_row_value  

                        # IDEAL RECORD
                        else:
                            entry_dict[record_row_key] = record_row_value

            except:
                logging.error("{}:{} -> {} ->LINE {} ".format(
                    time.time(), Exception.with_traceback, line_count, line))
        
        input_file.close()
    except AttributeError as atr:
        logging.error("AttributeError: {}".format(AttributeError))
    except TypeError:
        logging.error("CRETICAL:TypeError-> {}".format(TypeError))

    return


# FOR THE ItemRestrictions.txt AND LiveCad4Build.txt RECORD GENERATION
def key_value_other_files(file_name, separator, seconday_key):

    try:
        record_file_dict = dict()
        input_file_item = open("./items/"+file_name, "r")
        output_file_item = open(file_name, "w")
        logging.info("Process File: {}".format("./items/{}".format(file_name)))
        for line in input_file_item:
            key, val = line.split(separator)
            val = val.replace("\n", "")

            if key not in record_file_dict:
                record_file_dict[key] = val.strip()
            else:
                record_file_dict[key] = record_file_dict[key]+"|"+val.strip()

        for key, val in record_file_dict.items():

            if key == "ItemNumber" or key == "part":
                continue    # HEADING SECTION
            out_string = key + "\t{\""+seconday_key + \
                "\": \"" + val.strip() + "\"}\n"

            output_file_item.write(out_string)

        output_file_item.close()
        input_file_item.close()
        
        logging.info("Output File: {}".format(file_name))
    except Exception as e:
        logging.error(e.args.items())
    

def aggregate_line_files(files_array, line_file_name):

    aggregated_line_output = open(line_file_name, "w")
    logging.info("Process Files: {}".format(files_array))
    for file_ in files_array:
        
        record_creator(file_, aggregated_line_output)

    aggregated_line_output.close()
    logging.info("Output File: {}".format(line_file_name))


def nexla_file_generation():
    try:
        final_outputfile_jsonline = open(
            "NX_MSCDIRECT_PROD_{}.jsonl".format(today), "w")           
        merge_line_input_file = open("merge_line.txt", "r")
        older_key = ''
        record_value = json.loads('{"test":"value"}')
        record_dict = dict()
        line =''
        older_key = ''
        key = ''
        for count, line in enumerate(merge_line_input_file):
            try:
                key, val = line.split("\t")
                if count == 0:
                    older_key = key

                if older_key != key:
                    if "sellingPrice" in record_dict:
                        record_dict["price"] = record_dict["sellingPrice"]
                        del record_dict["sellingPrice"]
                    if "webDesc" in record_dict:
                        record_dict['title'] = record_dict["webDesc"]
                        del record_dict["webDesc"]
                    if "img" in record_dict:
                        record_dict["thumb_image"] = "https://cdn.mscdirect.com/global/images/ProductImages/"+record_dict["img"]+".jpg"
                        del record_dict["img"]
                    record_dict["availibility"] = "true"
                    crumbs = ''
                    if "crumbs_id" in record_dict and "crumbs" in record_dict:
                        cid = record_dict["crumbs_id"].split("|")
                        cn = record_dict["crumbs"].split("|")
                        crumbs = "[["
                        for i in range(0,len(cid)):
                            if i > 0:
                                crumbs= crumbs+","
                            crumbs = crumbs+'{'+'"id":"'+cid[i]+'","name":"'+cn[i]+'"}'
                        crumbs = crumbs+"]]"
                    value = json.loads("{}")
                    value["attributes"] = json.loads(json.dumps(record_dict))
                    if crumbs!='':
                        value["category_paths"] = json.loads(crumbs)
                    record_value = json.loads('{"op":"add", "path": "/products/'+older_key+'"}')
                    record_value["value"] = value
                    final_outputfile_jsonline.write(json.dumps(record_value)+"\n")
                    older_key = key
                    older_key = key
                j1 = json.loads(val)
                for k,v in j1.items():
                    record_dict[k] = v
            except:
                logging.info("==>> Line Exception {}:  PID: {}".format(line,key))
        # CLOSE THE STREAMS
        merge_line_input_file.close()
        final_outputfile_jsonline.close()
    except IOError as e:
        logging.info("Unable to find merge_line.txt")
    except Exception as exp:
        logging.info("ERROR while creating record")


def main():

    # VALUES: baseline,other and postprocess
    operation_type = sys.argv[1]

    # IT'S ADDED TO HANDLE A CASE IN WHICH WE WOULD REQUEST FROM MULTIPLE SOURCE FILES
    '''
    INTIAL LOGIC WAS THERE TO CREATE ALTERNATE.TXT AND PRODUCT.TXT AND THEN MERGE THEM
    '''
    SOURCE_FILES = [sys.argv[value] for value in range(2, len(sys.argv))]

    if operation_type == "alternate":
        aggregate_line_files(SOURCE_FILES, "attribute.txt")

    elif operation_type == "product":
        aggregate_line_files(SOURCE_FILES, "prod.txt")

    # CREATES BASE.TXT. FORMAT -> PRODUCT ID \T {OBJECT}
    elif operation_type == "baseline":
        aggregate_line_files(SOURCE_FILES, "base.txt")

    # CREATES INDIVIDUAL FILES. FORMAT -> PRODUCT ID \T {OBJECT}
    elif operation_type == "other":
        key_value_other_files("ItemRestrictions.txt", "|", "RestrictionGroup")
        key_value_other_files("LiveCad4Build.txt", ",", "hasLiveCADDrawing")

    # CREATE NEXLA SUPPORTED FORMAT BY CONSUMING MERGE_LINE.TXT
    elif operation_type == "postprocess":
        nexla_file_generation()

    else:
        logging.error("ERROR: Incorrect operation_type IN THE REQUEST")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Execution Time:{} sec\n".format(end-start))


