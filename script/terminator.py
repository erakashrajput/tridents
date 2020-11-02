import time
import logging
import os

LOG_FILENAME = 'debug.log'
WORKING_DIR = os.getcwd()
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

PART_ID_ARR = []
SOURCE_FILES_ATTRIBUTE = ["IT_Alternate.TXT","IT_Alternate1.TXT"]
SOURCE_FILES_PRODUCT = ["IT_Product1.TXT","IT_Product2.TXT"]

# def Repeat(x): 
    # _size = len(x) 
    # repeated = [] 
    # for i in range(_size): 
    #     k = i + 1
    #     for j in range(k, _size): 
    #         if x[i] == x[j] and x[i] not in repeated: 
    #             repeated.append(x[i]) 
    # return repeated 
  
def json_validator(key,val):
    pass
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
                    output_file.write("{}\t{}\n".format(prod_key, entry_dict))
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
                            "|" + record_row_value
                        #    logging.debug("Duplicate {} -> Value:{}".format(record_row_key,entry_dict[record_row_key]))
                        else:
                            entry_dict[record_row_key] = record_row_value

            except:
                logging.debug("{}:{}".format(
                    time.time(), Exception.with_traceback))

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
                file_ = WORKING_DIR+"/items/"+file_   
                record_creator(file_,output_file)
    sort_file(line_file_name)

def main():
    # aggregated_line_files(SOURCE_FILES_ATTRIBUTE,"attribute.txt")
    # aggregated_line_files(SOURCE_FILES_PRODUCT,"prod.txt")
    merge_master_line()
    pass
    
if __name__ == "__main__":
    start = time.time() 
    main()
    end = time.time()
    print("Time:{}".format(end-start))

'''
1. created line file for attri - sorted
2. same for prod - sorted
3. we will make a join on first
'''