# Mypython

Install packages

[Ubuntu]

python2:
  1. sudo apt-get install python-pip
  2. sudo pip install selenium
  3. sudo apt-get install python-bs4
  4. sudo pip install matplotlib
  5. sudo apt-get install python-tk
  6. Install Gecodriver: https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu
	  6.1 wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
    6.2 tar -xvzf geckodriver*
    6.3 chmod +x geckodriver
    6.4 mv geckodriver /usr/local/bin
  7. python main.py 1.txt

python3:
  1. sudo apt-get install python3-pip
  2. sudo pip3 install selenium
  3. sudo pip3 install -U numpy
  4. sudo pip3 install matplotlib
  5. sudo pip3 install BeautifulSoup4
  6. sudo apt-get install python3-tk
  7. python3 main3.py 1.txt

[Mac OS]

python2:
  1. sudo easy_install pip
  2. sudo python -mpip install matplotlib
  3. sudo pip install selenium
  4. sudo pip install lxml
  5. Install Geckodriver:
    5.1 Download geckodriver v0.18 from https://github.com/mozilla/geckodriver/releases
    5.2 extract geckodriver
    5.3 chmod +x geckodriver
    5.4 mv geckodriver /usr/local/bin
  6. python main.py 1.txt

Python3:
  Install python3: (https://stringpiggy.hpd.io/mac-osx-python3-dual-install/)
  1. ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  2. brew doctor
  3. brew install python3
  4. sudo python3 -mpip install matplotlib
  5. sudo pip3 install selenium
  6. sudo pip3 install lxml
  7. sudo pip3 install bs4
  8. python3 main3.py 1.txt
  
條件一: 近三個月營收年增率大於5%
條件二: 近六個月營收年增率為正
條件三: 最近一季的EPS為正
第四畫出最近幾季的稅後淨利率平均
