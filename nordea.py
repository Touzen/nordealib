import urllib, urllib2, cookielib
from BeautifulSoup import BeautifulSoup

LOGIN_URL = 'https://mobil.nordea.se/banking-nordea/nordea-c1/login.html'
ACC_URL = 'https://mobil.nordea.se/banking-nordea/nordea-c1/accounts.html'

BALANCE_CLASS = 'bold'
ACC_BALANCE_CLASS = 'twoColumn'

class Connection(object):
    def __init__(self, pers_id, code):
        cookie = cookielib.CookieJar()
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

        soup = BeautifulSoup(self._opener.open(LOGIN_URL).read())
        csrf = soup.find(attrs={'name':'_csrf_token'}).attrMap['value']

        login_data = urllib.urlencode({'_csrf_token':csrf,
                                       'xyz':str(pers_id),
                                       'zyx':str(code)})

        response = self._opener.open(LOGIN_URL, login_data).read()

        if not 'Logga ut' in response:
            raise LoginFailed(response)

    @property
    def balance(self):
        soup = self._load(ACC_URL)

        acc_list = soup.findAll(attrs=ACC_BALANCE_CLASS)
        balance_list = soup.findAll(attrs=BALANCE_CLASS)[0::2]

        return dict({'total':balance_list[0].contents[0]}.items()
                    + {acc_list[i].contents[0].strip():
                       balance_list[i+1].contents[0]
                       for i in xrange(len(acc_list))}.items()) #Puke?

    def _load(self, url):
        html = self._opener.open(url).read()
        return BeautifulSoup(html, convertEntities="html")

class LoginFailed(Exception):
    def __init__(self, err):
        self.err = err
