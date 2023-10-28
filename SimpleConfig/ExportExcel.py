from array import array
import string
from types import CellType
import openpyxl
import os
import sys
import re

#当前工作目录
workpath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
templatescript = open(workpath + "/ConfigText/ConfigTemplate.txt" , mode = 'r' ,encoding = 'utf-8').read()
enity_export_path = workpath + "/EnityInitData"
workpath = workpath + "/Config/"



#配置文件data
class configdata:
    def __init__(self):
        #配置文件表的名称
        self.configname = ''
        #配置文件类型  id/item_name      
        self.configtype = []
        #配置文件描述  物品id/物品名称
        self.configdecription = []
        #配置文件中相关cell中值的类型
        self.configvaluetype = {}
        #配置文件内容
        self.configcontent = {}


def import_data (name):
    '''导入data'''
    excel_datas = []
    path = workpath + name
    wb = openpyxl.load_workbook(path)
    for sheet in wb:
        temp_config_name = sheet.title.strip()
        if temp_config_name.startswith('#'):
            print(f"当前表为描述表，不进行导出操作{temp_config_name}")
            continue


        data = configdata()
        data.configname = sheet.title.strip()
        for row in sheet.rows:
            for cell in row:
                #获取第一列的数据
                if cell.column == 1  and cell.value == 1:
                #如果有值，跳出本次循环
                    #print(f'跳出循环，当前行第一列有值')
                    break
                if cell.column == 2 and cell.row > 4 and not cell.value:
                    print(f"当前无id，不进行导出，configname:{data.configname},行数:{cell.row}")
                    break
                #移去第一行和第一列数据
                if cell.row != 1 and cell.column != 1:
                    #第二行数据为类型描述
                    if cell.row == 2:
                        data.configtype.append(cell.value)
                    elif cell.row == 3:
                        data.configdecription.append(cell.value)
                    elif cell.row == 4:
                    #用来对应列的数据   第二列在字典中 -> 0
                        data.configvaluetype[cell.column - 2] = cell.value
                    else:
                        
                        if not cell.row in data.configcontent:
                            data.configcontent[cell.row] = []
                        data.configcontent[cell.row].append(cell.value)
        excel_datas.append(data)
    return excel_datas


#data转换为config格式
def DataConvertConfig(data):
    #local module = {}
    tempscrpit = templatescript
    tempscrpit = tempscrpit.replace("表名",data.configname,-1)
    datadecription = '--'
    for decription in data.configdecription:
        datadecription += f"{decription},"
    tempscrpit = tempscrpit.replace("描述",datadecription,-1)
    creatdata = ''
    setdata = ''
    setdataindex = 1
    entity_data_name = f"{data.configname.lower()}_data"
    entity_wirte_text = f"\t\t\t\tlocal {entity_data_name} = ConfigHelper.GetConfig(ConfigName.{data.configname},id)\n"
    #所有的id
    all_keys = '{'
    for type in data.configtype:
        creatdata += f"\t\t\t\tdata.{type} = nil\n"
        setdata += f"\t\t\t\tdata.{type} = config[{setdataindex}]\n"
        entity_wirte_text += f"\t\t\t\tself.{type} = {entity_data_name}.{type}\n"
        setdataindex += 1
    tempscrpit = tempscrpit.replace("data初始化数据类型",creatdata,-1)
    tempscrpit = tempscrpit.replace("data中为所有数据赋值",setdata,-1)
    configcontent = ''
    for row in data.configcontent:
        dataindex = 0
        #当前的行数据
        line = ''
        length = len(data.configcontent[row]) - 1
        for value in data.configcontent[row]:
            value = getvaluetype(data,value,dataindex)
            #第一个数据 即为id
            if dataindex == 0:
                line += f'{data.configname}[{value}] = ' + '{'
                all_keys += f'{value},'
            if dataindex == length:
                line += f'{value}'
            else:
                line += f'{value},'
            dataindex += 1
        line += '}'
        #print(f'当前数据行为:{line}')
        configcontent += line + '\n'
    tempscrpit = tempscrpit.replace("配置文件中的所有值",configcontent)
    all_keys = all_keys[:-1]
    all_keys += '}'
    tempscrpit = tempscrpit.replace("所有keys",all_keys)

    #单独写入entity的配置文件
    with open(f'{enity_export_path}/{entity_data_name}.lua',mode = 'w',encoding = 'utf-8') as file:
        file.truncate(0)
        file.write(entity_wirte_text)

    return tempscrpit

#获取data的类型  index = 改value在数组中的索引，从0开始
def getvaluetype(data , value, valueindex):
    '''默认类型 int string float url int_array float_array string_array   int_table  float_table  string_table   int_dic  float_dic bool  bool_array'''
    
    valuetype =  data.configvaluetype[valueindex]
    if not value and valuetype == "bool":
        return 'false'
    if value == "FALSE":
        return 'false'
    if value == "0" or value == 0 :
        return 0

    
    if not value:
        return 'nil'
    if valuetype == "bool":
        return "true"
    if valuetype == "table":
        return value
    if valuetype == 'int' or valuetype == 'float':
        return value
    elif valuetype == 'string' or valuetype == 'url':
        return f"\"{value}\""
    elif valuetype == 'int_array' or valuetype == 'float_array':
        return value
    elif valuetype == 'string_array':
        value = value.replace('{','')
        value = value.replace('}','')
        temparray = str.split(value,',')
        resultvalue = '{'
        for temp in temparray:
            resultvalue += f'\"{temp}\",'
        resultvalue = resultvalue[:-1]
        resultvalue += '}'
        return resultvalue
    elif valuetype == 'int_table' or valuetype == 'float_table':
        resultvalue = '{'
        resultvalue += value
        resultvalue += '}'
        #直接返回
        return resultvalue
    elif valuetype == "string_table":
        '''给每一个字符增加""号'''
        #使用正则匹配挑出所有的单独table
        temparray = re.findall("{(.*?)}", value)
        resultvalue = '{'
        for temp in temparray:
            resultvalue += '{'
            string_temp = str.split(temp,',')
            for single_string in string_temp:
                resultvalue += f'\"{single_string}\",'
            resultvalue = resultvalue[:-1]
            resultvalue += '}'
        resultvalue += '}'
        return resultvalue
    elif valuetype == "int_dic" or valuetype == "float_dic":
        return value
    else:
        return value


