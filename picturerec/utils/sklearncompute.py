
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier

def load_data(absolute_file_name,feature_name,target_value,target_namne):
    """载入相对路径的数据集，得到特征集和标签集，如果有标签名称得到标签名称

    Args:
        absolute_file_name (_string_): _npz文件绝对路径——
        feature_name：npz文件对应的特征键值
        target_value：npz文件对应的标签索引
        target_namne：npz文件标签真实名称       
    """
   
    #载入数据
    datas=np.load(absolute_file_name,allow_pickle=True)
    
    if target_namne is None:
        return datas[feature_name],datas[target_value],None
    
    return datas[feature_name],datas[target_value],datas[target_namne]

def knn_predict(train_set,train_label,test_set,k):
    """KNN的测试数据
    """
    neigh = KNeighborsClassifier(n_neighbors=k)    
    return base_predict(neigh,train_set,train_label,test_set)
    
def knn(train_set,train_label,test_set,test_label,k):
    """基本KNN计算

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
        k (_type_): K值
    """   
    neigh = KNeighborsClassifier(n_neighbors=k)    
    return base_compute(neigh,train_set,train_label,test_set,test_label)
def base_compute(algorithm,train_set,train_label,test_set,test_label):
    """基础计算类型，因为sklearn很方便所以这里用统一的计算函数

    Args:
        algorithm (_type_): 算法对象
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
    """
    algorithm.fit(train_set,train_label)
    score = algorithm.score(test_set,test_label)
    return score,algorithm

def base_predict(algorithm,train_set,train_label,test_set):
    """基础计算类型预测函数，因为sklearn很方便所以这里用统一的计算函数

    Args:
        algorithm (_type_): 算法对象
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        
    """
    algorithm.fit(train_set,train_label)
    score = algorithm.predict(test_set)
    return score,algorithm
def split_sets(data,target,rate):
    """分割数据集

    Args:
        data (_type_): 原始数据集
        target (_type_): 原始标签集
        rate (_type_): 测试集比重
    """
    #相当于分层采样，这样均匀
    return train_test_split(data, target, test_size=rate, stratify=target,random_state=42)
def base_gridcv(algorithm,data,targets,parameters,cv):
    """网格交叉验证的基本计算函数

    Args:        
        algorithm (_type_): 基础算法
        data：数据集
        targets:标签集
        parameters (_type_): 参数
    """
    clf = GridSearchCV(algorithm, parameters,cv=cv)
    clf.fit(data,targets)
    return clf.cv_results_,clf
def cv_knn(data,targets,cv,k):
    """对于KNN的交叉验证

    Args:
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数
        k (_type_): k近邻次数，计算k-1,k+1,k
    """
    parameters={"n_neighbors":[k-1,k,k+1]}
    neigh = KNeighborsClassifier()    
    return base_gridcv(neigh,data,targets,parameters,cv)

def navi_gaus(train_set,train_label,test_set,test_label):
    """朴素贝叶斯，高斯模型

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签

    Returns:
        _type_: 返回score和算法描述
    """
    clf = GaussianNB()
    return base_compute(clf,train_set,train_label,test_set,test_label)

def navi_gaus_predict(train_set,train_label,test_set):
    """朴素贝叶斯，高斯模型,预测

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集        

    Returns:
        _type_: 返回score和算法描述
    """
    clf = GaussianNB()
    return base_predict(clf,train_set,train_label,test_set)
def cv_navi(data,targets,cv):
    """朴素贝叶斯的交叉验证

    Args:
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数

    Returns:
        _type_: _description_
    """
    parameters={}#无参数被枚举
    clf = GaussianNB()    
    return base_gridcv(clf,data,targets,parameters,cv)
def decision_tree(train_set,train_label,test_set,test_label,criterion):
    """决策树

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
    """
    clf = DecisionTreeClassifier(criterion=criterion)
    return base_compute(clf,train_set,train_label,test_set,test_label)

def decision_tree_predict(train_set,train_label,test_set,criterion):
    """决策树

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        
    """
    clf = DecisionTreeClassifier(criterion=criterion)
    
    return base_predict(clf,train_set,train_label,test_set)
def cv_decistion(data,targets,cv):
    """决策树的交叉验证

    Args:
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数

    Returns:
        _type_: _description_
    """
    clf = DecisionTreeClassifier()
    parameters={"criterion":["gini","entropy"]}#无参数被枚举
    return base_gridcv(clf,data,targets,parameters,cv)

def logic_regression(train_set,train_label,test_set,test_label):
    """对数几率回归

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
    """
    clf = LogisticRegression(random_state=0)
    return base_compute(clf,train_set,train_label,test_set,test_label)

def logic_regression_predict(train_set,train_label,test_set):
    """对数几率回归,预测

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        
    """
    clf = LogisticRegression(random_state=0)
    return base_predict(clf,train_set,train_label,test_set)

def cv_logic_regression(data,targets,cv):
    """对数几率回归的交叉验证

    Args:
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数
    """
    parameters={}#无参数被枚举
    clf = LogisticRegression()    
    return base_gridcv(clf,data,targets,parameters,cv)
def svm(train_set,train_label,test_set,test_label,kernel):
    """svm

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
        kernel (_type_): 核函数
    """
    clf= SVC(kernel=kernel)
    return base_compute(clf,train_set,train_label,test_set,test_label)

def svm_predict(train_set,train_label,test_set,kernel):
    """svm

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集        
        kernel (_type_): 核函数
    """
    clf= SVC(kernel=kernel)
    return base_predict(clf,train_set,train_label,test_set)

def cv_svm(data,targets,cv):
    """svm的交叉验证   

    Args:
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数
    """
    parameters={"kernel": ['rbf','poly','sigmoid']}
    clf= SVC()
    return base_gridcv(clf,data,targets,parameters,cv)
def random_forest(train_set,train_label,test_set,test_label,trees,cit="gini"):
    """随机审理

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
        trees (_type_): 树个数
        cit (_type_): 决策标准
    """
    clf=RandomForestClassifier(n_estimators=trees,criterion=cit)
    return base_compute(clf,train_set,train_label,test_set,test_label)

def random_forest_predict(train_set,train_label,test_set,trees,cit="gini"):
    """随机审理

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
        trees (_type_): 树个数
        cit (_type_): 决策标准
    """
    clf=RandomForestClassifier(n_estimators=trees,criterion=cit)
    return base_predict(clf,train_set,train_label,test_set)

def cv_random_forest(data,targets,cv):
    """随机森林交叉验证

    Args:
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数
    """
    parameters={"n_estimators":range(10,100,10)}
    clf=RandomForestClassifier()
    return base_gridcv(clf,data,targets,parameters,cv)
def adaboost(train_set,train_label,test_set,test_label,trees):
    """adaboost模型

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
        trees (_type_): 树个数
    """
    base_estimator= DecisionTreeClassifier(max_depth=3)   
    clf=AdaBoostClassifier(base_estimator=base_estimator,n_estimators=trees)    
    return base_compute(clf,train_set,train_label,test_set,test_label)

def adaboost_predict(train_set,train_label,test_set,trees):
    """adaboost模型

    Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        
        trees (_type_): 树个数
    """
    base_estimator= DecisionTreeClassifier(max_depth=3)   
    clf=AdaBoostClassifier(base_estimator=base_estimator,n_estimators=trees)    
    return base_predict(clf,train_set,train_label,test_set)

def cv_adaboost(data,targets,cv):
    """随机森林交叉验证

    Args:
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数
    """
    base_estimator= DecisionTreeClassifier(max_depth=3)
    #parameters={"n_estimators":range(20,100,20)}
    parameters={}
    clf=AdaBoostClassifier(base_estimator=base_estimator)
    return base_gridcv(clf,data,targets,parameters,cv)
def MLP_classfy(train_set,train_label,test_set,test_label,hidden_layer_sizes):
    """多层感知器模型
        Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集
        test_label (_type_): 测试集标签
        hidden_layer_sizes:隐藏个数     
    """
    clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes)
    return base_compute(clf,train_set,train_label,test_set,test_label)

def MLP_classfy_predict(train_set,train_label,test_set,hidden_layer_sizes):
    """多层感知器模型
        Args:
        train_set (_type_): 训练集
        train_label (_type_): 训练集标签
        test_set (_type_): 测试集        
        hidden_layer_sizes:隐藏个数     
    """
    clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes)
    return base_predict(clf,train_set,train_label,test_set)

def cv_MLP(data,targets,cv):
    """感知器模型交叉验证

    Args:         
        data (_type_): 数据集
        targets (_type_): 标签集
        cv (_type_): 交叉验证次数
    """
    parameters={}
    clf=MLPClassifier()
    return base_gridcv(clf,data,targets,parameters,cv)
    
    