import numpy as np

def check_npz(file,data,target,truename,imgheight,imgwidth):
    '''
    检查文件是否信息输入正确，不正确不能正确读取
    '''
    digits=np.load(file,allow_pickle=True)
    files=digits.files
    if (data  in files ) and (target in files):
        if truename is None:
            return True
        elif truename in files:
            return True
    return False
