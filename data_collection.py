#!/usr/bin/python
import pycurl
from io import BytesIO

def getVote(parliment, session, vote_num):
    URL = 'https://www.ourcommons.ca/Members/en/votes/' + str(parliment) + '/' \
        + str(session) + '/' + str(vote_num) + '/xml'
    
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, URL)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    print(buffer.getvalue().decode('iso-8859-1'))

def main():
    getVote(41, 2, 467)

if __name__ == "__main__":
    main()
