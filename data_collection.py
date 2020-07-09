#!/usr/bin/python
import pycurl
from io import BytesIO
import os
import xml.etree.ElementTree as ET


class Vote():
    def __init__(self):
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
    parseXML(filename)


def parseXML(filename):
    root = ET.parse(filename).getroot()
    votes = []
    for child in root:
        vote = Vote()
        vote.FirstName = child.find("PersonOfficialFirstName").text
        vote.LastName = child.find("PersonOfficialLastName").text
        vote.Party = child.find("CaucusShortName").text
        vote.Constituency = child.find("ConstituencyName").text
        vote.ProvinceTerritory = child.find("ConstituencyProvinceTerritoryName").text
        vote_res = child.find("IsVoteYea").text
        if vote_res == "true":
            vote.IsVoteYea = True
        vote_res = child.find("IsVoteNay").text
        if vote_res == "true":
            vote.IsVoteNay = True
        vote_res = child.find("IsVotePaired").text
        if vote_res == "true":
            vote.IsVotePaired = True
        vote_res = child.find("DecisionResultName").text
        if vote_res == "Agreed To":
            vote.DecisionAgreedTo = True
        votes.append(vote)


def main():
    getVote(41, 2, 300)

if __name__ == "__main__":
    main()
