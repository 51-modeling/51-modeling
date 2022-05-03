"""
Obtain optimal pooling strategy.

By scoring and comparing every possible COVID-19 test pooling strategy, find
the best strategy.

Typical using example:
optimal_x,optimal_score=(opts(rho,tpr,tnr))
"""

from cmath import log

def s(x,rho,tpr,tnr,xlb,xrb):
    """
    Scoring the pooling strategy .
    
    Return the expectation of tests to be conducted per person, the smaller the
    better.

    Args:
        x: Pool size
        rho: Prevalence in given sample
        tpr: True positive rate (aka. sensitivity, P{TP}/(P{TP}+P{FN})) of the
             test
        tnr: True negative rate (aka. specificity, P{TN}/(P{TN}+P{FP})) of the
             test
        xlb: Lower bound of the pool size, 2 by default
        xlb: Upper bound of the pool size, 32 by default
    
    Returns:
        An int evaluating given case. Return None if args exceeds boundaries.
    """
    # Check boundaries
    if x<xlb or x>xrb or int(x)!=x:
        return None
    if rho>1 or rho<0:
        return None
    if tpr>1 or tpr<0:
        return None
    if tnr>1 or tnr<0:
        return None
    # Calculate tpr after the dilution
    tpr_diluted=tpr*(1-log(x,10).real/7)
    # Calculate E[S]
    s_P=x+1
    s_N=1
    p_TP=(1-(1-rho)**x)*tpr_diluted
    p_FP=(1-rho)**x*(1-tpr_diluted)
    p_TN=(1-rho)**x*tnr
    p_FN=(1-(1-rho)**x)*(1-tnr)
    return (s_P*(p_TP+p_FP)+s_N*(p_TN+p_FN))/x

def opts(rho,tpr,tnr,xlb=2,xrb=32):
    """
    Find the best pool size.

    Find the best pool size of the given case by iterating the evaluation with
    size ranging from min to max.

    Args:
        rho: Prevalence in given sample
        tpr: True positive rate (aka. sensitivity, P{TP}/(P{TP}+P{FN})) of the
             test
        tnr: True negative rate (aka. specificity, P{TN}/(P{TN}+P{FP})) of the
             test
        xlb: Lower bound of the pool size, 2 by default
        xlb: Upper bound of the pool size, 32 by default

    Returns:
        A tuple of int consisting optimal pool size and its score.
    """
    opt_s=999
    opt_x=-1
    for i in range(xlb,xrb+1):
        new_s= s(i,rho,tpr,tnr,xlb,xrb)
        if(new_s<opt_s):
            opt_s=new_s
            opt_x=i
    return opt_x,opt_s