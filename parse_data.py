#!/usr/bin/python
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

def parseXML(parliment, session, vote_num):
    filename = 'data/' + str(parliment) + '_' + str(session) + '_' + str(vote_num) + '.xml'
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
    return votes

def breakdownByParty(votes):
    dict = {}
    for vote in votes:
        if vote.Party not in dict:
            dict[vote.Party] = 0
        dict[vote.Party] += 1
    print("Breakdown by Party")
    print(dict)

def breakdownByResult(votes):
    res = [0, 0]
    for vote in votes:
        if vote.IsVoteYea:
            res[0] += 1
        else:
            res[1] += 1
    print("Breakdown by Party [Yea, Nay]")
    print(res)

def main():
    votes = parseXML(41, 2, 467)
    breakdownByParty(votes)
    breakdownByResult(votes)

if __name__ == "__main__":
    main()