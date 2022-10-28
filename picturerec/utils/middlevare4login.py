from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
#Django 提供 django.utils.deprecation.MiddlewareMixin 来简单的创建中间件类
class Mymiddle4login(MiddlewareMixin):
    
    def process_request(self,request):
        #login登录不阻挡
        if request.path_info=="/login/":
            return
        #返回none意味着通过
        info=request.session.get("info")#不能直接用session["info"]因为此时还不一定存在
        #登录后直接通过
        if info:
            return
        #如果没有登录，要去掉login的访问
        return redirect("/login/")
        
    def process_response(self,request, response) :
        #必须返回，否则报错
        return response
    
    
    
    