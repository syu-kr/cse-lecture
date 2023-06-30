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

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

PROFESSOR_NAME = ""

DRIVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "/driver/"))
CHROMIUM_VER = chromedriver_autoinstaller.get_chrome_version().split(".")[0]
CHROMIUM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "/driver/" + CHROMIUM_VER + "/chromedriver.exe"))

if not os.path.exists(DRIVER_PATH):
  os.makedirs(DRIVER_PATH)
  
  chromedriver_autoinstaller.install(False, DRIVER_PATH)

options = Options()
options.add_argument("--start-maximized")

DRIVER = webdriver.Chrome(executable_path = CHROMIUM_PATH, options = options)
DRIVER.get("https://everytime.kr")
time.sleep(15)

#################################################################################### - 최근 강의평 클릭
WebDriverWait(DRIVER, 10).until(
  EC.element_to_be_clickable((By.XPATH, "//*[@id=\"container\"]/div[3]/div[4]/div/h3/a"))
).click()
print("최근 강의평이 클릭되었습니다.")
time.sleep(random.uniform(2, 8))
####################################################################################

#################################################################################### - 교수명 검색 입력
SEARCH_BTN = WebDriverWait(DRIVER, 10).until(
  EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/form/input[1]"))
)
SEARCH_BTN.click()
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
####################################################################################

#################################################################################### - 강의 목록 확인
LECTURE_DIV = DRIVER.find_element(By.XPATH, "/html/body/div/div/div[2]")
LECTURES = list(LECTURE_DIV.find_elements(By.TAG_NAME, "a"))
print(f"{PROFESSOR_NAME} 교수님의 강의가 {len(LECTURES)}개 확인되었습니다.")

for LECTURE in LECTURES:
  if (LECTURE.find_element(By.CLASS_NAME, "on").get_attribute("style") == "width: 0%;"):
    print(LECTURE.find_element(By.CLASS_NAME, "name").text + " 강의는 평가 정보가 없습니다.")
    continue
  
  print(LECTURE.find_element(By.CLASS_NAME, "name").text, end=" ")
  print(LECTURE.find_element(By.CLASS_NAME, "professor").text, end=" ")
  print(LECTURE.find_element(By.CLASS_NAME, "on").get_attribute("style"))
  
  LECTURE.click() # 강의 클릭
  time.sleep(random.uniform(2, 8))
  
  WebDriverWait(DRIVER, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "more"))
  ).click() # 강의평 더 보기 클릭
  time.sleep(random.uniform(2, 8))
  
  LECTURES_DIV = DRIVER.find_element(By.XPATH, "/html/body/div/div/div[2]/div")
  LECTURES_RE = list(LECTURES_DIV.find_elements(By.CLASS_NAME, "article"))
  for LECTURE_RE in LECTURES_RE:
    print("평가: " + LECTURE_RE.find_element(By.CLASS_NAME, "text").text.replace("\n", " "))
  
  DRIVER.back()
  DRIVER.back()
  
  time.sleep(random.uniform(2, 8))
####################################################################################