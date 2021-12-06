import os

cascades = "movielens-cascades2.txt"
n = 6
name_output = "movielens-inferred-network-{0}".format(n)
max_iter = 20000
model = 2 #0:exponential, 1:powerlaw, 2:rayleigh
expo = -12
alpha = 1*10**(expo) #default:1

#Execute netinf algorithm
command = "./netinf -i:{0} -o:{1} -m:{2} -e:{3} -a:{4}".format(cascades, name_output, str(model), str(max_iter), str(alpha))
os.system(command)
