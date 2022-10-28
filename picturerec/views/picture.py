import os
import uuid
import datetime
from django.shortcuts import render,HttpResponse,redirect
from django import forms
from picturerec import models

from picturerec.utils.forms import BootrapModelForm,BootrapForm
from picturerec.utils import checkfile
from picturerec.views.algorithm import ALGORITHMS

def picture_list(request):
    
    querySet=models.TrainSet.objects.all()  
    #算法选择需要 ALGORITHMS变量
    return render(request, 'pictur_list.html',{"title":"样本集列表","querySet":querySet,"algorithms":ALGORITHMS})

def picture_upload(request):
    """数据集上传

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.instance.setstype=0           
            form.save()
            return redirect("/picturerec/filelist/")
    else:
        form = FileUploadModelForm()
    return render(request, 'pictureupload.html', 
                  {'form': form, 'title':"上传样本集"})
def img_delete(request,uid):
    #试着删除服务器的文件
    file=models.UploadFileRecord.objects.filter(id=uid).first()    
  
    absolute_file_path = os.path.join('media', str(file))
    print(absolute_file_path)
    if os.path.exists(absolute_file_path):
        os.remove(absolute_file_path)
    else:
        print("file not exist")
    obj=models.UploadFileRecord.objects.filter(id=uid).delete()
    return redirect("/image/uploadfile/")
def img_upload(request):
    '''
    图片上传
    '''
    if request.method == "POST":
        form = ImageUploadModelForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.instance.create_time=datetime.datetime.now()
            #form.instance.upload_user=request.session.info.userName     
            info=request.session.get("info")
            if info:                
                form.instance.upload_user=info["userName"]
            else:
                form.instance.upload_user="test"                
            form.save()
            return redirect("/image/uploadfile/")
    else:
        querySet=models.UploadFileRecord.objects.all()    
        form = ImageUploadModelForm()
        set_id=""
        algo=""
        alpara=""
        if "set_id" in request.GET:
            #填入数据集选择信息
            set_id=request.GET["set_id"]
            algo=request.GET["algo"]
            alpara=request.GET["alpara"]
            print(alpara)

        trainQuerySet=models.TrainSet.objects.all()
        
        return render(request, 'image_upload.html', 
                  {'form': form, 'title':"上传图片","querySet":querySet,
                   "train_querySet":trainQuerySet,
                   "algorithms":ALGORITHMS,
                   "set_id":set_id,"algo":algo,"alpara":alpara})
        
    return render(request, 'image_upload.html', 
                  {'form': form, 'title':"上传图片"})
    
class ImageUploadModelForm(BootrapModelForm):
    "上传图片的Form"
    class Meta:
        model=models.UploadFileRecord        
        exclude=["upload_user","create_time"]
        bootstrap_exclude_fileds=["file"]    
    def clean_file(self):
            file = self.cleaned_data['file']
            ext = file.name.split('.')[-1].lower()
            if ext not in ["bmp","jpg","png"]:
                raise forms.ValidationError("仅支持bmp,jpg,png 类型文件")
            return file
            
def handle_uploaded_file(file):
    '''
    保存数据文件
    '''
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # file path relative to 'media' folder
    #file_path = os.path.join('files', file_name)
    
    absolute_file_path = os.path.join('media', 'images', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
class FileUploadForm(BootrapForm):
    file = forms.FileField(label="图片文件")
    # upload_method = forms.CharField(label="Upload Method", max_length=20,
    #                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["jpg", "png", "npz"]:
            raise forms.ValidationError("仅 jpg, png ,npz 类型文件允许上传")
        # return cleaned data is very important.
        return file   
class FileUploadModelForm(BootrapModelForm):
    class Meta():
        model = models.TrainSet
        #fields ="__all__"        
        exclude=["setstype"]
        bootstrap_exclude_fileds=["file"]      
        
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["npz"]:
            raise forms.ValidationError("仅支持npz 类型文件")
        # return cleaned data is very important.
        
        data=self.cleaned_data["featurename"]
        target=self.cleaned_data["targetname"]
        truename=self.cleaned_data.get("truename")
        img_height=self.cleaned_data.get("imageheight")
        img_weight=self.cleaned_data.get("imagewidth")
        result=checkfile.check_npz(file,data,target,truename,img_height,img_weight)
        if result[0]:
            return file   
        raise forms.ValidationError("npz文件中不存在相关特征名或标签名")                
        
