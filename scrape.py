from urllib2 import urlopen
import lxml.html
import sys
import re

# define some constants
URL = 'http://www.postalhistory.com/postoffices.asp?task=display'
STATES = ['AL',     'AK',     'AS',     'AZ',     'AR',     'CA',     'CO',     'CT',     'DE',     'DC',     'FM',     'FL',     'GA',     'GU',     'HI',     'ID',     'IL',     'IN',     'IA',     'KS',     'KY',     'LA',     'ME',     'MH',     'MD',     'MA',     'MI',     'MN',     'MS',     'MO',     'MT',     'NE',     'NV',     'NH',     'NJ',     'NM',     'NY',     'NC',     'ND',     'MP',     'OH',     'OK',     'OR',     'PW',     'PA',     'PR',     'RI',     'SC',     'SD',     'TN',     'TX',     'UT',     'VT',     'VI',     'VA',     'WA',     'WV',     'WI',     'WY']                                                             
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
    for state in STATES:
        download_data(state)


