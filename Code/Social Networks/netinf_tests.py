import os

cascades = "movielens-cascades2.txt"
name_output = "movielens-inferred-network"
max_iter = 20000
model = 2 #0:exponential, 1:powerlaw, 2:rayleigh
expo = -12
alpha = 1*10**(expo) #default:1

#Clean previous executions
#os.system("make clean")
os.system("rm {0}.txt".format(name_output))
os.system("rm {0}-edge.info".format(name_output))

#Execute netinf algorithm
command = "./netinf -i:{0} -o:{1} -m:{2} -e:{3} -a:{4}".format(cascades, name_output, str(model), str(max_iter), str(alpha))
os.system(command)
