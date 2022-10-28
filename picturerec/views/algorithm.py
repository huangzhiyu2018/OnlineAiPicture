import os
import ast
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from picturerec import models
from django.http import JsonResponse
from django.conf import settings
from picturerec.utils.forms import BootrapModelForm, BootrapForm
from picturerec.utils import sklearncompute
from django.db.models import Q
from PIL import Image
import numpy as np


ALGORITHMS=[
    #"criterion='gini'"
    #"kernel='rbf'"
    
    ("最近邻","n_neighbors=5"),\
    ("朴素贝叶斯","无"),\
    ("决策树","无"),\
    ("对数几率回归","无"),\
    ("SVM","无"),\
    ("随机森林","n_estimators=100"), \
    ("Adaboost","n_estimators=50"),\
    ("多层感知器","hidden_layer_sizes=100")]

def parse_para(para):
    """解析传过来的算法参数

    Args:
        para (_type_): _description_
    """
    if para=="无":
        return para
    i=para.index("=")
    
    if i>=0:
        return para[i+1:]
    return -1
    
def load_datas(data_id):
    """载入数据

    Args:
        data_id (_type_): _description_
    """
    querySet = models.TrainSet.objects.filter(id=data_id).first()
    #文件名称
    file = querySet.file
    #得到真实路径
    absolute_file_name = os.path.join(settings.MEDIA_ROOT, str(file))
    #载入数据
    data, target, truename = sklearncompute.load_data(absolute_file_name,
                                                      querySet.featurename,
                                                      querySet.targetname,
                                                      querySet.truename)
    return data, target, truename


def cv_compute(request):
    id = request.GET.get("sets_id")  #不用用直接[]这种方式
    cv = request.GET.get("cv_number")
    al = request.GET.get("algorithms")
    al_para = request.GET.get("algorithm_paras")
    #得到的是models.TrainSet对象
    data, target, truename = load_datas(id)
    #计算过程
    score = 0
    algorithm = "无"
    insert_dic={}
    insert_dic["datasets_id"]=int(id)
    insert_dic["algorithm"]=f"cv:{cv},算法：{al}"
    insert_dic["paramers"]=al_para

    para_value=parse_para(al_para)
    
    if al == "最近邻":
        K=int(para_value)
        score, algorithm = sklearncompute.cv_knn(data, target, int(cv), K)       
        
    if al == "朴素贝叶斯":
        score, algorithm = sklearncompute.cv_navi(data, target, int(cv))
    if al == "决策树":
        score, algorithm = sklearncompute.cv_decistion(data, target, int(cv))
    if al == "对数几率回归":
        score, algorithm = sklearncompute.cv_logic_regression(
            data, target, int(cv))
    if al == "SVM":
        score, algorithm = sklearncompute.cv_svm(data, target, int(cv))
    if al == "随机森林":
        score, algorithm = sklearncompute.cv_random_forest(
            data, target, int(cv))
    if al == "Adaboost":
        score,algorithm = sklearncompute.cv_adaboost(data,target,int(cv))
    if al == "多层感知器":
        score,algorithm = sklearncompute.cv_MLP(data,target,int(cv))
        
    insert_dic["score"]=f"{score}"
    
    info=request.session.get("info")
    if info:
        insert_dic["user"]=info["userName"]
    else:
        insert_dic["user"]="test"

    insert_dic["create_time"]=datetime.datetime.now()
    models.RecogResult.objects.create(**insert_dic)
    
    return JsonResponse({
        "status": True,
        "score": str(score),
        "algorithm": str(algorithm)
    })


def test_compute(request):
    
    rate = request.GET.get("test_rate")        
    id = request.GET.get("sets_id")  #不用用直接[]这种方式    
    al = request.GET.get("algorithms")
    al_para = request.GET.get("algorithm_paras")
    #加载数据集
    data, target, truename = load_datas(id)
    #分割数据集
    X_train, X_test, y_train, y_test = sklearncompute.split_sets(
        data, target, float(rate))
    #计算过程
    score = 0
    algorithm = "无"

    insert_dic={}
    insert_dic["datasets_id"]=int(id)
    insert_dic["algorithm"]=f"算法：{al}"
    insert_dic["paramers"]=al_para
    
    para_value=parse_para(al_para)
    #目前算法参数都是默认值，还没有进行解析
    if al == "最近邻":  #计算KNN
        K=int(para_value)
        score, algorithm = sklearncompute.knn(X_train, y_train, X_test, y_test,
                                              K)
    if al == "朴素贝叶斯":
        score, algorithm = sklearncompute.navi_gaus(X_train, y_train, X_test,
                                                    y_test)
    if al == "决策树":
        score, algorithm = sklearncompute.decision_tree(
            X_train, y_train, X_test, y_test,"gini")
    if al == "对数几率回归":
        score, algorithm = sklearncompute.logic_regression(
            X_train, y_train, X_test, y_test)
    if al == "SVM":
        score, algorithm = sklearncompute.svm(X_train, y_train, X_test, y_test,
                                              "rbf")
    if al == "随机森林":
        K=int(para_value)
        score, algorithm = sklearncompute.random_forest(
            X_train, y_train, X_test, y_test, K)
    if al == "Adaboost":
        K=int(para_value)
        score,algorithm=sklearncompute.adaboost(X_train, y_train, X_test, y_test,K)
    if al == "多层感知器":
        iStart=int(para_value)     
            
        score,algorithm = sklearncompute.MLP_classfy(X_train, y_train, X_test, y_test,(iStart,))

    insert_dic["score"]=f"{score}"
    
    info=request.session.get("info")
    if info:
        insert_dic["user"]=info["userName"]
    else:
        insert_dic["user"]="test"        
       
    insert_dic["create_time"]=datetime.datetime.now()
    models.RecogResult.objects.create(**insert_dic)
    return JsonResponse({
        "status": True,
        "score": score,
        "algorithm": str(algorithm)
    })
def result_list(request):
    querySet=models.RecogResult.objects.all()
    return render(request,"results_list.html",{"querySet":querySet})

def result_delete(request,uid):
    obj=models.RecogResult.objects.filter(id=uid).delete()
    return redirect("/algorithm/list/")

def image_recon(request):
    id = request.GET.get("sets_id")  #不用用直接[]这种方式    
    al = request.GET.get("algorithms")
    al_para = request.GET.get("algorithm_paras")     
    pic_ids=request.GET.get("pic_ids")
    pic_idlist=pic_ids.split(",")

    pic_ids=[int(temp.replace("pic_","")) for temp in pic_idlist]

    q1 = Q()
    q1.connector = 'OR'
    for temp in pic_ids:
        q1.children.append(("id",temp))

    #得到图片的存储信息
    querySet = models.UploadFileRecord.objects.filter(q1)

    testSet=[]

    for tempSet in querySet:
        file = tempSet.file
        #得到真实路径
        absolute_file_name = os.path.join(settings.MEDIA_ROOT,str(file))
        img=Image.open(absolute_file_name)
        temp=np.asarray(img)
        t=temp.reshape(1,-1).flatten()
        testSet.append(t)
        
    score = 0
    algorithm = "无"
#加载数据集
    data, target, truename = load_datas(id)
    
    insert_dic={}
    insert_dic["datasets_id"]=int(id)
    insert_dic["algorithm"]=f"算法：{al}"
    insert_dic["paramers"]=al_para
    
    para_value=parse_para(al_para)
    #目前算法参数都是默认值，还没有进行解析
    if al == "最近邻":  #计算KNN
        K=int(para_value)
        score, algorithm = sklearncompute.knn_predict(data,target,testSet,K)
    if al == "朴素贝叶斯":
        score, algorithm = sklearncompute.navi_gaus_predict(data,target,testSet)
    if al == "决策树":
        score, algorithm = sklearncompute.decision_tree_predict(data,target,testSet,"gini")
    if al == "对数几率回归":
        score, algorithm = sklearncompute.logic_regression_predict(data,target,testSet)
    if al == "SVM":
        score, algorithm = sklearncompute.svm_predict(data,target,testSet,
                                              "rbf")
    if al == "随机森林":
        K=int(para_value)
        score, algorithm = sklearncompute.random_forest_predict(data,target,testSet, K)
    if al == "Adaboost":
        K=int(para_value)
        score,algorithm=sklearncompute.adaboost_predict(data,target,testSet,K)
    if al == "多层感知器":
        iStart=int(para_value)     
            
        score,algorithm = sklearncompute.MLP_classfy_predict(data,target,testSet,(iStart,))

    insert_dic["score"]=f"{score}"
    
    info=request.session.get("info")
    if info:
        insert_dic["user"]=info["userName"]
    else:
        insert_dic["user"]="test"        
       
    insert_dic["create_time"]=datetime.datetime.now()
    models.RecogResult.objects.create(**insert_dic)

    
    score_str=f"pic_ids:{pic_ids} predict:{score}"
    
    return JsonResponse({
        "status": True,
        "score": score_str,
        "algorithm": str(algorithm)
    })
def image_result(request):
    """图片识别结果
    """
    q1 = Q()
    q1.connector = 'OR'
    q1.children.append(("picture",""))
    q1.children.append(("picture",None))
    #得到所有识别结果中，图片信息不为空的信息
    querySet=models.RecogResult.objects.exclude(q1).order_by("-create_time")
    #得到图片信息后，利用图片字段内容和识别结果构造新的数据集
    show_list=[]#未来显示的信息列表，每个元素都是一个记录信息
    for temp in querySet:
        #每个temp都是RecogResult类型
        #得到对应的图片id列表
        pic_id_list=f"{temp.picture}"
        score_list=f"{temp.score}".replace("[","").replace("]","").split(" ")
        L1=ast.literal_eval(pic_id_list)

        result_id=str(temp.id)        

        
       
        for index,pic_id in enumerate(L1):  #枚举所有图片列表中数据            
            temp_row=[]
            #得到图片信息
            picInfo=models.UploadFileRecord.objects.filter(id=pic_id).first()
            #for field in models.UploadFileRecord._meta.get_fields():
                #print(type(picInfor.field))
           
            #print(picInfo.__dict__)
            #print("*"*10)
            for key in picInfo.__dict__.keys():
                if key=="_state":                   
                    continue
                temp_row.append(picInfo.__dict__[key])#加入到行中

            temp_row.append(score_list[index])
            #最后一个元素计算时间
            temp_row.append(temp.create_time)

            show_list.append(temp_row)           
        
    #print(show_list)       
    return render(request,"img_result_list.html",{"querySet":show_list})
    
    