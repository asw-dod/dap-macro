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

def get_github_repo(access_token, repository_name):
    g = Github(access_token)
    repo = g.get_organization('asw-dod').get_repo(repository_name)
    return repo

def upload_github_issue(repo, title, body):
    repo.create_issue(title=title, body=body)

def delete_github_issue(repo):
    issues = repo.get_issues(state='open')
    for issue in issues:
        if "날짜 발열 테스트" in issue.title:
            issue.edit(state='closed')
            print(issue.title)


githubCall = False
if 'GITHUB_TOKEN' in os.environ:
    access_token = os.environ['GITHUB_TOKEN']
    deu_id = os.environ['DEU_ID_CHACHA']
    deu_pw = os.environ['DEU_PW_CHACHA']
    githubCall = True
    
repository_name = "dap-macro"

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("lang=ko_KR")
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")

# chrome driver
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

seoul_timezone = timezone('Asia/Seoul')
today = datetime.now(seoul_timezone)
today_data = today.strftime("%Y년 %m월 %d일 %H시 %M분 : %S초")


driver.get("https://dap.deu.ac.kr/sso/login.aspx")
driver.maximize_window()
driver.find_element_by_xpath('//*[@id="txt_id"]').send_keys(deu_id)
driver.find_element_by_xpath('//*[@id="txt_password"]').send_keys(deu_pw)
driver.find_element_by_xpath('//*[@id="BtnLogIn"]').click()

time.sleep(5)

driver.find_element_by_xpath('//*[@id="topmenu"]/ul/li[1]/a').click()

time.sleep(5)


titleTitle = ["학사공지", "취업공지", "교외행사", "취업교과목", "인턴십", "장학공지", "기숙사공지", "비교과공지", "개인정보활용공지"]
text = []
totalText = {}
nyanya = 0

for i in range(0, 6):
    t = '//*[@id="content"]/div[3]/div/ul/li[' + str(i + 1) + ']'
    print(t)
    driver.find_element_by_xpath(t).click()
    time.sleep(3)
    
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
        date = data.find_element_by_xpath('//tr[' + str(idx + 1) + ']//td[4]').get_attribute('innerText')
        text_row.append({"title": title, "date": date})
        
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
    repo = get_github_repo(access_token, repository_name)
    delete_github_issue(repo)
        
    title = f"DAP 정보 수집기 : ({today_data})"
    body = result
    upload_github_issue(repo, title, body)
