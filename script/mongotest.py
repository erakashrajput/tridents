from pymongo import MongoClient
client = MongoClient('localhost', 27017)
print(client)
mydatabase = client["preprocessor"]
mycollection = mydatabase["mscdirect"]
rec = {"title":"abc","role":"ss"}

# inserting the data in the database
rec = mydatabase.myTable.insert(rec)
# for i in mydatabase.myTable.find({"title":"manager","role":"dev"}):
#     print(i) 