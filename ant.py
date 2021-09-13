import datetime
import tkinter as tk
from tkinter import *
import re
import requests
import json
import time

# 读入基金代码
result = []
# 读入份额
fun = {}
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

with open(r'fene.json', 'r') as f:
    for line in f:
        jine = json.loads(line)

'''jzrq净值日期 dwjz当日净值 gsz净值估算 gszzl估算涨跌百分比'''
Header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}


def danweijingzhi(i):
    url = "http://fundgz.1234567.com.cn/js/%s.js" % i
    # print(url)
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text
    # 正则表达式
    pattern = r'^jsonpgz\((.*)\)'
    # 查找结果
    search = re.findall(pattern, content)

    # 遍历结果
    for j in search:
        data = json.loads(j)
        dwjz = float(data['dwjz'])

    return dwjz


def cookie(code):
    cookie_data = {}
    url = "http://www.fund123.cn/matiaria?fundCode=" + code
    res = requests.get(url, headers=Header)

    res_text = res.text
    pattern = r'context =(.*);</script>'
    resutlt = re.compile(pattern)
    search = resutlt.findall(res_text)[0]
    data = json.loads(search)

    productId = data['materialInfo']['productId']
    netValue = data['materialInfo']['titleInfo']['netValue']
    name = data['materialInfo']['fundBrief']['fundNameAbbr']
    csrf = data["csrf"]
    cookie = res.cookies

    cookie = requests.utils.dict_from_cookiejar(cookie)
    cookie_content = "ALIPAYJSESSIONID=" + cookie['ALIPAYJSESSIONID'] + ";ctoken=" + cookie['ctoken']

    cookie_data['productId'] = productId
    cookie_data['csrf'] = csrf
    cookie_data['cookie'] = cookie_content
    cookie_data['netValue'] = netValue
    cookie_data['name'] = name

    dwjz = danweijingzhi(code)

    cookie_data['dwjz'] = dwjz
    return cookie_data

def getdata(cookie_data):
    forecast = {}
    url = "http://www.fund123.cn/api/fund/queryFundEstimateIntraday?_csrf=%s" % cookie_data['csrf']
    # print(url)
    # 浏览器头

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

    forecastGrowth = res_text['list'][-1]['forecastGrowth']
    forecastNetValue = res_text['list'][-1]['forecastNetValue']

    forecast['forecastGrowth'] = forecastGrowth
    forecast['forecastNetValue'] = forecastNetValue

    return forecast

def getInfo():  # 获取信息函数
    sum = 0

    for i in jine:
        cookie_res = cookie(i)
        Info = getdata(cookie_res)
        forecast = {}
        url = "http://www.fund123.cn/api/fund/queryFundEstimateIntraday?_csrf=%s" %  cookie_res['csrf']
        # print(url)
        # 浏览器头

        payloadHeader = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Content-Type": "application/json", 'cookie': cookie_res['cookie']}

        # payload data
        data["startTime"] = todaysDate
        data["endTime"] = tomorrow
        data["limit"] = 200
        data["productId"] =  cookie_res['productId']
        data["format"] = "true"
        data["source"] = "WEALTHBFFWEB"

        payloadData = json.dumps(data)
        res = requests.post(url=url, data=payloadData, headers=payloadHeader)
        res_text = json.loads(res.text)

        forecastGrowth = res_text['list'][-1]['forecastGrowth']
        forecastNetValue = res_text['list'][-1]['forecastNetValue']

        forecast['forecastGrowth'] = forecastGrowth
        forecast['forecastNetValue'] = forecastNetValue

        gsz = float(Info['forecastNetValue']) - float(cookie_res['dwjz'])

        gszzl = 1 - float(forecastNetValue) - float(cookie_res['netValue'])
        now = time.strftime("%H:%M", time.localtime())
        income = '%.2f' % (gsz * float(jine[i]))

        code_gsz.append('%.2f'%float(forecastNetValue))
        code_sy.append(income)
        code_time.append(now)
        code_name.append(cookie_res['name'])
        code_data.append('%.2f'%float(gszzl))

        sy.append(income)
    for i in code_sy:
        sum += float(i)
    sum = '%.2f'%sum
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
