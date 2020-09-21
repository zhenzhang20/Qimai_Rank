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
          'date': '2019-10-31',
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
    with open(js_path, 'r',encoding='utf8') as f:
        js_content = f.read()
        ctx = execjs.compile(js_content)
        new_pwd = ctx.call("get0analysis", synct, params)
        print(new_pwd)
        return new_pwd


def check_ana_valid(ana):
    params['analysis'] = ana[0]
    print("params['analysis'] = " + params['analysis'] )
    # params['analysis'] = ana
    # print("params['analysis'] = " + params['analysis'])
    url = 'https://api.qimai.cn/userRequest/index?'
    print(url)
    res = requests.get(url=url,headers=headers,params=params)
    print("check_ana_valid res.text: ", res.text)
    try:
        resjson = json.loads(res.text)
        print(resjson)
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
            print("Try : ", str(100 - trytimes))
            time.sleep(10)
        elif str(jsondata1).strip().find('请半小时后重试') != -1:
            print("Try : ", str(100 - trytimes))
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
    searchkeys = ['佛经', '佛', '佛教', '拜佛', '佛法', '地藏', '观音']
    markets = {'360': '1', '百度': '2', '应用宝': '3', '小米': '4', '豌豆荚': '5', '华为': '6', '魅族': '7', 'VIVO': '8', 'OPPO': '9',
               'gogoleplay': '10'}  # 共10个android应用市场

    capture_page_numbers = 5
    for searchkey in searchkeys:
        download(searchkey, markets, capture_page_numbers)


    out_excel_filename = "android.xls"
    convert_result_to_one_excel(out_excel_filename)
    # convert_result_to_multi_excels()


# 错误信息：
# {'code': 10602, 'msg': 'Access Error'}
# {'code': 10602, 'msg': '当前网络或账号异常，请半小时后重试'}

# 正常信息：
# {'code': 10000, 'msg': '记录成功'}
#
# {'code': 10001, 'msg': '未获取到相关app'}
# {'code': 10000, 'msg': '成功', 'isActualAndroid': 0, 'offlineAppInfo': False, 'appList': [{'appInfo': {'appId': '4719824', 'appName': '博真美食', 'icon': 'https://appimg.dbankcdn.com/hwmarket/files/application/icon144/3cf292005b8b44efa8d0d154c3e2b387.png', 'publisher': '天津博真电子商务有限公司', 'comment_score': 0, 'comment_count': 0, 'version_time': '2019-09-29', 'app_download_num': '10000'}, 'genre': '', 'isMyApp': 0, 'company': {'id': 0, 'name': '天津博真电子商务有限公司'}, 'rankInfo': {'ranking': 0, 'change': 0, 'genre': '应用'}}, {'appInfo': {'appId': '151821', 'appName': '威海八爪团', 'icon': 'https://appimg.dbankcdn.com/hwmarket/files/application/icon144/677fd13874cf4e4ba052e6f3914427d5.png', 'publisher': '威海新正网络技术有限公司', 'comment_score': 2, 'comment_count': 12, 'version_time': '2020-05-07', 'app_download_num': '60000'}, 'genre': '', 'isMyApp': 0, 'company': {'id': '54825', 'name': '威海新正网络技术有限公司'}, 'rankInfo': {'ranking': 0, 'change': 0, 'genre': '应用'}}]}
 
# 运行报错
# FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory