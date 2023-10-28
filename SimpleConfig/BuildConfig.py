import os
import ExportExcel
import CompareConfig
import sys

ConfigOutPath =os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))) + "/ExprotData/"

def UpdateConfig():
    #获取要更新的excel
    updateExcel = CompareConfig.GetUpdateOrAddExcel()
    for data in updateExcel:
        print(f"当前更新的表为:{data.name}")
        configDatas = ExportExcel.import_data(data.name)
        for configdata in configDatas:
            fileName = configdata.configname
            config = ExportExcel.DataConvertConfig(configdata)
            with open(f'{ConfigOutPath}{fileName}.lua',mode = 'w',encoding = 'utf-8') as file:
                file.truncate(0)
                file.write(config)
        

UpdateConfig()