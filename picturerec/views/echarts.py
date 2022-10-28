from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from picturerec import models

def echarts(request):
    return render(request,"echarts.html")
def echarts_line(request):
    querySet=models.StudentsInfor.objects.all()
    
    for_xAxis=[]
    for_yValue=[]
    for obj in querySet:
        for_xAxis.append(obj.name)
        for_yValue.append(obj.score)        
        
    
    series_list=[
       for_yValue       
    ]
    data={
      "title": "学生成绩",
      "legend":  ["成绩"],        
      "xAxis": for_xAxis,
      "series":series_list
      }
    
    result={
        "status":True,
        "data":data
        }
    return JsonResponse(result)

def echarts_pie(request):
    querySet=models.StudentsInfor.objects.all()    
    for_pie=[]
    for obj in querySet:
        dic={"name":obj.name,"value":obj.score}
        for_pie.append(dic)        
   
   
    data={
      "title": "学生成绩",
      "legend":  ["成绩"], 
       "series":for_pie
      }
    
    result={
        "status":True,
        "data":data
        }
    return JsonResponse(result)