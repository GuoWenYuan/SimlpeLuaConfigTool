local DataTest = {}

DataTest.AllData = {}

function DataTest:Get(id)
	local data = self.AllData[id]
	if data then
		return data
	end
	if not DataTest[id] then
		print("没有找到:DataTest  中的:",id)
		return nil
	end
	data = {}
	local config = DataTest[id]
				data.id = config[1]
				data.desc = config[2]
				data.test_array = config[3]

	return data
end

--唯一id,描述,数组测试,

DataTest[1] = {1,12.33,{"你好","Hellow","hi"}}


DataTest.KEYS= {1}

return DataTest
