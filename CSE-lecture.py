#
#     ____                  __________
#    / __ \_   _____  _____/ __/ / __ \_      __
#   / / / / | / / _ \/ ___/ /_/ / / / / | /| / /
#  / /_/ /| |/ /  __/ /  / __/ / /_/ /| |/ |/ /
#  \____/ |___/\___/_/  /_/ /_/\____/ |__/|__/
# 
#  The copyright indication and this authorization indication shall be
#  recorded in all copies or in important parts of the Software.
# 
#  @author 0verfl0w767
#  @link https://github.com/0verfl0w767
#  @license MIT LICENSE
#
import os
import time
import random
import json
import re

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

PROFESSOR_LIST = [
  "고기림",
  # "김용승", Not Found
  "이근정",
  "최희식",
  # "최민석", Not Found
  "이한청",
  "김성완",
  "정수목",
  "신동근",
  "신인수",
  "오성규",
  "김정숙",
  "조양현",
  # "김진호", Not Found
  # "우별림", Not Found
  # "남윤진", Not Found
  "이선순",
  "손정혜",
  "주헌식",
  "김현규",
  "조충희"
]

DRIVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./driver/"))
CHROMIUM_VER = chromedriver_autoinstaller.get_chrome_version().split(".")[0]
CHROMIUM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./driver/" + CHROMIUM_VER + "/chromedriver.exe"))

if not os.path.exists(DRIVER_PATH):
  os.makedirs(DRIVER_PATH)
  
  chromedriver_autoinstaller.install(False, DRIVER_PATH)

options = Options()
options.add_argument("--start-maximized")

DRIVER = webdriver.Chrome(service=Service(CHROMIUM_PATH), options = options)
DRIVER.get("https://everytime.kr")
time.sleep(20)

#################################################################################### - 최근 강의평 클릭
WebDriverWait(DRIVER, 10).until(
  EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, \"/lecture\")]"))
).click()
print("최근 강의평이 클릭되었습니다.")
time.sleep(random.uniform(2, 8))
####################################################################################

for PROFESSOR_NAME in PROFESSOR_LIST:
  
  #################################################################################### - 교수명 검색 입력
  SEARCH_BTN = WebDriverWait(DRIVER, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/form/input[1]"))
  )
  SEARCH_BTN.click()
  SEARCH_BTN.clear()
  SEARCH_BTN.send_keys(PROFESSOR_NAME)
  print("교수명 검색이 입력되었습니다.")
  time.sleep(random.uniform(2, 8))
  ####################################################################################

  #################################################################################### - 교수명 검색 클릭
  WebDriverWait(DRIVER, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/form/input[2]"))
  ).click()
  print("교수명 검색이 클릭되었습니다.")
  time.sleep(random.uniform(2, 8))
  ####################################################################################

  #################################################################################### - 교수명 클릭
  WebDriverWait(DRIVER, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/div/label[2]"))
  ).click()
  print("교수명이 클릭되었습니다.")
  time.sleep(random.uniform(2, 8))
  ####################################################################################
  
  #################################################################################### - 바디 스크롤
  BODY = DRIVER.find_element(By.TAG_NAME, "body")
  
  for i in range(20):
    BODY.send_keys(Keys.PAGE_DOWN)

  for i in range(20):
      BODY.send_keys(Keys.PAGE_UP)
  ####################################################################################

  API = {}

  #################################################################################### - 강의 목록 확인
  LECTURE_DIV = DRIVER.find_element(By.XPATH, "/html/body/div/div/div[2]")
  LECTURES = list(LECTURE_DIV.find_elements(By.TAG_NAME, "a"))
  print(f"{PROFESSOR_NAME} 교수님의 강의가 {len(LECTURES)}개 확인되었습니다.")
  time.sleep(random.uniform(2, 8))

  for LECTURE in LECTURES:
    LECTURE_NAME = LECTURE.find_element(By.CLASS_NAME, "name").text
    if (LECTURE.find_element(By.CLASS_NAME, "on").get_attribute("style") == "width: 0%;"):
      print(LECTURE_NAME + " 강의는 평가 정보가 없습니다.")
      
      BODY.send_keys(Keys.ARROW_DOWN)
      BODY.send_keys(Keys.ARROW_DOWN)
    
      continue
    
    print(LECTURE_NAME, end=" ")
    print(LECTURE.find_element(By.CLASS_NAME, "professor").text, end=" ")
    print(LECTURE.find_element(By.CLASS_NAME, "on").get_attribute("style"))
    
    LECTURE.click() # 강의 클릭
    time.sleep(random.uniform(2, 8))
    
    LEC_COUNT = DRIVER.find_element(By.CLASS_NAME, "count").text
    PATTERN = re.compile("\(([^)]+)")
    VALUE = PATTERN.findall(LEC_COUNT)[0]
    
    print("총 " + VALUE[:-1] + "개의 강의평가가 기록되어 있습니다.")
    
    try:
      WebDriverWait(DRIVER, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "more"))
      ).click() # 강의평 더 보기 클릭
      
      time.sleep(random.uniform(2, 8))
      
      # for i in range(20):
      #   ActionChains(DRIVER).send_keys_to_element(DRIVER.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div[2]"), Keys.PAGE_DOWN)

      # for i in range(20):
      #   ActionChains(DRIVER).send_keys_to_element(DRIVER.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div[2]"), Keys.PAGE_UP)
      
      if int(VALUE[:-1]) > 20:
        LEC_BODY = DRIVER.find_element(By.TAG_NAME, "body")
        ActionChains(DRIVER).click_and_hold(DRIVER.find_element(By.CLASS_NAME, "articles")).perform()
        
        for i in range(20):
          LEC_BODY.send_keys(Keys.PAGE_DOWN)

        for i in range(20):
          LEC_BODY.send_keys(Keys.PAGE_UP)
      
      time.sleep(random.uniform(2, 8))
    
      LECTURES_DIV = DRIVER.find_element(By.XPATH, "/html/body/div/div/div[2]/div")
      LECTURES_RE = list(LECTURES_DIV.find_elements(By.CLASS_NAME, "article"))
      API[LECTURE_NAME] = []
      
      for LECTURE_RE in LECTURES_RE:
        YEAR_SEMESTER = LECTURE_RE.find_element(By.CLASS_NAME, "semester").text.strip()
        TEXT = LECTURE_RE.find_element(By.CLASS_NAME, "text").text.replace("\n", " ")
        RESULT = "("+ YEAR_SEMESTER + ") : " + TEXT
        API[LECTURE_NAME].append(RESULT)
        print(RESULT)
        
        # LEC_BODY.send_keys(Keys.ARROW_DOWN)
        # LEC_BODY.send_keys(Keys.ARROW_DOWN)
        # LEC_BODY.send_keys(Keys.ARROW_DOWN)
        
        time.sleep(random.uniform(0, 1))
      
      DRIVER.back()
      DRIVER.back()
      
      BODY.send_keys(Keys.ARROW_DOWN)
      BODY.send_keys(Keys.ARROW_DOWN)
      
      time.sleep(random.uniform(2, 8))
    except:
      print("문제가 발생하였습니다.")
      
      DRIVER.back()
      
      BODY.send_keys(Keys.ARROW_DOWN)
      BODY.send_keys(Keys.ARROW_DOWN)
      
  ####################################################################################

  #################################################################################### - API
  with open("./data/" +PROFESSOR_NAME + ".json", "w", encoding = "utf-8") as f:
    json.dump(API, f, ensure_ascii = False, indent = 2)
  ####################################################################################
  
  DRIVER.back()