#!/usr/bin/python
import pycurl
from io import BytesIO
import os
import xml.sax


class VoteHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentData = ""
        self.FirstName = ""
        self.LastName = ""
        self.Party = ""
        self.Constituency = ""
        self.ProvinceTerritory = ""
        self.IsVoteYea = False
        self.IsVoteNay = False
        self.IsVotePaired = False
        self.DecisionAgreedTo = False

def getVote(parliment, session, vote_num):
    URL = 'https://www.ourcommons.ca/Members/en/votes/' + str(parliment) + '/' \
        + str(session) + '/' + str(vote_num) + '/xml'
    
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, URL)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    filename = 'data/' + str(parliment) + '_' + str(session) + '_' + str(vote_num) + '.xml'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as my_data_file:
        my_data_file.write(buffer.getvalue().decode('iso-8859-1'))

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = VoteHandler()
    parser.setContentHandler( Handler )
    
    parser.parse(filename)


def main():
    getVote(41, 2, 467)

if __name__ == "__main__":
    main()
