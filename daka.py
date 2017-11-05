# -*- coding: utf-8 -*-

import datetime
import StringIO
import requests
from bs4 import BeautifulSoup

from captcha import Captcha
from utils.getch import getch
from utils.timedinput import timed_input
from utils.loading import LoadingAnimation
from config import (
    CAPTCHA_URL, LOGIN_URL, DAKA_URL, HEADERS, INPUT_TIMEOUT, DATEDELT)


#import os
#os.system('mode con: cols=100 lines=400')


def record_username_password():
    with open("key", "w") as f:
        username = raw_input("Please enter your username: ")
        password = raw_input("Please enter your password: ")
        print ""
        f.write("username %s\n" % username)
        f.write("password %s\n" % password)
    return username, password



print "What do you want to do?"
print "1. detect daka records"
print "2. change username/password"
print "Note: you have only %s seconds to make a choice, which is 1 by default." % INPUT_TIMEOUT[1]
print ""
print "Please enter your choice (1 or 2): "

while True:
    print ""
    choice = timed_input(default="1", timeout=INPUT_TIMEOUT[0])
    if choice == "1":
        try:
            with open("key", "r") as f:
                un_line = f.readline()
                pw_line = f.readline()
                username = un_line.split()[-1]
                password = pw_line.split()[-1]
        except IOError as e:
            print "I guess it is your first time to login."
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
        print "Sorry, please Enter 1 or 2: "


def login():
    captcha = Captcha()
    while True:
        ss = requests.Session()
        rp = ss.get(LOGIN_URL, headers=HEADERS)

        soup = BeautifulSoup(rp.text, "html.parser")

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
        
        words = captcha.identify(im)
        if words:
            login_payload["txtValidateCod"] = words
            return ss, login_payload

while True:
    print ""
    la = LoadingAnimation(message="Start to detect, loading ...")
    la.start()

    ss, login_payload = login()
    rp = ss.post(LOGIN_URL, headers=HEADERS, data=login_payload)
    if rp.url == LOGIN_URL:
        la.end()
        print "\r\n"
        print "It seems like your username or password is wrong."
        username, password = record_username_password()
    else:
        la.end()
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
        (datetime.datetime.now() - datetime.timedelta(days=DATEDELT)).strftime("%Y-%m-%d"),
    "ctl00$ContentPlaceHolder_Content$txtEndDate":
        datetime.datetime.now().strftime("%Y-%m-%d"),
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
print ""
for tr in trs:
    tds = tr.find_all("td")
    line = ""
    for td in tds[1:]:
        line += "%s  " % (td.string or u"无   ")
    try:
        print line
    except UnicodeEncodeError:
        print line.encode("utf-8")
    print ""


print ""
print "Press any key to exit!\n"
getch()
