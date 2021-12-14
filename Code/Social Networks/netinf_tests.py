import os

cascades = "movielens-cascades2.txt"
num_model = 6
name_output = "movielens-inferred-network-{0}".format(num_model)
max_iter = 200000
model = 1 #0:exponential, 1:powerlaw, 2:rayleigh
expo = -5
alpha = 7.5#1*10**(expo) #default:1

#Execute netinf algorithm
command = "./netinf -i:{0} -o:{1} -m:{2} -e:{3} -a:{4}".format(cascades, name_output, str(model), str(max_iter), str(alpha))
os.system(command)
