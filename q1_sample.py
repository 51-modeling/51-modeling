"""
Samples for question 1.

Samples for question 1 including a terminal print and a chart revealing the
corresponding optimal pool size given by the model under different prevalence.
"""

from optimal import opts
import numpy as np
import matplotlib.pyplot as plt

# Sample of the case which rho=.05, tpr=.95, tnr=.99
rho,tpr,tnr=0.05,0.95,0.99
opt_x,opt_s=(opts(rho,tpr,tnr))
print("示例 ("+"rho="+str(rho)+", TPR="+str(tpr)+", TNR="+str(tnr)+"):")
print("\t最佳混检池大小 = "+str(opt_x))
print("\t相应评分 = "+str(opt_s))

# Plot optimal pool size for different prevalence
rho=np.arange(0,0.1,0.0001)
tpr,tnr=0.95,0.99
x=[]
y=[]
for i in rho:
    x.append(opts(i,tpr,tnr)[0])
    y.append(opts(i,tpr,tnr)[1])
plt.plot(rho,x)
plt.title("Optimal pool size under different prevalence\n(TPR="+str(tpr)+", TNR="+str(tnr)+")")
plt.xlabel("Prevalence")
plt.ylabel("Optimal pool size")
plt.savefig("model2_sample.png")