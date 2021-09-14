import datetime
import tkinter as tk
from tkinter import *
import re
import requests
import json
import time

data = {}
sy = []


todaysDate = (datetime.date.today() + datetime.timedelta()).strftime("%Y-%m-%d")
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

with open(r'fene.json', 'r') as f:
    for line in f:
        jine = json.loads(line)

with open("INI.JSON", encoding="utf-8") as f:
    s = json.load(f)  # 加载

# 创建主体窗口程序
root = tk.Tk()
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

geometry = s['width'] + 'x' + s['height']
root.geometry('%dx%d+%d+%d' % (
    int(s['width']), int(s['height']), (screenwidth - int(s['width'])) / 2, (screenheight - int(s['height'])) / 2))

root.window_size = geometry
# root.geometry("200x220+1079+519")   # 右下角
root.attributes("-alpha", s['alpha'])
# root.configure(background='red')
root.overrideredirect(1)
root.wm_attributes('-topmost', True)

# 创建Listbox控件
listbox1 = Listbox(root, width=20)
listbox2 = Listbox(root, width=10)
listbox3 = Listbox(root, width=10)
listbox4 = Listbox(root, width=10)
listbox5 = Listbox(root, width=10)

listbox1.pack(side=LEFT)
listbox5.pack(side=RIGHT)
listbox2.pack(side=RIGHT)
listbox4.pack(side=RIGHT)
listbox3.pack(side=RIGHT)

# 定义数组
code_name = []
code_data = []
code_time = []
code_gsz = []
code_sy = []
# 读入基金代码
result = []
# 读入份额
fun = {}

'''jzrq净值日期 dwjz当日净值 gsz净值估算 gszzl估算涨跌百分比'''
Header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}


# 获取昨天的单位净值
def danweijingzhi(cookie_data,i):
    url = "http://www.fund123.cn/api/fund/queryFundHistoryNetValueList?_csrf=%s" % cookie_data['csrf']
    headers = {"Host": "www.fund123.cn",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
               "Content-Type": "application/json",
               "Cookie": cookie_data['cookie'],
               "accept": "json",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9"
               }
    payload = {"productId": cookie_data['productId'],
               "startDate": (datetime.date.today() + datetime.timedelta(days=-7)).strftime("%Y%m%d"),
               "endDate": (datetime.date.today() + datetime.timedelta()).strftime("%Y%m%d"),
               "pageNum": 1, "pageSize": 10}
    res = requests.post(url, json=payload, headers=headers).text
    history = json.loads(res)

    return history['list'][i]["netValue"]


# 从入口获取cookie、基金基本信息
def cookie(code):
    cookie_data = {}
    url = "http://www.fund123.cn/matiaria?fundCode=" + code
    res = requests.get(url, headers=Header)

    # 将接口传回信息转换为json格式
    res_text = res.text
    pattern = r'context =(.*);</script>'
    resutlt = re.compile(pattern)
    search = resutlt.findall(res_text)[0]
    data = json.loads(search)

    # 从接口返回信息
    productId = data['materialInfo']['productId']  # 基金Id
    netValue = data['materialInfo']['titleInfo']['netValue']  # 最新净值
    date = data['materialInfo']['titleInfo']['netValueDate'] # 净值日期
    name = data['materialInfo']['fundBrief']['fundNameAbbr']  # 基金名称
    csrf = data["csrf"]  # csrf_token
    cookie = res.cookies  # cookie

    cookie = requests.utils.dict_from_cookiejar(cookie)  # cookie格式化为字典形式
    cookie_content = "ALIPAYJSESSIONID=" + cookie['ALIPAYJSESSIONID'] + ";ctoken=" + cookie['ctoken']  # 拼接后的cookie

    # 将信息压入字典中
    cookie_data['productId'] = productId
    cookie_data['csrf'] = csrf
    cookie_data['cookie'] = cookie_content
    cookie_data['netValue'] = netValue
    cookie_data['name'] = name
    cookie_data['date'] = date

    return cookie_data

# 获取估算净值
def getdata(cookie_data):
    forecast = {}
    url = "http://www.fund123.cn/api/fund/queryFundEstimateIntraday?_csrf=%s" % cookie_data['csrf']
    payloadHeader = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Content-Type": "application/json", 'cookie': cookie_data['cookie']}

    # payload data
    data["startTime"] = todaysDate
    data["endTime"] = tomorrow
    data["limit"] = 200
    data["productId"] = cookie_data['productId']
    data["format"] = "true"
    data["source"] = "WEALTHBFFWEB"

    payloadData = json.dumps(data)
    res = requests.post(url=url, data=payloadData, headers=payloadHeader)
    res_text = json.loads(res.text)

    forecastGrowth = res_text['list'][-1]['forecastGrowth']  # 估算涨幅
    forecastNetValue = res_text['list'][-1]['forecastNetValue']  # 估算净值

    forecast['forecastGrowth'] = forecastGrowth
    forecast['forecastNetValue'] = forecastNetValue

    return forecast

# 处理数据
def getInfo():
    sum = 0  # 初始化总收益

    for i in jine:
        # 接收数据
        cookie_res = cookie(i)
        Info = getdata(cookie_res)

        if (cookie_res['date'] != time.strftime("%m-%d", time.localtime()) and int(time.strftime("%H", time.localtime())) < 9) or (cookie_res['date'] == time.strftime("%m-%d", time.localtime()) ) :
            # 获取昨天的单位净值
            dwjz = danweijingzhi(cookie_res,1)
            gsz = float(cookie_res['netValue']) - float(dwjz)  # 估算值
        else:
            dwjz = danweijingzhi(cookie_res, 0)
            gsz = float(Info['forecastNetValue']) - float(dwjz)  # 估算值

        gszzl = float(Info['forecastGrowth']) * 100  # 估算涨幅转换
        now = time.strftime("%H:%M", time.localtime())  # 格式化当前日期
        income = '%.2f' % (gsz * float(jine[i]))  # 收益

        # 数据压入
        code_gsz.append('%.4f' % float(Info['forecastNetValue']))
        code_sy.append(income)
        code_time.append(now)
        code_name.append(cookie_res['name'])
        code_data.append('%.2f' % float(gszzl))
        sy.append(income)

    # 计算总收益
    for i in code_sy:
        sum += float(i)
    sum = '%.2f' % sum
    code_sy.append(sum)
    code_name.append('蚂蚁基金接口|总收益：')


def button_1(event):  # 双击鼠标检测函数
    global x, y
    x, y = event.x, event.y
    # print("event.x, event.y = ", event.x, event.y)
    print("已退出")
    root.destroy()


def move(event):
    """窗口移动事件"""
    global x, y
    x, y = 40, 40
    new_x = (event.x - x) + root.winfo_x()
    new_y = (event.y - y) + root.winfo_y()
    s = f"{root.window_size}+{new_x}+{new_y}"
    root.geometry(s)


def topWin():  # 窗体置顶函数
    tp = Toplevel(root)
    tp.attributes('-topmost', True)


def clear_data():  # 清空列表原始数据
    code_name.clear()
    code_data.clear()
    code_time.clear()
    code_gsz.clear()
    code_sy.clear()


def f5():  # 递归刷新控件

    clear_data()
    print("开始获取信息")
    getInfo()
    print("成功获取信息")
    listbox5.delete(0, END)
    listbox4.delete(0, END)
    listbox3.delete(0, END)
    listbox2.delete(0, END)
    listbox1.delete(0, END)
    for i in range(len(code_name)):
        listbox1.insert(END, code_name[i])
    for i in range(len(code_data)):
        listbox2.insert(END, code_data[i])
    for i in range(len(code_time)):
        listbox3.insert(END, code_time[i])
    for i in range(len(code_gsz)):
        listbox4.insert(END, code_gsz[i])
    for i in range(len(code_sy)):
        listbox5.insert(END, code_sy[i])
    # while True:
    time.sleep(1)
    root.after(60000, f5)
    print("开始刷新")
    print('刷新成功')


# 监听事件
root.bind("<B1-Motion>", move)
root.bind("<Double-Button-1>", button_1)

# root.after(5000,f5)
f5()
root.mainloop()
