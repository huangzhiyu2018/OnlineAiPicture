import numpy as np
def Euclidean_distance(n1,n2):
    """计算欧式距离

    Args:
        n1 (_type_): _description_
        n2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    if n1.shape!=n2.shape:
        return 100000
    d=(n1-n2)**2
    return d.sum()**0.5