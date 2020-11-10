import time
import logging
import os
import json

LOG_FILENAME = 'debug.log'
WORKING_DIR = os.getcwd()
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

PART_ID_ARR = []
# SOURCE_FILES_ATTRIBUTE = ["IT_Alternate.TXT","IT_Alternate1.TXT","IT_Alternate2.TXT","IT_Alternate3.TXT","IT_Alternate4.TXT"]
# SOURCE_FILES_PRODUCT = ["IT_Product1.TXT","IT_Product2.TXT","IT_Product3.TXT","IT_Product4.TXT","IT_Product5.TXT","IT_Product6.TXT"]
SOURCE_FILES_ATTRIBUTE = ["IT_Alternate.TXT","IT_Alternate1.TXT"]
SOURCE_FILES_PRODUCT = ["IT_Product1.TXT","IT_Product2.TXT"]

def record_creator(file_,output_file):
    entry_dict = dict()
    prod_key = ''
    with open(file_, "r", errors='replace') as input_file:

        # IT WILL READ LINE BY LINE
        # HAVEN'T USED READLINE() TO AVAOID LOADING ENTIRE LIST IN RAM TO SAVE MEMORY

        for line in input_file:
            try:
                line = line.replace("\n", "")

                if line == "":  # EMPTY LINE
                    continue    

                if line == "REC$$": # END OF PRODUCT RECORD
                    output_file.write("{}\t{}\n".format(prod_key, json.dumps(entry_dict)))
                    # entry_dict = {}
                    entry_dict.clear()
                    prod_key = ""

                else:
                    record_row_key = line.split("=",1)[0]
                    record_row_value = line.split("=",1)[1]
                    if record_row_key is "":
                        print("Issue encountered")
                        continue

                    if record_row_key == "part":
                        prod_key = "{}".format(record_row_value)
                        PART_ID_ARR.append(prod_key)
                    else:
                        if record_row_key in entry_dict:
                            entry_dict[record_row_key] = entry_dict[record_row_key]+"|" + record_row_value
                        #    logging.debug("Duplicate {} -> Value:{}".format(record_row_key,entry_dict[record_row_key]))
                        else:
                            # CHECK FOR THE RF VALUES

                            entry_dict[record_row_key] = record_row_value

            except:
                logging.debug("{}:{}".format(
                    time.time(), Exception.with_traceback))
                print(line)

# THIS IS FOR THE ItemRestrictions.txt AND LiveCad4Build.txt
def key_value_item_files(file_name,separator,seconday_key):

    record_file_dict = dict()
    with open(WORKING_DIR+"/items/"+file_name,"r") as input_file_item:

        for line in input_file_item:
            key,val = line.split(separator)
            val = val.replace("\n","")
            
            if key not in record_file_dict:
                record_file_dict[key]=val
            else:
                record_file_dict[key]= record_file_dict[key]+"|"+val

    with open(WORKING_DIR+"/output/"+file_name,"w") as output_file_item:
        for key,val in record_file_dict.items():
           
            if key == "ItemNumber" or key == "part":
                # skip heading
                continue
            out_string = key +"\t{\""+seconday_key+"\": \"" + val+ "\"}\n"
            output_file_item.write(out_string)  
    sort_file(file_name)
    return

def sort_file(line_file_name):
    sort_string= "sort "+WORKING_DIR+"/output/"+line_file_name+ " -o "+WORKING_DIR+"/output/"+line_file_name
    os.system(sort_string)

def merge_master_line():
    os.chdir(WORKING_DIR+"/output/")
    # MADE LEFT OUTER JOIN
    merge_string = "join -a1 prod.txt attribute.txt |sed 's/} {/, /' > merge_file.txt"
    os.system(merge_string)

def aggregated_line_files(files_array, line_file_name):
    
    with open(WORKING_DIR+"/output/" + line_file_name, "w") as output_file:

            for file_ in files_array:
                print("File started:{}\t{}".format(time.ctime(),file_))

                file_ = WORKING_DIR+"/items/"+file_   
                record_creator(file_,output_file)

    sort_file(line_file_name)

def final_merge():
    print("Merge and Sort Started in at {}".format(time.ctime()))
    os.chdir(WORKING_DIR+"/output/")
    os.system("cat prod.txt attribute.txt LiveCad4Build.txt ItemRestrictions.txt| sort > merge_line.txt")
    print("Merge and Sort Completed in at {}\n----------".format(time.ctime()))


def post_merge():
    print("Final Record Creation started {}\n".format(time.ctime()))
    os.chdir(WORKING_DIR+"/output/")
    final_outputfile =  open("merge_line_unique.json","w") 
    final_outputfile.write("[\n")
    with open("merge_line.txt","r") as input_merge:

        temp_string = ""
        older_key = ''
        for count,line in enumerate(input_merge):
            key,val = line.split("\t")         
            if count == 0:
                older_key = key

            if key == older_key:
                temp_string=(temp_string+val.replace("\n","")).replace("}{",", ")          
            else:
                # final_outputfile.write("{}\t{}\n".format(older_key,temp_string)) 
                x = '"op":"add", "path": "/products/pid-{}", "attributes": {}'
                if line != '':
                    # NEED TO ADD SOMETHING TO HANDLE THE LAST ,
                    final_outputfile.write("{ "+x.format(older_key,temp_string)+"},\n") 
                else:
                    final_outputfile.write("{ "+x.format(older_key,temp_string)+"}\n") 
                temp_string=val.replace("\n","")
                older_key = key
        final_outputfile.write("\n]")

def main():
    print("File Aggregation Started in at {}".format(time.ctime()))
    aggregated_line_files(SOURCE_FILES_ATTRIBUTE,"attribute.txt")
    aggregated_line_files(SOURCE_FILES_PRODUCT,"prod.txt")
    key_value_item_files("ItemRestrictions.txt","|","RestrictionGroup")
    key_value_item_files("LiveCad4Build.txt",",","hasLiveCADDrawing")
    print("File Aggregation Completed in at {}\n----------".format(time.ctime()))
    # Aggregated file creation completed
    # merge_master_line()
    final_merge()
    post_merge()
    pass
    
if __name__ == "__main__":
    start = time.time() 
    main()
    end = time.time()
    print("TOTAL EXECUTION:{} sec".format(end-start,))

