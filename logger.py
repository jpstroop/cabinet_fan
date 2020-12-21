from json import dump
from json import load

class Logger():
    def __init__(self, retain_entries=100):
        self.path = './html/log.json'
        self.log = self._load()
        self.max_len = retain_entries

    def append(self, time, temp, action):
        self.log.append({'time': time.isoformat(), 'temp': temp, 'action': action})
        self._trim()
        self.dump()
        return True

    def dump(self):
        with open(self.path, 'w') as f:
            dump(self.log, f, indent=2, ensure_ascii=False)
        return True

    def _trim(self):
        while len(self.log) > self.max_len:
            self.log.pop()

    def _load(self):
        try:
            with open(self.path) as f:
                log = load(f)
        except FileNotFoundError:
            log = []
        return log
