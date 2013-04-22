from .regexes import matching_re


class Paste(object):
    def __init__(self):
        self.matches = {}

    def match(self):
        for name, regex in matching_re.iteritems():
            matched = regex.findall(self.text)
            if matched:
                self.matches[name] = matched
        return len(self.matches) != 0
