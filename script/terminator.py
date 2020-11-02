import time
import logging

OUTPUT_FILE= "/Users/akash.rajput/Downloads/CUSTOMERS/automated/mscdirect/items/testing/out3.txt"
OUTPUT_FILE1="/Users/akash.rajput/Downloads/CUSTOMERS/automated/mscdirect/items/testing/out2.txt"
INPUT_FILE = "/Users/akash.rajput/Downloads/CUSTOMERS/automated/mscdirect/items/IT_Alternate.TXT"
INPUT_FILE1 = "/Users/akash.rajput/Downloads/CUSTOMERS/automated/mscdirect/items/testing/testing.txt"

LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

PART_ID_ARR = []
# SOURCE_FILES = ["IT_Alternate.TXT ","IT_Alternate1.TXT ","IT_Alternate2.TXT ",
#                 "IT_Alternate3.TXT ","IT_Product1.TXT","IT_Product2.TXT","IT_Product3.TXT","IT_Product4.TXT"]
SOURCE_FILES_TEST = ["IT_Alternate.TXT ","IT_Alternate1.TXT ","IT_Product1.TXT ","_Product2.TXT ",]

def Repeat(x): 
    _size = len(x) 
    repeated = [] 
    for i in range(_size): 
        k = i + 1
        for j in range(k, _size): 
            if x[i] == x[j] and x[i] not in repeated: 
                repeated.append(x[i]) 
    return repeated 
  

def terminator():
    entry_dict = dict()
    prod_key = ''
    with open(INPUT_FILE1, "r", errors='replace') as input_file, open(OUTPUT_FILE1, "w") as output_file:

        # IT WILL READ LINE BY LINE
        # HAVEN'T USED READLINE() TO AVAOID LOADING ENTIRE LIST IN RAM TO SAVE MEMORY

        for line in input_file:
            try:
                line = line.replace("\n", "")

                if line == "":  # EMPTY LINE
                    continue    

                if line == "REC$$": # END OF PRODUCT RECORD
                    output_file.write("{}\t{}\n".format(prod_key, entry_dict))
                    entry_dict = {}
                    prod_key = ""

                else:
                    record_row_key = line.split("=")[0]
                    record_row_value = line.split("=")[1]
                    if record_row_key == "part":
                        prod_key = "{}\t".format(record_row_value)
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

def merge_line_files():
    pass
def main():
    start = time.time()
    terminator()
    end = time.time()
    print(Repeat(PART_ID_ARR))
    print("Time:{}".format(end-start))
    pass


if __name__ == "__main__":
    main()


"""
1. READ FILE -> EXTRACT DATA AND AND CLUB THEM TOGETHER
2. WRTE DATA TO MASTER FILE
3. 

"""