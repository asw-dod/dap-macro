import os
from datetime import datetime
from pytz import timezone
import time
import random
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from github import Github

def get_github_repo(access_token, org_name: str, repository_name: str):
    g = Github(access_token)
    repo = g.get_organization(org_name).get_repo(repository_name)
    return repo

def upload_github_issue(repo, title, body):
    repo.create_issue(title=title, body=body)

def delete_github_issue(repo):
    issues = repo.get_issues(state='open')
    for issue in issues:
        if "DAP 정보 수집기" in issue.title:
            issue.edit(state='closed')
            print(issue.title)


githubCall = True
access_token = os.environ['GITHUB_TOKEN']
deu_id = os.environ['DEU_ID_CHACHA']
deu_pw = os.environ['DEU_PW_CHACHA']
repository_name = os.environ['REPO_NAME'] # dap-macro
org_name = os.environ['ORG_NAME']         # asw-dod


options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu") 
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--disable-dev-shm-usage')

# chrome driver
driver = webdriver.Chrome('chromedriver', chrome_options=options)

print(driver.current_window_handle)
own_window_handle = driver.current_window_handle

seoul_timezone = timezone('Asia/Seoul')
today = datetime.now(seoul_timezone)
today_data = today.strftime("%Y년 %m월 %d일 %H시 %M분 : %S초")

# DAP 로그인
# 프록시 서버를 이용하거나 VPN을 이용하면 막히기 때문에 학교 망을 이용하거나, 개인 컴퓨터를 활용 해야함.
driver.get("https://dap.deu.ac.kr/sso/login.aspx")
driver.find_element_by_xpath('//*[@id="txt_id"]').send_keys(deu_id)
driver.find_element_by_xpath('//*[@id="txt_password"]').send_keys(deu_pw)
driver.find_element_by_xpath('//*[@id="BtnLogIn"]').click()
time.sleep(3)

driver.switch_to.window(own_window_handle)

titleTitle = ["비교과", "학사공지", "취업공지", "교외행사", "취업교과목", "인턴십", "장학공지", "기숙사공지", "비교과공지", "개인정보활용공지"]
text = []
totalText = {}
nyanya = 0

driver.find_element_by_xpath('//*[@id="Mcont02"]/div[4]/div[1]/ul/li[1]/a[2]').click();
time.sleep(3)

text_row = []
table_row = driver.find_elements_by_xpath('//*[@id="CP1_grdView"]/tbody/tr')
for idx, data in enumerate(table_row):
    programCount = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[1]').get_attribute('innerText')
    title = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[2]').get_attribute('innerText')
    depart = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[3]').get_attribute('innerText')
    receptionTime = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[4]').get_attribute('innerText')
    playTime = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[5]').get_attribute('innerText')
    
    text_row.append({"sessionCount": programCount, 
                     "title": title, 
                     "department": depart, 
                     "receptionTime": receptionTime, 
                     "playTime": playTime})
    
totalText[titleTitle[nyanya]] = {"notice": text_row}
nyanya += 1

driver.find_element_by_xpath('//*[@id="topmenu"]/ul/li[1]/a').click()
time.sleep(5)


for i in range(0, 6):
    t = '//*[@id="content"]/div[3]/div/ul/li[' + str(i + 1) + ']'
    print(t)
    driver.find_element_by_xpath(t).click()
    time.sleep(4)
    
    row_xpath = ""
    if i == 4:
        row_xpath = '//*[@id="CP1_divDefault"]/table/tbody/tr' 
    else:
        row_xpath = '//*[@id="CP1_pnl1"]/div/table/tbody/tr'
        
    text_row = []
    table_row = driver.find_elements_by_xpath(row_xpath)
    for idx, data in enumerate(table_row):
        num1 = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[1]').get_attribute('innerText')
        if num1 == "공지":
            continue
        
        title = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[2]/a').get_attribute('innerText')
        department = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[3]').get_attribute('innerText')
        date = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[4]').get_attribute('innerText')
        text_row.append({"title": title, "date": date, "department": department})
        
    totalText[titleTitle[nyanya]] = {"notice": text_row}
    nyanya += 1
    if i == 1: 
        for loop in range(0, 3): 
            tbody = driver.find_elements_by_xpath('//*[@id="CP1_grdView' + str(loop + 1) + '"]/tbody/tr')
            text_row = []
            
            for idx, data in enumerate(tbody):
                title = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[1]/input').get_attribute('value')
                date = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[2]').get_attribute('innerText')
                date = date.replace("-", ".", 2)
                text_row.append([title, date])
            
            totalText[titleTitle[nyanya]] = {"notice": text_row}
            nyanya += 1
        
        # tbody = driver.find_elements_by_xpath('//*[@id="CP1_grdView2"]/tbody/tr')
        # text.append(tbody.get_attribute('innerHTML'))
        
        # tbody = driver.find_elements_by_xpath('//*[@id="CP1_grdView3"]/tbody/tr')
        # text.append(tbody.get_attribute('innerHTML'))
    

import json

result = json.dumps(totalText, ensure_ascii=False)

seoul_timezone = timezone('Asia/Seoul')
today = datetime.now(seoul_timezone)
today_data = today.strftime("%Y년 %m월 %d일 %H시 %M분 : %S초")

if githubCall:
    repo = get_github_repo(access_token, org_name, repository_name)
    delete_github_issue(repo)
        
    title = f"DAP 정보 수집기 : ({today_data})"
    body = result
    upload_github_issue(repo, title, body)
