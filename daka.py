# -*- coding: utf-8 -*-

import time
import StringIO
import requests
from bs4 import BeautifulSoup

from config import CAPTCHA_URL, LOGIN_URL, DAKA_URL, HEADERS
from captcha import Captcha


#import os
#os.system('mode con: cols=100 lines=400')
#os.system('mode con: cols=100')

def record_username_password():
    with open("key", "w") as f:
        username = raw_input("Please enter your username: ")
        password = raw_input("Please enter your password: ")
        print ""
        f.write("username %s\n" % username)
        f.write("password %s\n" % password)
    return username, password



print "What do you want to do?"
print "1. login to get daka record"
print "2. change username/password"
print ""

choice = raw_input("Please enter your choice: ")
print ""

while True:
    if choice == "1":
        try:
            with open("key", "r") as f:
                un_line = f.readline()
                pw_line = f.readline()
                username = un_line.split()[-1]
                password = pw_line.split()[-1]
        except IOError as e:
            print "I guess it must be your first time to login."
            username, password = record_username_password()
        except Exception as e:
            print "It seems like something was broken up. Let's relogin."
            username, password = record_username_password()
        finally:
            break
    elif choice == "2":
        print "Well, Let's change your username and password."
        username, password = record_username_password()
        break
    else:
       choice = raw_input("Sorry, please Enter 1 or 2: ")


def login():
    while True:
        ss = requests.Session()
        rp = ss.get(LOGIN_URL, headers=HEADERS)

        soup = BeautifulSoup(rp.text, "html.parser")
        viewstate = soup.find(id="__VIEWSTATE")
        eventvalidation = soup.find(id="__EVENTVALIDATION")

        login_payload = {
            "__VIEWSTATE": soup.find(id="__VIEWSTATE")["value"],
            "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")["value"],
            "txtLoginName": username,
            "txtPassword1": password,
            "txtValidateCod": None,
            "ImageButton1.x": 33,
            "ImageButton1.y": 22,
        }


        rp = ss.get(CAPTCHA_URL, headers=HEADERS)
        im = StringIO.StringIO(rp.content)
        im.seek(0)
        cp = Captcha()
        if cp.identify(im):
            login_payload["txtValidateCod"] = cp.identify(im)
            return ss, login_payload

while True:
    ss, login_payload = login()
    rp = ss.post(LOGIN_URL, headers=HEADERS, data=login_payload)
    if rp.url == LOGIN_URL:
        print "It seems like you enter a wrong username or password."
        username, password = record_username_password()
    else:
        break


rp = ss.get(DAKA_URL, headers=HEADERS)

soup = BeautifulSoup(rp.text, "html.parser")

daka_payload = {
    "__EVENTTARGET": soup.find(id="__EVENTTARGET")["value"],
    "__EVENTARGUMENT": soup.find(id="__EVENTARGUMENT")["value"],
    #"__EVENTTARGET": "ctl00$ContentPlaceHolder_Content$AspNetPager1",
    #"__EVENTARGUMENT": 2,
    "__LASTFOCUS": soup.find(id="__LASTFOCUS")["value"],
    "__VIEWSTATE": soup.find(id="__VIEWSTATE")["value"],
    "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")["value"],
    "ctl00$ContentPlaceHolder_Content$txtStartDate":
        "2017-09-01",
    "ctl00$ContentPlaceHolder_Content$txtEndDate":
        "2017-11-30",
    "ctl00$ContentPlaceHolder_Content$btnSearch":
        soup.find(id="ctl00_ContentPlaceHolder_Content_btnSearch")["value"],
    "ctl00$ContentPlaceHolder_Content$ddlCenter":
        soup.find(id="ctl00_ContentPlaceHolder_Content_ddlCenter").find(
            "option", attrs={"selected": "selected"})["value"],
    "ctl00$ContentPlaceHolder_Content$ddlDepart":
        soup.find(id="ctl00_ContentPlaceHolder_Content_ddlDepart").find(
            "option", attrs={"selected": "selected"})["value"],
    "ctl00$ContentPlaceHolder_Content$ddluser":
        soup.find(id="ctl00_ContentPlaceHolder_Content_ddluser").find(
            "option", attrs={"selected": "selected"})["value"],
    "ctl00$ContentPlaceHolder_Content$ddlstatus":
        soup.find(id="ctl00_ContentPlaceHolder_Content_ddlstatus").find(
            "option", attrs={"selected": "selected"})["value"],
}

rp = ss.post(DAKA_URL, headers=HEADERS, data=daka_payload)

soup = BeautifulSoup(rp.text, "html.parser")
trs = soup.find(id="divContent").find("table").find_all("tr")
for tr in trs:
    tds = tr.find_all("td")
    line = ""
    for td in tds[1:]:
        line += "%s  " % (td.string or u"无   ")
    print line
    print ""

print ""
raw_input("Press any key to exit!\n")
