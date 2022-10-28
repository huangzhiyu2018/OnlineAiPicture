from django.shortcuts import render,HttpResponse,redirect
from picturerec import models

from django import forms
from django.core.exceptions import ValidationError
from picturerec.utils.forms import BootrapModelForm,BootrapForm
from picturerec.utils.encrypt import md5
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

def user_add(request):
    
    title="添加用户"
    if request.method=="GET":
        form=UserAddModelForm()             
        return render(request,"change.html",{"title":title,"form":form})
    
    form =UserAddModelForm(data=request.POST) 
    if form.is_valid():
        form.save()
        return redirect("/user/list/") 
    
    return render(request,"change.html",{"title":title,"form":form})
#免除cs_token认证
@csrf_exempt
def user_addbyajax(request):
    """利用ajax提交添加信息

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    form =UserAddModelForm(data=request.POST) 
    if form.is_valid():
        form.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False,"errors":form.errors})

class UserAddModelForm(BootrapModelForm):    
    #新建一个字段,加上render_value=True防止提交后密码重置
    confirm_password=forms.CharField(label='确认密码',widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=models.UserInfor
        fields=["userName",'passWord',"confirm_password","powerRights"]
        widgets={
            "passWord":forms.PasswordInput(render_value=True),
        }
    #这是提交时的处理，clean是按照fields中的定义顺序进行的
    def clean_passWord(self):
        pwd=self.cleaned_data.get("passWord")
        return md5(pwd)
    def clean_confirm_password(self):
        #对密码的确认,cleaned_data字典
        confirm=self.cleaned_data.get("confirm_password")
        #这是已经加密的
        pwd=self.cleaned_data.get("passWord")
        
        confirm=md5(confirm)
        if pwd!=confirm:
            raise ValidationError("确认密码与密码不一致")
        return confirm

class UserEditModelForm(BootrapModelForm):    
    class Meta:
        model=models.UserInfor
        fields=["userName","powerRights"]    
    
def user_edit(request,uid):    
    """
    编辑用户
    """
    row_obj=models.UserInfor.objects.filter(id=uid).first()
    title="编辑用户"
    
    if request.method=="GET":
        if not row_obj:
            return redirect("/user/list/")        
        form=UserEditModelForm(instance=row_obj)             
      
        return render(request,"change.html",{"title":title,"form":form})
    form=UserEditModelForm(instance=row_obj,data=request.POST)             
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request,"change.html",{"title":title,"form":form})
def user_list(request):
    """
    用户列表
    """
    form=UserAddModelForm()      
    querySet=models.UserInfor.objects.all()        
    
    return render(request,"user_list.html",{"querySet":querySet,"form":form})


def user_delete_ajax(request):
    """ajax删除

    Args:
        request (_type_): _description_
    """
    uid=request.GET.get("uid")
    models.UserInfor.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})
    
def user_delete(request,uid):
    """
    删除列表
    """
    models.UserInfor.objects.filter(id=uid).delete()
    return redirect("/user/list/")
class UserResetModelForm(BootrapModelForm):    
    confirm_password=forms.CharField(label='确认密码',widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=models.UserInfor
        fields=['passWord']
        widgets={
            "passWord":forms.PasswordInput(render_value=True),
        }
    #这是提交时的处理，clean是按照fields中的定义顺序进行的
    def clean_passWord(self):
        pwd=self.cleaned_data.get("passWord")
        return md5(pwd)
    def clean_confirm_password(self):
        #对密码的确认,cleaned_data字典
        confirm=self.cleaned_data.get("confirm_password")
        #这是已经加密的
        pwd=self.cleaned_data.get("passWord")
        
        confirm=md5(confirm)
        if pwd!=confirm:
            raise ValidationError("确认密码与密码不一致")
        return confirm  
    
def user_reset(request,uid):
    """
    重置密码
    """
    row_obj=models.UserInfor.objects.filter(id=uid).first()
    title="重置密码"
    
    if request.method=="GET":
        if not row_obj:
            return redirect("/user/list/")        
        form=UserResetModelForm()             
      
        return render(request,"change.html",{"title":title,"form":form})
    form=UserResetModelForm(instance=row_obj,data=request.POST)             
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request,"change.html",{"title":title,"form":form})

class UserLoginModelForm(BootrapForm):    
    userName=forms.CharField(
        label='用户名',
        widget=forms.TextInput
        )
    passWord=forms.CharField(label='密码',widget=forms.PasswordInput(render_value=True))
    #这是提交时的处理，clean是按照fields中的定义顺序进行的
    def clean_passWord(self):
        pwd=self.cleaned_data.get("passWord")
        return md5(pwd)
    
def login(request):
    if request.method=="GET":
        form=UserLoginModelForm()
        return render(request,"login.html",{"form":form})
    
    form = UserLoginModelForm(data=request.POST)
    if form.is_valid():        
        #传入字典可以空**转成元组
        obj=models.UserInfor.objects.filter(**form.cleaned_data).first()
        if obj:
            #加入一个sesssion
            request.session['info']={"id":obj.id,"userName":obj.userName,"powerRights":obj.powerRights}
            #根据权限转到不同页面
            if obj.powerRights=="管理员":
                return redirect("/user/list/")
            else:
                return redirect("/picturerec/uploadfile/")
        form.add_error("passWord","用户名或密码错误")
        return render(request,"login.html",{"form":form})
    return render(request,"login.html",{"form":form})
    
def logout(request):
    """注销

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """       
    request.session.clear()
    return redirect("/login/")