# -*- coding: utf-8 -*-

import StringIO
import requests
from bs4 import BeautifulSoup

from config import CAPTCHA_URL, LOGIN_URL, HEADERS
from captcha import Captcha

s = requests.Session()
r = s.get(LOGIN_URL, headers=HEADERS)

soup = BeautifulSoup(r.text, "html.parser")
viewstate = soup.find(id="__VIEWSTATE")
eventvalidation = soup.find(id="__EVENTVALIDATION")

payload = {
    "__VIEWSTATE": viewstate["value"],
    "__EVENTVALIDATION": eventvalidation["value"],
    "txtLoginName": raw_input("Enter your username: "),
    "txtPassword1": raw_input("Enter your password: "),
    "ImageButton1.x": 33,
    "ImageButton1.y": 22,
}


r = s.get(CAPTCHA_URL, headers=HEADERS)
im = StringIO.StringIO(r.content)
im.seek(0)
cp = Captcha()
payload["txtValidateCod"] = cp.identify(im)

if payload["txtValidateCod"]:
    r = s.post(LOGIN_URL, headers=HEADERS, data=payload)
    print r.text
