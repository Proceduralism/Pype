class Globals():
   	"""docstring for Envs"""
	def __init__(self, job_dir, prj, node, node_ver, hip_ver, asset, sim, render):
		super(Globals, self).__init__()
		self.job_dir = job_dir 
		self.prj	  = prj
		self.node     = node
		self.nver     = node_ver
		self.hver     = hip_ver
		self.asset 	  = asset
		self.sim 	  = sim
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