"""
Sample for Q3

Plot the optimal pooling strategy for actual and predicted cases, Manhattan
only as sample.
"""

# Parameters
tpr,tnr=0.95,0.99

from optimal import opts
import pandas as pd
import matplotlib.pyplot as plt

# Calculate the optimal pooling strategy
def calc_opt(tpr, tnr, pvl):
    """
    Calculate the optimal pooling strategy.

    Args:
        tpr: True positive rate (aka. sensitivity, P{TP}/(P{TP}+P{FN})) of the
             test
        tnr: True negative rate (aka. specificity, P{TN}/(P{TN}+P{FP})) of the
             test
        pvl: Prevalence of the virus in the sample

    Returns:
        A tuple of int consisting optimal pool size and its score.
    """
    opt_x=[]
    for i in range(days):
        opt_x.append(0)
        opt_x[i],trash=opts(pvl[i]/100,tpr,tnr)
    return opt_x

# Load data
df=pd.read_csv("nyc_prevalence.csv")
date=df.iloc[:,0].values
days=date.shape[0]
pvl=df.iloc[:,3].values.tolist() # Only Manhattan, actual prevalence
df_=pd.read_csv("undetective.csv")
pvl_pred=df_.iloc[:,3].values.tolist() # Only Manhattan, predicted prevalence

# Calculate the optimal pooling strategy
opt_x= calc_opt(tpr, tnr, pvl)
opt_x_pred = calc_opt(tpr, tnr, pvl_pred)

# Plot
plt.plot(range(days),opt_x,c='r',label='Actual')
plt.plot(range(days),opt_x_pred,c='b',label='Predicted')
plt.title("Manhattan optimal pool size")
plt.xlabel("days since 2022/1/26")
plt.ylabel("optimal pool size")
plt.legend()
plt.savefig("plot/q3.png")
plt.clf()