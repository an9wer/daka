import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTCHA_DIR = os.path.join(BASE_DIR, "captcha")

SOURCE_DIR = os.path.join(CAPTCHA_DIR, "source")
COMPONENT_DIR = os.path.join(CAPTCHA_DIR, "component")
LETTER_DIR = os.path.join(CAPTCHA_DIR, "letter")


CAPTCHA_COUNT = 10000
CAPTCHA_URL = "http://localhost:80/Admin/validateCode.aspx?"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
}
