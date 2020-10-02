####################################
#!/usr/bin/python
#	Filename        : PypeCore.py
#	Author          : Jihyun Nam		
#	Version         : 0.4
#   Python Version  : 2.7.x
####################################

import readline
import json
import os
import csv
import OpenImageIO as oiio

class Completer(object):  
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  
            if text:  
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  
                self.matches = self.options[:]

        try: 
            return self.matches[state]
        except IndexError:
            return None

    def parser(self):
        completer = Completer(self.options)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')   

class JsonIO(object):  
    def __init__(self, json_file):     
        self.initFile(json_file)
        self.json_file = json_file
        self.project_db = self.loadJSON(json_file)
    
    def loadJSON(self, json_file):
        with open(json_file) as data_file:
            data = json.load(data_file)
            #data = [s.encode('utf-8') for s in data_file]        
        return data
    
    def dumpJSON(self, json_file, dic_data):
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

class Foo: # Property Sample Class
	"""docstring for Foo"""
	def __init__(self):
		self._age = 0

	@property
	def age(self):
		return self._age

	@age.setter
	def age(self, value)		:
		self._age = value            

class FileChecker(object):
    def __init__(self):
        pass
    def integrity(self, filename):
        input = oiio.ImageInput.open(filename)
        spec = input.spec()
        if spec.tile_width == 0 :
            for y in range(spec.y, spec.y+spec.height) :
                pixels = input.read_scanline (y, spec.z, oiio.UNKNOWN)
                if pixels == None :
                    #print "Broken at scanline " + str(y)
                    #print "geterr = " + input.geterror()
                    return False
                    break                   
                else:
                    return True        


class setDB():
 
    def __init__(self):
        if platform.system() == "Windows":

            self.sesi_path = self.getEnv("SESI")
            self.htoa_path = self.getEnv("HTOA")            
            
##            try:
##                self.sesi_path = os.environ["SESI"]
##            except KeyError:
##                print "{}{}".format("Variable ", "SESI is not defined")
##                
##            try:
##                self.htoa_path = os.environ["HTOA"]
##            except KeyError:
##                print "{}{}".format("Variable ", "HTOA is not defined")

                                        
            
    @property
    def hou(self):
        versions = self.collectVer(self.sesi_path)
        foo_db = self.getHouMinor(versions)
        return foo_db

    @property
    def htoa(self):
        return self.htoa_path.split("-")[-1]
    
    
    def check_essential_env(self, sesi_path, htoa_path):
        if sesi_path == None:
            print("\n/// User env variable 'SESI' is not defined ///\n")
            time.sleep(-1)
        if htoa_path == None:
            print("\n/// User env variable 'HTOA' is not defined ///\n")
            time.sleep(-1)

    def getEnv(self, ENV_VAR):
        try:
            return os.environ[ENV_VAR]
        except KeyError:
            print( "{} {} {}".format("Variable", ENV_VAR, "is not defined"))

    
    def collectVer(self, sesi_path):
        self.dirs = os.listdir(sesi_path)
        self.versions = []
        for x in self.dirs:
            self.versions.append(x.split(" ")[-1])
        return self.versions


##    def getHouMajor(self, versions):
##        self.majors = []
##        for x in versions:
##            if x[:4] not in self.majors:
##                self.majors.append(x[:4])
##        return self.majors

    
    def getHouMinor(self, versions):
        majors = []
        for x in versions:
            if x[:4] not in majors:
                majors.append(x[:4])       

        temp_dic = {}
        for x in majors:
            self.minors = []
            for y in versions:
                if x in y:
                    self.minors.append(y.split(".")[2])
            temp_dic[x] = self.minors
        return temp_dic

class Globals():
    """docstring for Envs"""
    def __init__(self, job_dir, prj, node, node_ver, hip_ver, asset, sim, render):
        super(Globals, self).__init__()
        self.job_dir = job_dir 
        self.prj      = prj
        self.node     = node
        self.nver     = node_ver
        self.hver     = hip_ver
        self.asset    = asset
        self.sim      = sim
        self.render   = render

    
    def saveHip(self):   

        path = "{}{}/{}/{}/hip/".format(self.job_dir 
                                ,self.prj
                                ,self.node
                                ,self.nver)
                                
        filename = "{}_{}_v{}.hip".format(self.prj
                                         ,self.node
                                         ,self.hver)

        if not os.path.isdir(path):
            os.makedirs(path)

        hou.hipFile.save(path + filename)
        
        #set JOB environment var
        #hou.hscript("setenv JOB=%s/%s/%s" %(job_dir,prj,node))

        hou.hscript("setenv JOB=%s" %(self.job_dir + self.prj +"/"))    
        hou.hscript("setenv VER=%s" %(self.nver))  


    def loadHip(self):
        path = "{}{}/{}/{}/hip/".format(self.job_dir 
                                ,self.prj
                                ,self.node
                                ,self.nver)
                                
        filename = "{}_{}_v{}.hip".format(self.prj
                                        ,self.node
                                        ,self.hver)

        hou.hipFile.load(path + filename)


    def buildDirs(self):

        dir_list = ["geo", "hda", "sim", "abc", "render", "scripts"]    
        
        for i in dir_list:                 
            foo = "label_" + i       
            dir = str(self.job_dir + self.prj + '/' + i + "/")        
            if hou.node(".").parm(foo).eval() == 1:
                os.makedirs(dir)
            else:
                pass


    def setEnv(self):
        job_dir = hou.node(".").evalParm("job_dir")
        prj = hou.node(".").evalParm("prj")
        
        #set JOB environment var
        hou.hscript("setenv JOB=%s/%s" %(self.job_dir, self.prj))
        
        display = "JOB variable set: " + str(self.job_dir + "/" + self.prj)
        hou.ui.displayMessage(display)


    def upver(self):        
        current_ver = int(self.nver)
        hou.node(".").parm("version").set(str(current_ver + 1).zfill(4))


    def setfrange(self):
        pass        


    def setEnvVar(self):   

        build_env_dirs()
               
        #set JOB environment var
        hou.hscript("setenv NODE=%s" %(self.prj))
        hou.hscript("setenv ASSET=%s" %(self.asset))
        hou.hscript("setenv SIM=%s" %(self.sim))
        hou.hscript("setenv RENDER=%s" %(self.render))
        hou.hscript("setenv VER=%s" %(self.nver))       


    def build_env_dirs(self):
        job_dir = hou.getenv("HIP")    

        dir_list = ["Asset", "Sim", "Render"]

        for i in dir_list:           
            dir = str(job_dir +"/"+i)
            if not os.path.isdir(dir):
                os.makedirs(dir)

        temp_dir = hou.getenv("JOB") 
        
        if not os.path.isdir(temp_dir):
            os.makedirs("script")                           