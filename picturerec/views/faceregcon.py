import os
import ast
import datetime
import uuid
from django.shortcuts import render,  redirect
from django import forms
from picturerec import models
from django.http import JsonResponse
from django.conf import settings
from picturerec.utils.forms import BootrapModelForm
from picturerec.utils import dlibcompute
from django.db.models import Q
from PIL import Image
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
    return render(request,"testcascade.html")
def handle_uploaded_file(file):
    '''
    保存数据文件
    '''
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # file path relative to 'media' folder
    #file_path = os.path.join('files', file_name)
    url_file_name=os.path.join('upload',file_name)
    
    absolute_file_path = os.path.join('media', url_file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return url_file_name
@csrf_exempt
def face_recon(request):
    """人脸识别

    Args:
        request (_type_): _description_
    """
    if request.method=="GET":
        querySet = models.PersonInfor.objects.all() 
        return render(request,"personrecon.html",{"querySet":querySet})
    #提交图片后进行识别
    form= PersonInforModelForm(request.POST,request.FILES)  
    if form.is_valid():
        file = request.FILES.get("file")   
        urlfilename=handle_uploaded_file(file)
        #有效的提交进行图片处理
        return JsonResponse({"status":True,"path":urlfilename,"valide":0,"person":""})    
    else:            
        return JsonResponse({"status":False,"errors":form.errors})    

    

def face_list(request):    
    querySet = models.PersonInfor.objects.all() 
    return render(request,"personlist.html",{"querySet":querySet})

def face_delete(request):
    """通过ajax删除人脸信息

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    uid=request.GET.get("uid")
    
    file=models.PersonInfor.objects.filter(id=uid).first()  
    
    #得到图片真实绝对路径
    absolute_file_path = os.path.join('media', str(file.file))
    #print(absolute_file_path)
    if os.path.exists(absolute_file_path):
        os.remove(absolute_file_path)
    else:
        print("file not exist")
    models.PersonInfor.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

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