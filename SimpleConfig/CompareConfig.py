'''比较文件的MD5,并输出需要进行更新的md5'''
import os
import hashlib
from statistics import mode
import sys

workpath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
lastexcelmd5 = open(workpath + "/ConfigText/ConfigMD5.txt" , mode = 'r' ,encoding = 'utf-8')
excelpath = workpath + "/Config/"

class ExcelData:
    def __init__(self,name,fullpath,md5):
        self.name = name
        self.fullpath = fullpath
        self.md5 = md5

def GetUpdateOrAddExcel():
    '''获取更新或者增加的excel'''
    #获取现有的excel
    configfolder = os.listdir(excelpath)
    updateexcel = []
    #工作中的excel文件路径
    workexceldic = {}
    for excel in configfolder:
        fullpath = excelpath + excel
        data = ExcelData(excel,fullpath,GetHash(fullpath))
        print(f'name = {data.name},fullpath = {data.fullpath},md5 = {data.md5}')
        workexceldic[data.name] = data
    #上一次的data信息
    lastexceldata = {}
    #上一次的excel文件
    for line in lastexcelmd5.readlines():
        line = line.strip()
        lastdata = line.split('=')
        data = ExcelData(lastdata[0],'',line[1])
        lastexceldata[lastdata[0]] = data
    lastexcelmd5.close()
    with open(workpath + "/ConfigText/ConfigMD5.txt",mode = 'w',encoding = 'utf-8') as file:
        file.truncate(0)
        for excelname in workexceldic:
            data = workexceldic[excelname]
            file.write(f'{data.name} = {data.md5}\n')
            if not data.name in lastexceldata:
                updateexcel.append(data)
            else:
                if lastexceldata[data.name].md5 !=  data.md5:
                    updateexcel.append(data)
    for item in updateexcel:
        print(item.name)
    return updateexcel
         

def GetHash(filepath):
    '''获取文件hash值'''
    with open(filepath,'rb') as file:
        data = file.read()
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

