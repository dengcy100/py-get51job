# encoding=utf8
import requests
from html.parser import HTMLParser

class Myparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.infos = []
        self.flag = False
        self.count = 0
        self.placeflag = False
        self.salaryflag = False
        self.dateflag = False
        self.company = ""
        self.info = {}

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
            return None

        if tag=="p":
            self.count += 1
        if tag=="em":
            self.count += 1
        if tag=="input":
            self.count += 1
        if tag=="span":
            self.count += 1
        if tag=="a":
            self.count += 1
        #print("handle_starttag>" + tag + ">" + str(self.count) + ">" + str(attrs)+str(self.dateflag))
        if len(attrs)>=2 and tag=="a" and self.count == 14:
            #print("公司："+attrs[1][1])
            self.company = attrs[1][1]
        else:
            self.company = ""
        if self.count == 13 and _attr(attrs,"class")=="t3":
            self.placeflag = True
        if self.count == 13 and _attr(attrs,"class")=="t4":
            self.salaryflag = True
        if self.count == 13 and _attr(attrs,"class")=="t5" and self.flag == True:
            self.dateflag = True

    def handle_endtag(self, tag):
        if tag=="p":
            self.count -= 1
        if tag=="em":
            self.count -= 1
        if tag=="input":
            self.count -= 1
        if tag=="span":
            self.count -= 1
        if tag=="a":
            self.count -= 1
        #print("handle_endtag>" + tag + ">" + ">" + str(self.count))

    def handle_data(self, data):
        #print(str(data).strip() + ">" + str(self.count))
        #print("aaa:"+self.company)
        if self.company!="":
            self.info['company'] = self.company
            self.company = ""
        if self.count == 15:
            self.info = {}
            #print("职位：" + str(data).strip()+">"+str(self.count) )
            self.info['position']=str(data).strip()
            self.flag = True
        if self.placeflag == True and self.flag == True and self.count == 13 and str(data).strip()!="" :
            #print("上班地点："+str(data).strip()+">"+str(self.count))
            self.info['place'] = str(data).strip()
            self.placeflag = False
        if self.salaryflag == True and self.flag == True  and self.count == 13 and str(data).strip()!="" :
            #print("薪资："+str(data).strip()+">"+str(self.count))
            self.info['salary'] = str(data).strip()
            self.salaryflag = False
        if self.dateflag == True and self.flag == True  and self.count == 13 and str(data).strip()!="" :
            #print("发布日期："+str(data).strip()+">"+str(self.count))
            self.info['date'] = str(data).strip()
            self.infos.append(self.info)
            self.dateflag = False


def htmlparser(url):
    headers = {}
    req = requests.get(url)
    req.encoding = 'gbk'
    s = req.text
    myparser = Myparser()
    myparser.feed(s)
    myparser.close()
    return myparser.infos


def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


if __name__ == '__main__':
    #url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=Java&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
    url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=python&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
    req = requests.get(url)
    req.encoding = 'gbk'
    s = req.text
    pagenum = s.split("共")[2].split("页")[0]
    print("共"+pagenum+"页")
    for n in range(int(pagenum)):
        #url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=Java&keywordtype=2&curr_page="+str(n+1)+"&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
        url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=python&keywordtype=2&curr_page="+str(n+1)+"&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
        print("------------------第"+str(n+1)+"页---------------------")
        infos = htmlparser(url)
        for each in infos:
            print('%(position)s|%(company)s|%(place)s|%(salary)s|%(date)s' % each)
        #print(len(infos))
