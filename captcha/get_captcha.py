import time
import requests

from config import SOURCE_DIR, CAPTCHA_COUNT, CAPTCHA_URL, HEADERS

for i in xrange(CAPTHCA_COUNT):
    r = requests.get(CAPTCHA_URL, headers=HEADERS)
    time.sleep(1)
    with open("%s/%d.gif" % (SOURCE_DIR, i), "wb") as f:
        f.write(r.content)
