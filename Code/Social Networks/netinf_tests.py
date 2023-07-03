import os

def execute_netinf(cascades, name_output, max_iter, model, alpha):
    """
    Execute NetInf algorithm on cascades data.

    Parameters:
        cascades (str): Path to the cascades data file.
        name_output (str): Name of the output file.
        max_iter (int): Maximum number of iterations for NetInf algorithm.
        model (int): Model selection: 0 for exponential, 1 for power law, 2 for Rayleigh.
        alpha (int): Alpha value for the algorithm.

    Returns:
        None
    """
    # Construct the NetInf command
    command = "./netinf -i:{0} -o:{1} -m:{2} -e:{3} -a:{4}".format(cascades, name_output, str(model), str(max_iter), str(alpha))
    
    # Execute the NetInf algorithm
    os.system(command)

if __name__ == "__main__":
    cascades = "movielens-cascades.txt"
    num_model = 6
    name_output = "movielens-inferred-network-{0}".format(num_model)
    max_iter = 200000
    model = 1 #0:exponential, 1:powerlaw, 2:rayleigh
    expo = -5
    alpha = 11#1*10**(expo) #default:1
    execute_netinf(cascades, name_output, max_iter, model, alpha)