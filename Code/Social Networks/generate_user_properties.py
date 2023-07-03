from snap_sn import netinf_results

models = ['expo', 'pow', 'ray']
for model in models:
    N = 100
    for i in range(N):
        print(f'executing {model} model number {i}')
        input_name = f'inferred_netowrks/inferred-network-{model}-{i}.txt'
        netinf_results(input_name)

#execution time = 8 min 7s