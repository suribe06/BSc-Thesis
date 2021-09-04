import os

cascades = "example-cascades.txt"
name_output = "example"
edges = 100
alpha = 1 #default:1

#Clean previous executions
#os.system("make clean")
os.system("rm {0}.txt".format(name_output))
os.system("rm {0}-edge.info".format(name_output))

#Build netinf algorithm
#os.system("make all")

#Execute netinf algorithm
command = "./netinf -i:{0} -o:{1} -e:{2} -a:{3}".format(cascades, name_output, str(edges), str(alpha))
os.system(command)
