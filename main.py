#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os

if len(sys.argv) < 2:
    print ("Usage:", sys.argv[0], "<target file>")
    sys.exit(1)
fileName = sys.argv[1]
os.path.exists(fileName)
f = open(fileName, "rU")
#target = f.read().split('\n')
target = f.read().splitlines()
#del target[-1]
f.close()

for ID in target:
    print ("Target : " + ID + " " + str(len(ID)))
    factor = True
    tdTable = []
    ratioTable = []
    monthTable = []
    SeasonTable = []
    url2 = "https://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID=" + ID
    driver = webdriver.Firefox()
    driver.get(url2)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "row0")))
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")
    except Exception as e:
        print ("Not found target")
        driver.close()
        continue
    print soup.findAll("", {"href":"StockDetail.asp?STOCK_ID=" + ID})[1].get_text()
    #1
    for i in range(0, 6):
        for child in soup.find("tr", {"id": "row" + str(i)}).findAll("td"):
            if child.get_text == "-":
                tdTable.append("0")
            else:
                tdTable.append(child.get_text())
        monthTable.append(tdTable[0])
        ratio = float(tdTable[-3])
        ratioTable.append(ratio)
        del tdTable[:]

    s = "月營收年增率 YoY"
    if (ratioTable[0] > 5) & (ratioTable[1] > 5) & (ratioTable[2] > 5):
        print ("\n#1 (" +  str(s) + ") Pass")
    else:
        print ("\n#1 (" + str(s) + ") Fail")
        factor = False
    print (monthTable[0] + " : " + str(ratioTable[0]))
    print (monthTable[1] + " : " + str(ratioTable[1]))
    print (monthTable[2] + " : " + str(ratioTable[2]))

    #2
    if factor:
        ratioAvg = float(sum(ratioTable))/ len(ratioTable)
        if (min(ratioTable[0], ratioAvg) > 5):
            print ("\n#2 Pass")
        else:
            print ("\n#2 Fail")
            factor = False
        print ("ratio 1 : " + str(ratioTable[0]))
        print ("前六個月營收年增率平均 : " + str(ratioAvg))

    #3
    if factor:
        url2 = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=" + ID
        driver.get(url2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtFinBody")))
        select = Select(driver.find_element_by_id("RPT_CAT"))
        select.select_by_value("XX_M_QUAR")
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")

        tdTable = []
        ratioTable = []
        s = "每股稅後盈餘 (元)稅後淨利 / 發行股數"
#       new_name = soup.find("tr", {"id": "row6"}).findAll("td")[0].get_text()
#       original_unicode_form = new_name.encode('utf-8')
#       print original_unicode_form
        for i in range(0, 10):
            new_name = soup.find("tr", {"id": "row" + str(i)}).findAll("td")[0].get_text()
            original_unicode_form = new_name.encode('utf-8')
            if s == original_unicode_form:
                break
        eps = float(soup.find("tr", {"id": "row" + str(i)}).findAll("td")[1].get_text())
        if eps > 0:
            print ("\n#3 (EPS) Pass")
        else:
            print ("\n#3 (EPS) Fail")
            factor = False
        print ("EPS : " + str(eps) + "\n")

    #4
    plt.figure(1)
    plt.title("Comparison Diagram")
    plt.xlabel("Season(N-3 to N)")
    plt.ylabel("Season Average Growth Rate(%)")

    if factor:
        s = "獲利能力"
        for child in soup.find("div", {"id": "divFinDetail"}).findAll("td"):
            original_unicode_form = child.get_text().encode('utf-8')
            if s == original_unicode_form:
                for i in range(0, 10):
                    child = child.find_next("td")
                    SeasonTable.append(child.get_text().encode('utf-8'))
                break
    
        s = "稅後淨利率合併稅後淨利 / 營業收入 x 100%"
        for i in range(0, 10):
            new_name = soup.find("tr", {"id": "row" + str(i)}).findAll("td")[0].get_text()
            original_unicode_form = new_name.encode('utf-8')
            if s == original_unicode_form:
                break

        for child in soup.find("tr", {"id": "row" + str(i)}).findAll("td"):
            if child.get_text == "-":
                tdTable.append("0")
            else:
                tdTable.append(child.get_text())
        del tdTable[0]
        i = 0
        for ratio in tdTable:
            if ratio == "-":
                ratio = 0
                ratioTable.append(ratio)
            else:
                ratioTable.append(float(ratio))
            print (SeasonTable[i] + " 稅後淨利率 : " + str(ratioTable[-1]))
            i += 1

        plotx = [1, 2, 3, 4]
        ploty = []
        for i in range(6, 2, -1):
            avgRatio = float(sum(ratioTable[i-3:i+1]))/4
            ploty.append(avgRatio)
        growthRate = ploty[3] - ploty[0]
        if growthRate > 0:
            print ("\n#4 Pass")
        else:
            print ("\n#4 Fail")
            factor = False
        print ("Growth Rate Avg(4th) - Growth Rate Avg(1st)) : " + str(growthRate))
        for i in range(len(ploty)):
            print ("Growth Rate Avg Per 4 season(" + str(i+1) + ") : " + str(ploty[i]))
#        if not factor:
#            break
        plt.plot(plotx, ploty, '-o', label = ID)
    print ('\n')
    driver.close()
    
plt.xticks(np.arange(1, 5))
plt.legend()
plt.savefig(fileName + ".png")

