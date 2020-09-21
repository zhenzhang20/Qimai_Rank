通过python写脚本抓取七麦数据上Android应用在各大应用平台的下载量。


### 获取js代码

网络上有很多方法，不展开，最终获取信息如下：

```
function C(a, n) {
    a = a["split"]("");
    for (var t = a["length"], e = n["length"], r = "charCodeAt", i = 0; i < t; i++) a[i] = m(a[i][r](0) ^ n[(i + 10) % e][r](0));
    return a["join"]("")
}

function m(n) {
        var t = "fromCharCode";
        return String[t](n)
    }
    //上面是分析f(k)函数
    //下面是f(e)函数
    //函数v(n)就是f（e）函数的结果，m函数和上面的函数一样，只需要分析其中的n_fun函数的实现

function v(n) {
    return n_fun(encodeURIComponent(n)["replace"](/%([0-9A-F]{2})/g,
        function (a, n) {
            return m("0x" + n)
        }))
}

function n_fun(t) {
    var n;
    n = e_from(t.toString(), "binary") ;
    return q_fromByteArray(n) // 这一处的代码相当于 n.toString("base64")
}

function e_from(t_str, b) {
    var r = t_str.length;
    t = new Uint8Array(r);
    var i = t_write(t, t_str, b, r);
    return t
}

function t_write(t, e, b, r) {
    return K(W(e), t, 0, r)
}

function K(t, e, n, r) {
    for (var j = 0; j < r && !(j + n >= e.length || j >= t.length); ++j) e[j + n] = t[j];
    return j
}

function W(t) {
    for (var e = [], n = 0; n < t.length; ++n) e.push(255 & t.charCodeAt(n));
    return e
}
l = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9,+,/"
l = l.split(",")
function q_fromByteArray(t) {

    for (var e, n = t.length,
        r = n % 3,
        i = "",
        o = [], a = 16383, u = 0, c = n - r; u < c; u += a) o.push(s(t, u, u + a > c ? c : u + a));
    return 1 === r ? (e = t[n - 1], i += l[e >> 2], i += l[e << 4 & 63], i += "==") : 2 === r && (e = (t[n - 2] << 8) + t[n - 1], i += l[e >> 10], i += l[e >> 4 & 63], i += l[e << 2 & 63], i += "="),
        o.push(i),
        o.join("")
}

function s(t, e, n) {
    for (var r, i = [], o = e; o < n; o += 3) r = (t[o] << 16 & 16711680) + (t[o + 1] << 8 & 65280) + (255 & t[o + 2]),
        i.push(a(r));
    return i.join("")
}

function a(t) {
    return l[t >> 18 & 63] + l[t >> 12 & 63] + l[t >> 6 & 63] + l[63 & t]
}

function get0analysis(synct, params) {
    var g = new Date() - 1000 * synct;
    var e = new Date() - g - 1515125653845;
    var analy = [];
    var palist = [];
    for (var key in params) {
        palist.push(params[key])
    }
    var mm = palist["sort"]()["join"]("");
    var mmm = v(mm); //参数mm先执行f(e)函数
    var m_str1 = mmm + '@#/rank/indexPlus/brand_id/1@#57313212470@#1';
    var m_str0 = mmm + '@#/rank/indexPlus/brand_id/0@#57313212470@#0';
    var m_str2 = mmm + '@#/rank/indexPlus/brand_id/2@#57313212470@#2';
    var b_str = "00000008d78d46a";
    var r2 = v(C(m_str2, b_str));
    var r0 = v(C(m_str0, b_str));
    var r1 = v(C(m_str1, b_str)) ;
    analy.push(r0, r1, r2);
    return analy
}
```

### python下载脚本

```
# -*- coding:utf-8 -*-

import requests, execjs,json
import random
import time, os
import pandas as pd


user_agent = [
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
	"Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
    ]

headers = {
    "User-Agent": random.choice(user_agent),
    'Origin': 'https://www.qimai.cn',
    'Referer': 'https://www.qimai.cn/rank',
    "Accept": "application/json,text/plain,*/*",
}

params = {'brand': 'all',
          'country': 'cn',
          'device': 'iphone',
          'genre': '5000',
          'date': '2020-8-31',
          'page': 2
          }

TRY_TIMES = 10

def getAnalysis():
    resp = requests.get('https://www.qimai.cn/rank', headers=headers, verify=False)
    t = resp.cookies.get_dict()
    synct = t.get('synct')#时间
    print("current time is : " + synct)
    ana = getanaly(synct)
    return ana


def getanaly(synct):
    js_path = "qimai.js"
    try:
        new_pwd = "dummy"
        with open(js_path, 'r',encoding='utf8') as f:
            js_content = f.read()
            ctx = execjs.compile(js_content)
            new_pwd = ctx.call("get0analysis", synct, params)
    except Exception as ex:
        print("Exception when run js file....., will return dummy pwd")
    finally:
        print("getanaly result is: ", new_pwd)
        return new_pwd

def check_ana_valid(ana):
    params['analysis'] = ana[0]
    print("params['analysis'] = " + params['analysis'] )
    # params['analysis'] = ana
    # print("params['analysis'] = " + params['analysis'])
    url = 'https://api.qimai.cn/userRequest/index?'
    # print(url)
    res = requests.get(url=url,headers=headers,params=params)
    # print("check_ana_valid res.text: ", res.text)
    try:
        resjson = json.loads(res.text)
        print("check ana result: " , resjson)
        return(resjson)
    except Exception as ex:
        return""


def check_specifykey_specifymarket_exist(ana, market, searchkey):
    params['analysis'] = ana[1]
    params['market'] = market #'6'
    params['search'] = searchkey # '每团‘

    url = 'https://api.qimai.cn/search/checkHasBundleId?'
    print(url)
    res = requests.get(url=url,headers=headers,params=params)
    print("check_specifykey_specifymarket_exist res.txt: "+ res.text)
    try:
        resjson = json.loads(res.text)
        print(resjson)
        return (resjson)
    except Exception as ex:
        return ""



# 查询pagenum页信息
def search_specifykey_specifymarket(ana, market, searchkey, outfilename, keys, pagenum):
    params['analysis'] = ana[1]
    params['market'] = market #'6'
    params['search'] = searchkey # '每团‘
    for i in range(1,pagenum):
        params['page'] = i
        url = 'https://api.qimai.cn/search/android?'
        print(url)
        print("params: %s" % str(params))
        res = requests.get(url=url,headers=headers,params=params)
        print("search_specifykey_specifymarket res.txt: "+ res.text)
        try:
            resjson = json.loads(res.text)
            print(resjson)
            if str(resjson).strip() == '' or str(resjson).strip().find("10602") != -1:
                ana = getAna(TRY_TIMES)
                search_specifykey_specifymarket(ana, market, searchkey, outfilename, keys, pagenum)
            else:
                if not resjson.get('appList') is None:
                    print(resjson.get('appList')[0])
                    save_json_to_file(outfilename, resjson, keys)
        except Exception as ex:
            return ""



# save json data to file
# keys is filter, if keys value exist, don't save
def save_json_to_file(outfilename, jsondata, keys):
    with open(outfilename, 'a+', encoding='UTF-8') as f:
        f.seek(0)
        lines = f.read().splitlines()
        EXIST = False
        newline = str(jsondata).strip()
        try:
            newlinedict = eval(newline)
        except Exception as ex:
            newlinedict = {}
            print("newline is :" + newline)
        if len(lines) == 0:
            f.writelines(newline + '\n')
        else:
            if not EXIST:
                for line in lines:
                    try:
                        linedict = eval(line)
                    except Exception as ex:
                        continue
                    for key in keys:
                        cont = linedict.get(key)
                        cont_newline = newlinedict.get(key)

                        if not cont_newline == cont:
                            EXIST = False
                            break
                        EXIST = True
            if not EXIST:
                f.writelines(newline + '\n')


def download(searchkey, markets, capture_page_numbers):
    ana = getAna(TRY_TIMES)
    # 共10个android应用市场
    # markets = {'360': '1', '百度': '2', '应用宝': '3', '小米': '4', '豌豆荚': '5', '华为': '6', '魅族': '7', 'VIVO': '8', 'OPPO': '9',
    #            'gogoleplay': '10'}  #共10个android应用市场
    for market_name in markets.keys():
        market_id = markets.get(market_name)
        # jsondata2 = check_specifykey_specifymarket_exist(ana, market, searchkey)
        # save_json_to_file("test.txt", jsondata2, ["code", "msg"])
        outfilename = searchkey + "_market_" + market_name + ".txt"
        search_specifykey_specifymarket(ana, market_id, searchkey, outfilename, [], capture_page_numbers)


def getAna(trytimes):
    ana = getAnalysis()
    jsondata1 = check_ana_valid(ana)
    # newline = str(jsondata1).strip()
    while str(jsondata1).strip() == '' or str(jsondata1).strip().find("10602") != -1:
        if str(jsondata1).strip().find('Access Error') != -1:
            print("Current try time is No.: ", str(TRY_TIMES - trytimes), ". Please wait 10 secs")
            time.sleep(10)
        elif str(jsondata1).strip().find('请半小时后重试') != -1:
            print("Current try time is No.: ", str(TRY_TIMES - trytimes), ". Please wait 30 mins")
            time.sleep(1850)
        ana = getAnalysis()
        jsondata1 = check_ana_valid(ana)
        trytimes -= 1
        if trytimes == 0:
            break
    save_json_to_file("check_ana_valid.txt", jsondata1, ["code", "msg"])
    return ana


def json_to_excel(text):
    df = pd.DataFrame()  # 最后转换得到的结果
    df1 = pd.DataFrame([text])
    df = df.append(df1)
    df.to_excel('data.xlsx', sheet_name='Data', startcol=0, index=False)


def json_file_cont_to_excel_special(inputdata, outputfile):
    print("will generate {outputfile} base on {inputdata}".format(outputfile=outputfile,inputdata=inputdata))
    data = []  # 用于存储每一行的数据
    with open(inputdata, 'r', encoding='UTF-8') as fr:
        for line in fr:
            data.append(line)
    df = pd.DataFrame()  # 最后转换得到的结果
    for line in data:
        #每行的数据转为json格式，再转为dataframe格式
        line_json = eval(line)
        applist_cont_list = line_json.get('appList')
        for i in applist_cont_list:
            info = {}
            if 'appInfo' in i.keys():
                info.update(i.get('appInfo'))
            if 'company' in i.keys():
                info.update(i.get('company'))
            if 'rankInfo' in i.keys():
                info.update(i.get('rankInfo'))
            df1 = pd.DataFrame(info,index=[0])
            # df1 = pd.DataFrame.from_dict(info,orient='index').T
            df = df.append(df1)
    sheet_name = inputdata[:inputdata.find('.')]
    df.to_excel(outputfile, sheet_name=sheet_name, startcol=0, index=False)
    print("generated {outputfile} base on {inputdata} finish".format(outputfile =outputfile,inputdata=inputdata))


def convert_result_to_one_excel(excelfilename):
    list_file = os.listdir('./')
    write = pd.ExcelWriter(excelfilename)
    for contentfile in list_file:
        name = os.path.splitext(contentfile)[0]
        suffix = os.path.splitext(contentfile)[1]
        if suffix == '.txt' and name.find('_market') != -1:
            json_file_cont_to_excel_special(contentfile, write)
    write.save()

def convert_result_to_multi_excels():
    list_file = os.listdir('./')
    for contentfile in list_file:
        name = os.path.splitext(contentfile)[0]
        suffix = os.path.splitext(contentfile)[1]
        if suffix == '.txt' and name.find('_market') != -1:
            output_excel_name = name + '.xls'
            json_file_cont_to_excel_special(contentfile, output_excel_name)

if __name__ == "__main__":
    searchkeys = ['拜佛', '佛教']
    markets = {'360': '1', '百度': '2', '应用宝': '3', '小米': '4', '豌豆荚': '5', '华为': '6', '魅族': '7', 'VIVO': '8', 'OPPO': '9',
               'gogoleplay': '10'}  # 共10个android应用市场

    capture_page_numbers = 5
    for searchkey in searchkeys:
        download(searchkey, markets, capture_page_numbers)


    out_excel_filename = "android.xls"
    convert_result_to_one_excel(out_excel_filename)
    # convert_result_to_multi_excels()


```

### 运行日志信息及最终结果展示

#### 日志:

![](https://github.com/zhenzhang20/zhenzhang20.github.io/tree/master/2020/09/17/2020-09-17-Spider-Qimai-Rank/2020-09-16-qimai_full_log.png)

#### 结果文件

![](https://github.com/zhenzhang20/zhenzhang20.github.io/tree/master/2020/09/17/2020-09-17-Spider-Qimai-Rank/2020-09-16-qimai_sample_result_file.png)

#### txt结果内容示例

```
{'code': 10000, 'msg': '成功', 'isActualAndroid': 0, 'wechatList': [], 'isSearch': True, 'totalNum': '20', 'maxPage': 1, 'offlineAppInfo': False, 'appList': [{'appInfo': {'appId': '164404', 'appName': '拜佛', 'icon': 'https://static-cdn.qimai.cn/pic/view/type/android/source/aHR0cDovL3AyLnFoaW1nLmNvbS90MDE5ZjU2NTY3YWNkZmZjMmFmLndlYnA=', 'publisher': '深圳市功德文化有限公司', 'comment_score': 1, 'comment_count': 260, 'version_time': '2020-06-23', 'app_download_num': '196454'}, 'genre': '常用工具', 'isMyApp': 0, 'company': {'id': '11863', 'name': '深圳市聚英杰科技有限公司'}, 'rankInfo': {'ranking': 0, 'change': 0, 'genre': '游戏'}}, {'appInfo': {'appId': '132294', 'appName': '怀恩菩提心', 'icon': 'https://static-cdn.qimai.cn/pic/view/type/android/source/aHR0cDovL3AyLnFoaW1nLmNvbS90MDE0NzVkNjRhMGRhM2M2Njc0LndlYnA=', 'publisher': '上海怀恩网络科技有限公司', 'comment_score': 1, 'comment_count': 664, 'version_time': '2019-12-11', 'app_download_num': '362645'}, 'genre': '常用工具', 'isMyApp': 0, 'company': {'id': '49880', 'name': '上海怀恩网络科技有限公司'}, 'rankInfo': {'ranking': 0, 'change': 0, 'genre': '游戏'}}, {'appInfo': {'appId': '132096', 'appName': '修行者', 'icon': 'https://static-cdn.qimai.cn/pic/view/type/android/source/aHR0cDovL3AyLnFoaW1nLmNvbS90MDE2OTUxNmM5YTZjNWVhNzdjLndlYnA=', 'publisher': '广东灵机文化传播有限公司', 'comment_score': 0.9, 'comment_count': 169, 'version_time': '2018-07-19', 'app_download_num': '693930'}, 'genre': '生活服务', 'isMyApp': 0, 'company': {'id': '863', 'name': '广东亿俊计算机系统有限公司'}, 'rankInfo': {'ranking': 0, 'change': 0, 'genre': '游戏'}}]}

```



#### excel结果内容示例

https://github.com/zhenzhang20/zhenzhang20.github.io/tree/master/2020/09/17/2020-09-17-Spider-Qimai-Rank/2020-09-16-qimai_sample_result_excel.png


### 说明

1. 下载后，会根据关键字、平台把结果存入多个不同的txt文件中
2. 方便查看，最后会把txt格式转为excel格式：可以通过调整下面代码实现把结果存放到同一个excel或多个分开的excel


```
    #存到同一个excel文件
    convert_result_to_one_excel(out_excel_filename)
    #存到多个分开的excel文件
    convert_result_to_multi_excels()
```


3. 经常会下载是获取不到信息，多等一段时间即可。同时发现，没有获取到正确的analysis亦可爬取到结果

[Fork/Star on Github](https://github.com/zhenzhang20/Qimai_Rank)

