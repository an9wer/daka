import sys
import time
import threading
import itertools

class LoadingAnimation(object):

    def __init__(self, message="loading"):
        self.done = False
        self.message = message

    def __animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write('\r%s %s' % (self.message, c))
            sys.stdout.flush()
            time.sleep(0.1)

    def end(self):
        self.done=True

    def start(self):
        th = threading.Thread(target=self.__animate)
        th.start()
