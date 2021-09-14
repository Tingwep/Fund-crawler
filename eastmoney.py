import tkinter as tk
from tkinter import *
import re
import requests
import json
import time

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
listbox1 = Listbox(root, width=20,height=s['height'])
listbox2 = Listbox(root, width=10,height=s['height'])
listbox3 = Listbox(root, width=10,height=s['height'])
listbox4 = Listbox(root, width=10,height=s['height'])
listbox5 = Listbox(root, width=10,height=s['height'])

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


def getInfo():  # 获取信息函数
    sum = 0

    for i in jine:

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
        print(search)

        # 遍历结果
        for j in search:
            data = json.loads(j)
            gsz = float(data['gsz']) - float(data['dwjz'])
            sy = gsz * float(jine[i])
            sy = '%.2f' % sy


            code_sy.append(sy)
            code_gsz.append((data['gsz']))
            code_data.append(data['gszzl'])
            gztime = data['gztime']
            GZtime = ""

            for l in gztime:
                if l == " ":
                    GZtime = ""
                else:
                    GZtime += l
            # print(GZtime)
            code_time.append(GZtime)
            code_name.append(data['name'])
            # print("基金:{},收益值:{},时间：".format(data['name'], data['gsz']),GZtime,sep='')
    for i in code_sy:
        sum += float(i)
    sum = '%.2f'%sum
    code_sy.append(sum)
    code_name.append('天天基金接口|总收益：')

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
