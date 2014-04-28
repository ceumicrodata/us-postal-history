from urllib2 import urlopen
import lxml.html
import sys
import re

# define some constants
URL = 'http://www.postalhistory.com/postoffices.asp?task=display'
PATTERN = re.compile('>([\w \.,]*?\(\d{4}.*?\))')

def return_rows(html):
    return PATTERN.findall(html)

def download_data(state='DE'):
    # loop through pages
    page = 1
    while True:
        html = urlopen(URL + '&state=%s&pagenum=%d' % (state, page)).read()
        offices = return_rows(html)
        if not offices:
            break
        else:
            for office in offices:
                print "%s, %s" % (office, state)
            page += 1

if __name__=='__main__':
    state = sys.argv[1]
    download_data(state)


