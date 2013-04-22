import re

matching_re = {
    'email': re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}', re.I),
    'hash32': re.compile(r'[^<A-F\d/]([A-F\d]{32})[^A-F\d]', re.I),
    'lulz': re.compile(r'(lulzsec|antisec)', re.I),
    'cisco_hash': re.compile(r'enable\s+secret', re.I),
    'cisco_pass': re.compile(r'enable\s+password', re.I),
    'google_api': re.compile(r'\W(AIza.{35})'),
    'honeypot': re.compile(r'<dionaea\.capture>', re.I),
    'steam':  re.compile(r'steam accounts', re.I),
    'bitcoin':  re.compile(r'bitcoin', re.I),
}

# I was hoping to not have to make a blacklist, but it looks like I
# don't really have a choice
blacklist_re = {
    'blacklist': [
        # SQL
    re.compile(
    r'(select\s+.*?from|join|declare\s+.*?\s+as\s+|update.*?set|insert.*?into)', re.I),
        re.compile(
            r'(define\(.*?\)|require_once\(.*?\))', re.I),  # PHP
        re.compile(
            r'(function.*?\(.*?\))', re.I),
        re.compile(
            r'(Configuration(\.Factory|\s*file))', re.I),
        re.compile(
            r'((border|background)-color)', re.I),  # Basic CSS (Will need to be improved)
        re.compile(
            r'(Traceback \(most recent call last\))', re.I),
        re.compile(
            r'(java\.(util|lang|io))', re.I),
        re.compile(r'(sqlserver\.jdbc)', re.I)
    ]
}

# The banlist is the list of regexes that are found in crash reports
banlist_re = {
    'banlist': [
        re.compile(r'faf\.fa\.proxies', re.I),
        re.compile(r'Technic Launcher is starting', re.I)
    ]
}
