from email.policy import default
from django.db import models

class UserInfor(models.Model):
    """登录用户信息

    Args:
        models (_type_): _description_
    """
    userName=models.CharField(max_length=30,verbose_name='用户名')
    passWord=models.CharField(max_length=80,verbose_name='密码')
    right_choice = ((0, "管理员"), (1, "用户"))
    powerRights=models.SmallIntegerField(verbose_name='权重',choices=right_choice)
class TrainSet(models.Model):
    """训练集信息，文件必须是numpy压缩文件.npz格式
    读取得到的npz文件信息，npz文件中files是存储对应的变量名
    
    featurename：文件中对应特征的键值
    targetname:文件中对应标签的键值
    imagesize:图片大小
    truename:真实图片名称，标签值一般是索引，这里是真实名称
    Args:
        models (_type_): _description_
    """
    
    featurename=models.CharField(max_length=30,verbose_name='特征名',default="data")
    targetname=models.CharField(max_length=30,verbose_name='标签名',default="target")
    imageheight=models.SmallIntegerField(verbose_name='图片高度（像素）',default=8)
    imagewidth=models.SmallIntegerField(verbose_name='图片宽度（像素）',default=8)
    truename=models.CharField(max_length=30,verbose_name='真实标签名',null=True,blank=True)
    descreb=models.CharField(max_length=125,verbose_name='数据集描述',null=True,blank=True,default="手写体数据集")
    file=models.FileField(verbose_name="文件",max_length=125,upload_to="train/",default="")   
    type_choice=((0,"训练集"),(1,"测试集"),(2,"验证集")) 
    setstype=models.SmallIntegerField(verbose_name='样本集类型',choices=type_choice,default=0)
    #显示信息用
    def __str__(self):
        return "文件：{0} 描述：{1}".format(self.file,self.descreb)
class UploadFileRecord(models.Model):
    '''
    上传文件信息
    '''
    create_time = models.DateField(verbose_name='上传时间')
    upload_user=models.CharField(max_length=30,verbose_name='上传者')
    file=models.FileField(verbose_name="文件",max_length=125,upload_to="images/",default="")  
      #显示信息用
    def __str__(self):
        return str(self.file)
class RecogResult(models.Model):
    '''
    识别结果列表
    '''
    datasets=models.ForeignKey(to="TrainSet",to_field="id",on_delete=models.SET_NULL,null=True,blank=True,verbose_name='数据集',default=None)
    algorithm=models.CharField(max_length=30,verbose_name='算法名',default="KNN")
    paramers=models.CharField(max_length=125,verbose_name='参数',null=True,blank=True)
    score=models.TextField(verbose_name='评估值',null=True,blank=True)
    picture=models.CharField(max_length=125,verbose_name='图片ID列表',default="")
    user=models.CharField(max_length=30,verbose_name='操作者',default="")
    create_time = models.DateField(verbose_name='计算时间',default=None,null=True,blank=True)