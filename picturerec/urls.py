from django.urls import path
from picturerec.views import user,picture,algorithm
urlpatterns = [
    #对管理员的操作
    path("user/list/",user.user_list),
    path("user/add/",user.user_add),
    path("user/addbyajax/",user.user_addbyajax),
    path("user/<int:uid>/edit/",user.user_edit),
    path("user/<int:uid>/reset/",user.user_reset),    
    path("user/<int:uid>/delete/",user.user_delete),
    path("user/delete/",user.user_delete_ajax),
    #数据集上传
    path("picturerec/uploadfile/",picture.picture_upload),
    path("picturerec/filelist/",picture.picture_list),
    #登录注册
    path("login/",user.login),
    path("logout/",user.logout),
    #图片文件上传
    path("image/uploadfile/",picture.img_upload),
    path("image/recog/",algorithm.image_recon),
    path("image/<int:uid>/delete/",picture.img_delete),
    path("image/result/",algorithm.image_result),
    #计算
    path("algorithm/cv/",algorithm.cv_compute),   
    path("algorithm/test/",algorithm.test_compute),
    path("algorithm/list/",algorithm.result_list),
    path("algorithm/<int:uid>/delete/",algorithm.result_delete),
]