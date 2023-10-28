1.将需要添加的Excel放入Config中，可以在改路径下修改文件。
2.点击Build.bat，cmd命令执行完成之后会自动识别此次增加了/修改了哪些文件
3.所有的文件生成路径在ExportData中
4.Excel格式:第一行为空，不填写数据  第一列从数据行开始阶段若标记为1  则不导出当行数据
  	 第二行为变量名称
	 第三行为变量描述
	 第四行为变量类型 目前支持 默认类型 int string float url int_array float_array string_array   int_table  float_table  string_table  int_dic   float_dic   
	 其他为对应的值
	 注意：第一列有值的类型必须为int格式的id

5.各类型说明： 在弱脚本中 int = float = number    所以所有数字类的配置类型都填写  int即可  ，有小数点也无所谓
	      int string float url  bool不做说明
	      int_array = {1,1,1}           string_array = {n,n,n}
 	      int_table = {1,1,1},{2,2,2},{3,3,3}   string_array = {n,n,n},{m,m,m}
  	      int_dic = {{{1,1,1},{2,2,2}},{{3,3,3},{4,4,4}}}  以此类推 ~~~~~~
	      bool_array = {TRUE,FALSE,TRUE,FALSE}
	      string_dic 相关内容暂未提供，若有需要可添加 

6.打包及excel规则见Config中数据。