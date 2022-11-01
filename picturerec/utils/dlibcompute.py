import os
import glob
import cv2
import dlib
import numpy as np

sModelFolder=r"./dlibmodels"

def find_person_rect(sFile):
    """得到当前图片的人脸数据方框

    Args:
        sFile (_type_): _description_
    """
    #人脸检测器
    
    detector = dlib.get_frontal_face_detector()
    #加载图片
    if glob.glob(sFile):
        print("FileExist:",sFile)
    else:
        print("Not exsist",sFile)
    image = cv2.imread(sFile)    
    #得到人脸信息
    rects = detector(image)
    for rect in rects:        
        #绘制绿色方框
        cv2.rectangle(image,(rect.left(), rect.top()),(rect.right(), rect.bottom()),(0,255,0))
    #保存成功    
    cv2.imwrite(sFile,image)
    
    return rects,image

if __name__ == '__main__':
    base_dir=os.getcwd()
    folder=os.path.join(base_dir,"media/persons")
    sFile=os.path.join(folder,"Tom.jpg")
    #测试通过
    rects,image=find_person_rect(sFile)
    cv2.imshow("temp",image)    
    cv2.waitKey(0)
    cv2.destroyAllWindows()