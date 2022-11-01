import os
import ast
import datetime
import base64
import uuid
from django.shortcuts import render,  redirect
from django import forms
from picturerec import models
from django.http import JsonResponse
from django.conf import settings
from picturerec.utils.forms import BootrapModelForm, BootrapForm
from picturerec.utils import dlibcompute
from django.db.models import Q
from PIL import Image
import numpy as np
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def scrapy_image(request):
    if request.method=="POST": 
        #传入信息
        form= PersonInforModelForm(request.POST,request.FILES)  
             
        if form.is_valid(): 
           
            form.instance.create_time=datetime.datetime.now()
            #form.instance.upload_user=request.session.info.userName     
            info=request.session.get("info")
            if info:                
                form.instance.upload_user=info["userName"]
            else:
                form.instance.upload_user="test"                
            
             #先保存，否则没有图片
            form.save()
            #得到图片绝对路径           
            absolute_file_path = os.path.join('media',form.instance.file.name)            
            #print(form.instance.file.name)
            #print(absolute_file_path)
            #得到人脸信息
            rects,image=dlibcompute.find_person_rect(absolute_file_path)    
                       
            #print(len(rects))         

            isValide=0
            if len(rects)==1:
                isValide=1 

            models.PersonInfor.objects.filter(file=form.instance.file.name).update(isvalide=isValide)
            
            return JsonResponse({"status":True,"path":form.instance.file.name,"valide":isValide})
        else:            
            return JsonResponse({"status":False,"errors":form.errors})
                
        # personName=request.POST.get("person_name")
        # file = request.FILES.get("file")           
        # db_file = handle_uploaded_file(file,personName)
        # print(db_file)        
        # return render(request,"scraperimage.html",{"status":True,"personName":personName,"dbFile":db_file})
        #return render(request,"scraperimage.html",{"status":True})
    
    return render(request,"scraperimage.html")

def face_test(request):
    querySet = models.PersonInfor.objects.all()       
    #取出第一个进行测试
    first=querySet[0]
    absolute_file_path = os.path.join('media',first.file.name)
    #得到人脸信息
    rects,image=dlibcompute.find_person_rect(absolute_file_path)
    print(rects)
    return render(request,"personlist.html",{"querySet":querySet})

# def handle_uploaded_file(file,personName):
#     '''
#     保存数据文件
#     '''

#     file_data = file.read()
#     #查看下数据信息
#     print(type(file_data))
    
#     # img_data = file_data.strip().split(",")[-1]
#     img = base64.b64decode(file_data)
    
#     ext = "jpg"
#     file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

#     # file path relative to 'media' folder
#     #file_path = os.path.join('files', file_name)
#     #存入的文件名
#     database_folder=os.path.join("persons",personName, file_name)
#     #写入的文件名
#     absolute_file_path = os.path.join('media',database_folder )
#     #检查路径是否存在
#     directory = os.path.dirname(absolute_file_path)
#     if not os.path.exists(directory):
#         os.makedirs(directory)    
#     #写入数据
#     with open(absolute_file_path, 'wb+') as destination:
#         destination.write(img)
    
#     return database_folder

class PersonInforModelForm(BootrapModelForm):
    """针对上传人物图片的模型

    Args:
        BootrapModelForm (_type_): _description_
    """
    class Meta:
        model=models.PersonInfor        
        exclude=["upload_user","create_time","isvalide"]
        bootstrap_exclude_fileds=["file"]   
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["bmp","jpg","png"]:
            raise forms.ValidationError("仅支持bmp,jpg,png 类型文件")
        return file