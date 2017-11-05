import time

try:
    from .getch import getch
except ImportError:
    try:
        from msvcrt import getch
    except ImportError:
        getch = raw_input


class _TimedInput(object):
    def __init__(self):
        try:
            import msvcrt
        except ImportError:
            self.impl = _TimedInputUnix()
        else:
            del msvcrt
            self.impl = _TimedInputWindows()


class _TimedInputUnix(object):

    def __alarm_handler(self, signum, frame):
        raise

    def __call__(self, default=None, timeout=10):
        import signal
        signal.signal(signal.SIGALRM, self.__alarm_handler)
        signal.alarm(timeout)
        try:
            char = getch()
            signal.alarm(0)
            return char
        except Exception:
            pass
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return default


class _TimedInputWindows(object):

    def __call__(self, default=None, timeout=10):
        import msvcrt
        finishat = time.time() + timeout
        while True:
            if msvcrt.kbhit():
                return getch()
            else:
                if time.time() > finishat:
                    return default
                time.sleep(0.1)


timed_input = lambda default=None, timeout=10: _TimedInput().impl(default, timeout)
