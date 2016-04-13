from requests import post
from bs4 import BeautifulSoup
from os import system
from selenium.webdriver import PhantomJS
from sys import argv
from re import search


def addOption(a, n, b):  # 参数,空格数,描述
    '''排版用'''
    spaceStr = ''
    for i in range(n - len(a)):
        spaceStr += ' '
    print(a + spaceStr + b)


class information(object):

    def __init__(self):
        system('color a')

    def showInfo(self):
        print('*******************************')
        print('*     查询百度权重,谷歌PR;     *')
        print('*     可筛选权重,谷歌PR值;      *')
        print('*     频繁查询会暂时封ip      *')
        print('*   经测试每小时上限50次查询 *')
        print('*               作者:Evi1m1   *')
        print('*                2016.4.11    *')
        print('*******************************')
        print("==============================>>>请输入'seo -h'查看帮助!")

    def showHelp(self):
        spaceNum = 10  # 控制help的空格数
        addOption('-h', spaceNum, '查看帮助文档')
        addOption('-u', spaceNum, '查询单个url')
        addOption('-r', spaceNum, '导入txt文件批量查询')
        addOption('-d', spaceNum, '导入文件')
        addOption('-qn', spaceNum, '过滤参数,显示百度权重大于n的url')
        addOption('-pn', spaceNum, '过滤参数,显示谷歌PR大于n的url')
        self.showExample()

    def showExample(self):
        spaceNum = 45  # 控制example的空格数
        print("For example:")
        addOption("seo -u 'www.taobao.com'", spaceNum, "单个查询淘宝信息")
        addOption("seo -r 'D:\\urls.txt'", spaceNum, "批量查询txt文件中url信息")
        addOption("seo -r 'D:\\urls.txt' -qn 4", spaceNum, "批量查询并筛选百度权重大于4的url")
        addOption("seo -r 'D:\\urls.txt' -pn 1234", spaceNum, "指量筛选谷歌PR大于1233的url")
        addOption("seo -r 'urls.txt' -qn 4 -pn 123", spaceNum, "同时筛选权重和收录")
        addOption("seo -r 'urls.txt' -qn 4 -d 'D:\\t.txt'", spaceNum, "筛选结果后导出到某文件")


class toolSeo(object):

    def __init__(self):
        self.spaceNum = 25  # 全局控制数字
        self.bdqzs = {}  # 百度权重
        self.bdsls = {}  # 谷歌PR

    def onebaiduQz(self, url):
        '''返回单个权重'''
        qzUrl = 'http://rank.chinaz.com/'  # 百度权重查询地址
        payload = {'host': url}
        req = post(qzUrl, data=payload)
        soup = BeautifulSoup(req.text, "lxml")
        try:
            qz = soup.find_all(id='br')[0].string  # 百度权重值
        except:
            divs = soup.find_all(class_='errormsg')[0].stripped_strings  # 查询异常
            for msg in divs:
                qz = msg
        return qz  # 字符

    def onegoogolePR(self, url):
        '''返回单个PR'''
        prUrl = 'http://pr.chinaz.com'  # 谷歌PR查询地址
        driver = PhantomJS()
        driver.get(prUrl)
        driver.find_element_by_id('PRAddress').send_keys(url)
        driver.find_element_by_class_name('search-write-btn').click()
        try:
            imgsrc = driver.find_element_by_css_selector('span#pr>img').get_attribute('src')
            pr = search(r'\d', imgsrc).group()
        except:
            pr = '暂无数据'
        driver.quit()
        return pr

    def onebaidu(self, url):
        qz = self.onebaiduQz(url)
        pr = self.onegoogolePR(url)
        msg = '百度权重: ' + qz + ' 谷歌PR: ' + pr
        addOption(url, self.spaceNum, msg)

    def manybaidu(self, doc, qn=-1, pn=-1):
        '''读取文件查询循环查询权重'''
        try:
            with open(doc, 'r', encoding='utf-8') as f:
                urls = f.readlines()
            qn = int(qn)
            pn = int(pn)
            for url in urls:
                url = url.strip()
                if url is not '':  # 防止文件结尾有空换行影响查询次数
                    qz = self.onebaiduQz(url)
                    pr = self.onegoogolePR(url)
                    if qn < 0 and pn < 0:  # 说明执行-r命令
                        msg = '百度权重: ' + qz + ' 谷歌PR: ' + pr
                        addOption(url, self.spaceNum, msg)
                    else:  # 执行过滤命令
                        try:
                            if int(qz) >= qn and int(pr) >= pn:  # 权重收录双过滤
                                msg = '百度权重: ' + qz + ' 谷歌PR: ' + pr
                                addOption(url, self.spaceNum, msg)
                            else:
                                if int(qz) >= qn and pn < 0:  # 过滤权重
                                    msg = '百度权重: ' + qz + ' 谷歌PR: ' + pr
                                    addOption(url, self.spaceNum, msg)
                                elif int(pr) >= pn and qn < 0:  # 过滤收录
                                    msg = '百度权重: ' + qz + ' 谷歌PR: ' + pr
                                    addOption(url, self.spaceNum, msg)
                        except:  # 权重获取得到错误信息无法转int排除
                            pass
        except Exception as e:
            print(e, '\n请检查输入!')


if __name__ == '__main__':
    info = information()
    bd = toolSeo()
    if len(argv) == 1:
        info.showInfo()
        system('cmd')
    elif '-h' in argv:
        info.showHelp()
    else:
        argn = len(argv)
        if '-u' in argv:
            '''查询单个url'''
            pos = argv.index('-u') + 1
            bd.onebaidu(argv[pos])
        elif '-r' in argv:
            '''指量查询'''
            pos1 = argv.index('-r') + 1
            if '-qn' in argv and '-pn' in argv:
                pos2 = argv.index('-qn') + 1
                pos3 = argv.index('-pn') + 1
                bd.manybaidu(argv[pos1], qn=argv[pos2], pn=argv[pos3])
            elif '-qn' in argv and '-pn' not in argv:
                '''查百度权重'''
                pos2 = argv.index('-qn') + 1
                bd.manybaidu(argv[pos1], qn=argv[pos2])
            elif '-pn' in argv and '-qn' not in argv:
                '''查谷歌PR'''
                pos3 = argv.index('-pn') + 1
                bd.manybaidu(argv[pos1], pn=argv[pos3])
            else:
                '''不过滤查询'''
                if len(argv) == 3:
                    bd.manybaidu(argv[pos1])
                else:
                    print("未识别命令,请查看帮助文档!")
        else:
            print("未识别命令,请查看帮助文档!")
