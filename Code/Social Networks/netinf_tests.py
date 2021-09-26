import os

cascades = "movielens-cascades2.txt"
name_output = "movielens2"
edges = 205412
model = 0
alpha = 1*10**(-8) #default:1

#Clean previous executions
#os.system("make clean")
os.system("rm {0}.txt".format(name_output))
os.system("rm {0}-edge.info".format(name_output))

#Build netinf algorithm
#os.system("make all")

#Execute netinf algorithm
command = "./netinf -i:{0} -o:{1} -m:{2} -e:{3} -a:{4}".format(cascades, name_output, str(model), str(edges), str(alpha))
os.system(command)
