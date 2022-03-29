import json
import os
from datetime import datetime
from pytz import timezone
from selenium import webdriver
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
        if "교외 활동 공지" in issue.title:
            issue.edit(state='closed')
            print(issue.title)

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

def getDeec(): 
    driver.get('https://deec.deu.ac.kr/Module/Board/Board_List.aspx?mc=23&RowNum=50&bno=4&ca1=0&ca2=0&sg=SC3&sk=&bk=&VIEW=N&PageNo=1')
    itemList = driver.find_elements_by_xpath('//*[@id="IContents_Board_Ctrl_List_div내용"]/div[2]/table/tbody/tr')
    text = []
    for idx in range(0, len(itemList)): 
        # //*[@id="IContents_Board_Ctrl_List_div내용"]/div[2]/table/tbody/tr[1]/td[1]
        ino = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[1]').get_attribute('innerText')
        title = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[2]').get_attribute('innerText')
        url = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[2]/a').get_attribute('href')
        # writer = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[3]').get_attribute('innerText')
        date = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[4]').get_attribute('innerText')
#         if ino == "공지":
#             continue
        # text_row.append({"title": title, "date": date})
        text.append({'title': title, 'date': date})
    return text
    
def getAsw():
    driver.get('https://asw.deu.ac.kr/asw/sub06_03.do')
    itemList = driver.find_elements_by_xpath('//*[@id="cms-content"]/div/table/tbody/tr')
    text = []
    for idx in range(0, len(itemList)): 
        ino = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[1]').get_attribute('innerText')
        title = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[2]').get_attribute('innerText')
        
        date = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[3]').get_attribute('innerText')
        date = date.replace("-", ".", 2)
        # text_row.append({"title": title, "date": date})
        text.append({'title': title, 'date': date})
    return text

def getDeu(boardLength: int):
    text = []    
    for idx in range(0, boardLength):
        driver.get('https://www.deu.ac.kr/www/board/3/' + str(idx + 1))
        itemList = driver.find_elements_by_xpath('//*[@id="tablelist"]/tbody/tr')
        for idx in range(0, len(itemList)): 
            ino = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/th[1]').get_attribute('innerText')
            if ino == '공지':
                continue
            title = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[1]').get_attribute('innerText')
            writer = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[2]').get_attribute('innerText')
            date = itemList[idx].find_element_by_xpath('//tr[' + str(idx + 1) + ']/td[3]').get_attribute('innerText')
            # text_row.append({"title": title, "date": date})
            text.append({'title': title, 'date': date, 'writer': writer})
    return text
# 

# ["창업교육센터", "학과공지", "학교공지"]
text = {}
text['창업교육센터'] = getDeec()
text['학과공지'] = getAsw()
text['학교공지'] = getDeu(2)

seoul_timezone = timezone('Asia/Seoul')
today = datetime.now(seoul_timezone)
today_data = today.strftime("%Y년 %m월 %d일 %H시 %M분 : %S초")

result = json.dumps(text, ensure_ascii=False)

access_token = os.environ['GITHUB_TOKEN']
repository_name = os.environ['REPO_NAME'] # dap-macro
org_name = os.environ['ORG_NAME']         # asw-dod

repo = get_github_repo(access_token, org_name, repository_name)
delete_github_issue(repo)
        
title = f"교외 활동 공지 : ({today_data})" # 리얼 짱 멋진 코딩하는 척 하는 중! 후후 난  너무 멋쪄
body = result
upload_github_issue(repo, title, body)
