from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os

class bcolors:
    HEADER      = '\033[95m'
    OKBLUE      = '\033[94m'
    OKGREEN     = '\033[92m'
    WARNING     = '\033[93m'
    FAIL        = '\033[91m'
    ENDC        = '\033[0m'
    BOLD        = '\033[1m'
    UNDERLINE   = '\033[4m'

PassColor = bcolors.OKBLUE
FailColor = bcolors.FAIL

def YoYPerMonth(ID, driver):
    tdTable = []
    ratioTable = []
    monthTable = []
    url2 = "https://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID=" + ID
    driver.get(url2)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "row0")))
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")
    except Exception as e:
        print ("Not found target")
        return False
    print (bcolors.HEADER + soup.findAll("", {"href":"StockDetail.asp?STOCK_ID=" + ID})[1].get_text() + bcolors.ENDC)
#1
    for i in range(0, 6):
        for child in soup.find("tr", {"id": "row" + str(i)}).findAll("td"):
            if child.get_text == "-":
                tdTable.append("0")
            else:
                tdTable.append(child.get_text())
        if len(tdTable) <= 0:
            return False
        monthTable.append(tdTable[0])
        ratio = float(tdTable[-3])
        ratioTable.append(ratio)
        del tdTable[:]

    print (monthTable[0] + " : " + str(ratioTable[0]))
    print (monthTable[1] + " : " + str(ratioTable[1]))
    print (monthTable[2] + " : " + str(ratioTable[2]))

    s = "月營收年增率 YoY"
    if (ratioTable[0] > 5) & (ratioTable[1] > 5) & (ratioTable[2] > 5):
        print (PassColor + "\n#1 (" + str(s) + ") Pass" + bcolors.ENDC)
    else:
        print (FailColor + "\n#1 (" + str(s) + ") Fail" + bcolors.ENDC)
        return False

#2
    ratioAvg = float(sum(ratioTable)) / len(ratioTable)
    if (min(ratioTable[0], ratioAvg) > 5):
        print (PassColor + "\n#2 Pass" + bcolors.ENDC)
    else:
        print (FailColor + "\n#2 Fail 前六個月營收年增率平均 < 5%" + bcolors.ENDC)
        return False
    print ("ratio 1 : " + str(ratioTable[0]))
    print ("前六個月營收年增率平均 : " + str(ratioAvg))
    return True

def EPSandNetProfit(ID, driver, tdTable, ratioTable):
    url2 = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=" + ID
    driver.get(url2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtFinBody")))
    select = Select(driver.find_element_by_id("RPT_CAT"))
    select.select_by_value("XX_M_QUAR")
    time.sleep(5)
    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")

    s = u"每股稅後盈餘 (元)稅後淨利 / 發行股數"
    for i in range(0, 10):
        new_name = soup.find("tr", {"id": "row" + str(i)}).findAll("td")[0].get_text()
        if s == new_name:
            break
    if i >= 9:
        print (bcolors.WARNING + "Can't find 每股稅後盈餘 (元)稅後淨利 / 發行股數\n" + bcolors.ENDC)
        return False
    eps = float(soup.find("tr", {"id": "row" + str(i)}).findAll("td")[1].get_text())
    if eps > 0:
        print (PassColor + "\n#3 (EPS) Pass" + bcolors.ENDC)

    else:
        print (FailColor + "\n#3 (EPS) Fail" + bcolors.ENDC)
        return False

    SeasonTable = []

    s = u"獲利能力"
    for child in soup.find("div", {"id": "divFinDetail"}).findAll("td"):
        original_unicode_form = child.get_text()
        if s == original_unicode_form:
            for i in range(0, 10):
                child = child.find_next("td")
                SeasonTable.append(child.get_text())
            break
    
    s = u"稅後淨利率合併稅後淨利 / 營業收入 x 100%"
    for i in range(0, 10):
        new_name = soup.find("tr", {"id": "row" + str(i)}).findAll("td")[0].get_text()
        if s == new_name:
            break

    for child in soup.find("tr", {"id": "row" + str(i)}).findAll("td"):
        if child.get_text == "-":
            tdTable.append("0")
        else:
            tdTable.append(child.get_text())
    del tdTable[0]
    i = 0
    if len(SeasonTable) <= 0:
        print ("SeasonTable is empty.")
        return False
    for ratio in tdTable:
        if ratio == "-":
            ratio = 0
            ratioTable.append(ratio)
        else:
            ratioTable.append(float(ratio))
        print (str(SeasonTable[i]) + " 稅後淨利率 : " + str(ratioTable[-1]))
        i += 1

    return True


if len(sys.argv) < 2:
    print ("Usage:", sys.argv[0], "<target file>")
    sys.exit(1)
fileName = sys.argv[1]
my_file = Path(fileName)
target = []
if my_file.is_file():
    f = open(fileName, "rU")
    target = f.read().splitlines()
    f.close()
else:
    target.append(fileName)

for ID in target:
    print ("\n===============================================================")
    print ("\nTarget : " + ID)
    driver = webdriver.Firefox()

    if not YoYPerMonth(ID, driver):
        driver.close()
        continue

#3
    tdTable = []
    ratioTable = []
    if not EPSandNetProfit(ID, driver, tdTable, ratioTable):
        driver.close()
        continue
    
#4
    plt.figure(1)
    plt.title("Comparison Diagram")
    plt.xlabel("Season(N-3 to N)")
    plt.ylabel("Season Average Growth Rate(%)")
    plotx = [1, 2, 3, 4]
    ploty = []
    for i in range(6, 2, -1):
        avgRatio = float(sum(ratioTable[i - 3 : i + 1])) / 4
        ploty.append(avgRatio)
    growthRate = ploty[3] - ploty[0]
    if growthRate > 0:
        print (PassColor + "\n#4 Pass" + bcolors.ENDC)
    else:
        print (FailColor + "\n#4 Fail" + bcolors.ENDC)
    print ("Growth Rate Avg(4th) - Growth Rate Avg(1st)) : " + str(growthRate))
    for i in range(len(ploty)):
        print ("Growth Rate Avg Per 4 season(" + str(i+1) + ") : " + str(ploty[i]))
    plt.plot(plotx, ploty, '-o', label = ID)
    print ('\n')
    driver.close()
 
plt.xticks(np.arange(1, 5))
plt.legend()
plt.savefig(fileName + ".png")


