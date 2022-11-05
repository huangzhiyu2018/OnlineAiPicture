import sys
sys.path.append('../')
from picturerec import models
if __name__ == '__main__':
    querySet = models.PersonInfor.objects.filter(isvalide=1,descriptions__isnull=False)#得到数据集，必须要求描述不空
    for temp in querySet:
        #record_description=(temp.descriptions)
        print(type(temp.descriptions))
        print(temp.descriptions)
        #np_description=pickle.loads(temp.descriptions)
        #print(type(np_description),np_description)
        break