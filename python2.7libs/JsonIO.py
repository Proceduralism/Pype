####################################
#!/usr/bin/python
#   Filename        : JsonIO.py
#   Author          : Jihyun Nam        
#   Version         : 0.5
#   Python Version  : 2.7.x
####################################
import os, json

class JsonIO(object):  
    def __init__(self, json_file):     
        self.initFile(json_file)
        self.json_file = json_file
        self.project_db = self.loadJSON(json_file)
    
    def loadJson(self, json_file):
        with open(json_file) as data_file:
            data = json.load(data_file)
            #data = [s.encode('utf-8') for s in data_file]        
        return data
    
    def dumpJson(self, json_file, dic_data):
        with open(json_file, 'w') as filename:
            json.dump(dic_data, filename, sort_keys=True, indent=4) 
    
    def initFile(self, filename):  
        if os.path.exists(filename):
            pass
        else:
            f = open(filename, "w")
            f.write("{}")
            f.close()
        
    def addItems(self, key, item):
        database = self.project_db
        database[key] = item
        self.dumpJSON(self.json_file, database)
    
    def readCSV(csv_file): 
            with open(csv_file, 'r') as f:
            	movieList = [line.strip() for line in f]         	
            readData = {}
            for x in movieList:
                key = x.split(",")[0]
                value = x.split(",")[-4:]
                readData[key] = value
            return readData


video_db = "video_db.json"
temp_db ={"labs::spiral":"www.google.com"}
jsonio = JsonIO(video_db)

db = {"Globals":"http://www.google.com"
		,"Geomtry":"http://www.google.com"
		,"File":"http://www.google.com"
      ,"labs::spiral":"http://www.google.com"
		}