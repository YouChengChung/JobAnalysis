# 求職網站職缺
from bs4 import BeautifulSoup
import requests 
import openpyxl
import time
import datetime
#print("共有",soup.find("span",class_="js-txt").text)
start_time=time.ctime()
"""處理薪資上下界"""
def number_adjust(b):
    each_salaryb=[]
    x=""
    if "~" in b:
        for i in b[:b.find("~")]:
            if i.isdigit():
                x+=i
        each_salaryb.append(int(x))
        x=""
        for i in b[b.find("~"):]:#頂
            if i.isdigit():
                x+=i
        each_salaryb.append(int(x))
    else:
        for i in b:
            if i.isdigit():
                x+=i
        each_salaryb.append(int(x))
        each_salaryb.append(int(x))
    return each_salaryb

def salary_adjust(a):
    each_salary=[]
    if a =="待遇面議":
        each_salary.append(40000)
        each_salary.append(40000)
    elif "年薪" in a:
        each_salary = number_adjust(a)
        each_salary[0] = int(each_salary[0]/12)
        each_salary[1] = int(each_salary[1]/12)
    else:
        each_salary = number_adjust(a)
    return each_salary

"""用openpyxl寫進worksheet"""
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["職缺名稱","公司名稱","職缺地區","學歷要求","經歷要求","薪資1","薪資2"]) 
"""Crawler"""
x=1
for i in range(1,151):
    print("page",i)
    time.sleep(2)
    URL="https://www.104.com.tw/jobs/search/?ro=1&kwop=7&keyword=%E6%95%B8%E6%93%9A%E5%88%86%E6%9E%90&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page="+str(i)+"&mode=s&jobsource=tab_cs_to_job&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
    res = requests.get(URL)
    soup=BeautifulSoup(res.text,"html.parser")
    #工作區
    job_area = soup.find(id="js-job-content")
    total_jobs=job_area.find_all("div","b-block__left")
    for i in total_jobs: #每一筆資料
        print("(",x,")","-"*50,sep="")
        title = i.find("a").text #也可以用i.select("a")[1].text
        company = i.select("a")[1].text
        company = company[:company.find("\n")]
        location = i.find("ul",class_="b-list-inline b-clearfix job-list-intro b-content").find("li").text
        edu = i.find("ul",class_="b-list-inline b-clearfix job-list-intro b-content").select("li")[2].text
        req = i.find("ul",class_="b-list-inline b-clearfix job-list-intro b-content").select("li")[1].text
        
        if not req[0].isdigit():
            req=0
        elif req[1].isdigit():
            req=int(req[:2])
        else:
            req = int(req[0])

        try:
            salary = i.find("a",class_="b-tag--default").text
            if "元" not in salary:
                salary = i.find("span",class_="b-tag--default").text
        except AttributeError:
            salary = i.find("span",class_="b-tag--default").text
        salary = salary_adjust(salary)

        print("Title：",title,sep="")
        print("Company：",company)
        print("Location：",location)
        print("Edu：",edu)
        print("Qualification：",req)
        print("SalaryH",salary[0])
        print("SalaryL",salary[1])
        x+=1

        try:
            #寫進worksheet
            ws.append([title,company,location,edu,req,salary[0],salary[1]])
        except:
            pass

finish_time=time.ctime()
month = str(datetime.datetime.today().month)
day = str(datetime.datetime.today().day)
wb.save("104_"+month+day+".xlsx")
print("Finish")
print("TimeLast:",start_time,finish_time)
