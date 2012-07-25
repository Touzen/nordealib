import urllib, urllib2, cookielib

LOGIN_URL = 'https://mobil.nordea.se/banking-nordea/nordea-c1/login.html'
ACC_URL = 'https://mobil.nordea.se/banking-nordea/nordea-c1/accounts.html'

class Connection(object):
    def __init__(self, pers_id, code):
        cookie = cookielib.CookieJar()
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

        csrf = self._get_csrf()
        login_data = urllib.urlencode({'_csrf_token':csrf,
                                    'xyz':str(pers_id),
                                    'zyx':str(code)})

        response = self._opener.open(LOGIN_URL, login_data).read()

        if not 'Logga ut' in response:
            raise LoginFailed(response)

    def _get_csrf(self):
        offset = 38
        length = 43
        
        html = self._opener.open(LOGIN_URL).read()
        csrf_index = html.index('csrf') + offset

        return html[csrf_index : csrf_index + length]

class LoginFailed(Exception):
    def __init__(self, err):
        self.err = err
