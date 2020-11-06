from pymongo import MongoClient
import os
import json
import time

WORKING_DIR = os.getcwd()


def start_mongodb():
    client = MongoClient('localhost', 27017)
    mydatabase = client["preprocessor"]
    mycollection = mydatabase["mscdirect.myTable"]
    return mycollection

# CREATE NEW RECORD IF IT DOESN'T EXIST
def record_creator(product_id,attribute_value,mongo_connection):

    record_created = {"_id":product_id,"op": "add","path": "/products/"+product_id, "attribute":attribute_value}
    return record_created

# 4 DIFFERENT FILES WILL BE CALL THIS FUNCTION : WE CAN CHOOSE TO DO IT WITH MULTITASK
def read_file(mongo_connection,file_name):

    with open(WORKING_DIR+"/output/"+file_name) as input_file:
        try:
            for line in input_file:
            
                # BREAK THE ROW AT \T IN EACH LINE FILE
                
                pid,value = line.split("\t") 
                value=value.replace("\n","")

                # INTERACT WITH THE DB TO CHECK THE STATUS
                check_record = mongo_connection.find_one({"_id":pid},{"_id":0,"path":1,"attribute":1})
                if check_record != None:
                    # RECORD EXIST
                   
                    existing_attribute = check_record["attribute"].replace("\'","\"") # will update later
                    print("PID: {} =-> Value {} -> existing_attribute ->{} ->exist_pid {} ".format(pid,value,existing_attribute,check_record["path"]))
                    # TO HANDLE EDGE CASE OF DUPLICACY
                    if existing_attribute == value:
                        continue
                    updated_attribute = existing_attribute + value
                    updated_attribute = updated_attribute.replace("}{",", ")
                   
                    # UPDATE THE RECORD IN DB
                    mongo_connection.find_one_and_update({"_id":pid},{"$set":{"attribute":updated_attribute}})
                  
                else:
                    # RECORD DOESN'T EXIST
                    record = record_creator(pid,value,mongo_connection)
                    rec = mongo_connection.insert_one(record)
        except:
            print("Error at line {} : ".format(line))
                
    return

def write_to_master_merge_from_db(mongo_connection):
    cursor = mongo_connection.find({},{"_id":0})
    with open(WORKING_DIR+"/output/master_merge.txt","w") as output_file:
        output_file.write("[")
        for i in cursor:
           output_file.write(str(i)+",\n")
        output_file.write("]")
    return
def clean_db():
     print(mongo_connection.delete_many({}))

def main(mongo_connection):

    file_names = ["prod.txt","attribute1.txt","ItemRestrictions.txt","LiveCad4Build.txt"]
    # file_names = ["prod1.txt","attribute1.txt","ItemRestrictions1.txt","LiveCad4Build1.txt"]

    for file_name in file_names:
        print("reading:{}".format(file_name))
        read_file(mongo_connection, file_name)
        input("next file \n")   
    
    # WRITE TO FILE - completed
    write_to_master_merge_from_db(mongo_connection)
    

if __name__ == "__main__":
    start = time.time() 
    mongo_connection = start_mongodb()
    end = time.time()
    print("Time:{}".format(end-start))
    # main(mongo_connection)
    clean_db()
    