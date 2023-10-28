local Test = {}

Test.AllData = {}

function Test:Get(id)
	local data = self.AllData[id]
	if data then
		return data
	end
	if not Test[id] then
		print("没有找到:Test  中的:",id)
		return nil
	end
	data = {}
	local config = Test[id]
				data.id = config[1]
				data.desc = config[2]
				data.test_array = config[3]

	return data
end

--唯一id,描述,数组测试,

Test[1] = {1,"我是测试表的描述",{1,1,1}}


Test.KEYS= {1}

return Test
