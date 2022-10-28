from django import forms
class Bootstrap:
    bootstrap_exclude_fileds=[]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)        
        for name,field in self.fields.items():
            #不需要bootstrap的字段
            if name in self.bootstrap_exclude_fileds:
                continue
            if  field.widget.attrs:
                field.widget.attrs['class']='form-control'
                field.widget.attrs['placeholder']=field.label
            else:
                field.widget.attrs={"class":"form-control",'placeholder':field.label}            
class BootrapModelForm(Bootstrap,forms.ModelForm):
    pass
class BootrapForm(Bootstrap,forms.Form):
    pass
    