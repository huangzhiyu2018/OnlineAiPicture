import os
import glob
import cv2
import dlib
import numpy as np

MODELFOLDER ="dlibmodels"

def find_person_rect(sFile):
    """得到当前图片的人脸数据方框

    Args:
        sFile (_type_): _description_
    """
    #人脸检测器
    
    detector = get_front_face_dector()
    #加载图片
    if glob.glob(sFile):        
        image = cv2.imread(sFile)    
        #得到人脸信息
        rects = detector(image)
        for rect in rects:        
            #绘制绿色方框
            cv2.rectangle(image,(rect.left(), rect.top()),(rect.right(), rect.bottom()),(0,255,0))
        #保存成功    
        cv2.imwrite(sFile,image)
        
        return rects,image
    else:
        return None,None
def get_front_face_dector():
    """人脸监测

    Returns:
        _type_: _description_
    """
    detector = dlib.get_frontal_face_detector()
    return detector
def get_face_encodeing(baseDir):
    """得到人脸编码模型

    Returns:
        _type_: _description_
    """
    shape_5_Folder=MODELFOLDER
    if baseDir:
        shape_5_Folder=os.path.join(baseDir,shape_5_Folder)
        
    shape_5_file=os.path.join(shape_5_Folder,"dlib_face_recognition_resnet_model_v1.dat")
    if glob.glob(shape_5_file):         
        face_encoder = dlib.face_recognition_model_v1(shape_5_file)
        return face_encoder
    else:
        print("not exisxt",shape_5_file)
        return None
def get_point_5_infor(baseDir):
    """得到人脸识别5个数据点的模型

    Returns:
        _type_: _description_
    """
    shape_5_Folder=MODELFOLDER
    if baseDir:
        shape_5_Folder=os.path.join(baseDir,shape_5_Folder)
    
    shape_5_file=os.path.join(shape_5_Folder,"shape_predictor_5_face_landmarks.dat")
    #与执行的路径有关
    if glob.glob(shape_5_file): 
        #print("exist",shape_5_file)
        pose_predictor_5_point = dlib.shape_predictor(shape_5_file)
        return pose_predictor_5_point
    else:
        print("not exisxt",shape_5_file)
        return None
   
def get_point_68_infor(baseDir):
    """得到人脸识别5个数据点的模型

    Returns:
        _type_: _description_
    """
    shape_5_Folder=MODELFOLDER
    if baseDir:
        shape_5_Folder=os.path.join(baseDir,shape_5_Folder)
    shape_5_file=os.path.join(shape_5_Folder,"shape_predictor_68_face_landmarks.dat")
    if glob.glob(shape_5_file): 
        print("exist",shape_5_file)
        pose_predictor_5_point = dlib.shape_predictor(shape_5_file)
        return pose_predictor_5_point
    else:
        print("not exisxt",shape_5_file)
        return None
def face_encoding_by_file(sFile,detector,landmarks_predictor, face_encoder,number_of_times_to_upsample=1, num_jitters=1):
    """根据文件进行编码

    Args:
        sFile (_type_): _description_
        detector (_type_): _description_
        landmarks_predictor (_type_): _description_
        face_encoder (_type_): _description_
        number_of_times_to_upsample (int, optional): _description_. Defaults to 1.
        num_jitters (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """
    if glob.glob(sFile): 
        image = cv2.imread(sFile) 
        return face_dector_encodings(image,detector,landmarks_predictor, face_encoder,number_of_times_to_upsample, num_jitters)
    else:
        print("File not exist",sFile)
        return None,None

def face_dector_encodings(face_image,detector,landmarks_predictor, face_encoder,number_of_times_to_upsample=1, num_jitters=1):
    """返回图像中每个人脸的 128D 描述符"""
    # 检测人脸
    face_locations = detector(face_image, number_of_times_to_upsample)
    #print(f"Face Number：{len(face_locations)}")
    return face_encodings(face_image,face_locations,landmarks_predictor, face_encoder, num_jitters)

def face_encodings(face_image,face_locations,landmarks_predictor, face_encoder, num_jitters=1):
    """返回图像中每个人脸的 128D 描述符"""
    if landmarks_predictor and face_encoder:        
        # 检测面部特征点
        raw_landmarks = [landmarks_predictor(face_image, face_location) for face_location in face_locations]
        # 使用每个检测到的特征点计算每个检测到的人脸的编码,返回numpy的列表，方便转换
        return np.array([np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for
                raw_landmark_set in raw_landmarks]),np.array(raw_landmarks)
        
    else:
        return None,None
if __name__ == '__main__':
    #base_dir=os.getcwd()
    #sModelFolder=os.path.join(base_dir,r"utils/",sModelFolder)
    #print(sModelFolder)
    #folder=os.path.join("..\media\persons")
    #对于中文文件名不识别，不知道为什么？
    
    #在下面的路径下执行
    #(base) E:\vscodeforpython\Web\recogpic\picturerec\utils>
    sFile=os.path.join(r"..\..\media\upload","dd98e9fa1b.jpg")
    if glob.glob(sFile): 
        print("exist",sFile)
        image = cv2.imread(sFile) 
    
        detector=get_front_face_dector()        
        landmarks_predictor=get_point_5_infor()
        face_encoder=get_face_encodeing()
        n=face_dector_encodings(image,detector,landmarks_predictor,face_encoder)
        print(type(n[0]),n)
    else:
        print("not exisxt",sFile)
    
    
    
    
    # #测试通过
    # rects,image=find_person_rect(sFile)
    # cv2.imshow("temp",image)    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()