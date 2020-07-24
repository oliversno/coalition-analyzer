#!/usr/bin/python
import pycurl
from io import BytesIO
import sys
import os


def getVote(parliment, session, vote_num):
    filename = 'data/' + str(parliment) + '_' + str(session) + '_' + str(vote_num) + '.xml'
    if os.path.isfile(filename): # skip read if file already exists, vote data will never change
        return True

    URL = 'https://www.ourcommons.ca/Members/en/votes/' + str(parliment) + '/' \
        + str(session) + '/' + str(vote_num) + '/xml'
    
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, URL)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    res = buffer.getvalue()
    if len(res) <= 125:
        return False

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as my_data_file:
        my_data_file.write(res.decode('iso-8859-1'))
    return True


def main():
    if len(sys.argv) != 3:
        print("Please Input Parliment# and Session#")
        return
    parliment = sys.argv[1]
    session = sys.argv[2]
    vote = 1
    while getVote(parliment, session, vote):
        vote += 1

if __name__ == "__main__":
    main()
