运行需要以下两个文件

1、INI.JSON
 
可修改几个GUI参数 
{
"alpha": "0.3",  # 透明度   
"width": "420", # GUI宽度   
"height": "190" # GUI高度 
}  

2、fene.json
 
填入基金代码与持有份额，用于计算收益 
{    
"xxx这里填基金代码": "xxx这里填持有份额",   
"xxx这里填基金代码": "xxx这里填持有份额", 
}

找到了解决蚂蚁基金接口获取历史净值的提交方式，去掉了原来用天天基金接口获取昨日净值的方法。
