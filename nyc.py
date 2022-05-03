"""
Optimal pooling strategy for NYC.

Given the prevalence data of New York, NY, give an optimal pooling Covid PCR
test strategy with the model constructed.
"""

# Parameters
tpr,tnr=0.95,0.99

from optimal import opts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def graph_plot(data,region,type):
    """
    Plot the data.

    Plot the given data and save to ./plot/*.png.

    Args:
        data: np.1darray, the data to be plotted.
        region: str, the region name.
        type: str, "pool" or "test". The type of the data.

    Returns:
        0. -1 if type is not "pool" or "test".
    """
    plt.plot(range(opt_x.shape[0]),data)
    if(type=="pool"):
        type_str="optimal pool size"
        save_str="_pool_size.png"
    elif(type=="test"):
        type_str="tests required"
        save_str="_tests_to_be_conducted.png"
    else:
        return -1
    plt.title(region+" "+type_str)
    plt.xlabel("days since 2022/1/26")
    plt.ylabel(type_str)
    plt.savefig("plot/"+"nyc_"+region+""+save_str)
    plt.clf()
    return 0

# Load data
df=pd.read_csv("nyc_prevalence.csv")
date=df.iloc[:,0].values
pvl=df.iloc[:,1:6].values
header=df.columns[:6].values
df_pop=pd.read_csv("nyc_population.csv")
pop=df_pop.iloc[177:182,:].values

# Calculate the optimal pooling strategy
opt_x=np.zeros(pvl.shape)
opt_s=np.zeros(pvl.shape)
opt_t=np.zeros(pvl.shape)
for j in range(pvl.shape[1]):
    pop_j=pop[j,1]
    for i in range(pvl.shape[0]):
        opt_x[i,j],opt_s[i,j]=opts(pvl[i,j]/100,tpr,tnr)
        opt_x[i,j]=int(opt_x[i,j])
        opt_t[i,j]=pop_j*opt_s[i,j]
opt_t_sum=np.sum(opt_t,axis=1)

# Plot
for i in range(opt_x.shape[1]):
    graph_plot(opt_x[:,i],header[i+1],'pool')
    graph_plot(opt_t[:,i],header[i+1],'test')
graph_plot(opt_t_sum,"Total",'test')

# Save
opt_x=np.concatenate((date.reshape(date.shape[0],1),opt_x),axis=1)
opt_x=pd.DataFrame(opt_x,columns=header)
opt_x.to_csv("nyc_optimal_pooling.csv",index=False)
opt_t=np.concatenate((date.reshape(date.shape[0],1),opt_t),axis=1)
opt_t=pd.DataFrame(opt_t,columns=header)
opt_t.to_csv("nyc_optimal_test.csv",index=False)