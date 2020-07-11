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
            dict[vote.Party] = []
        dict[vote.Party].append(vote)
    return dict

def breakdownByResult(votes):
    res = {}
    res["Yea"] = []
    res["Nay"] = []
    for vote in votes:
        if vote.IsVoteYea:
            res["Yea"].append(vote)
        else:
            res["Nay"].append(vote)
    return res

def main():
    votes = parseXML(41, 2, 467)
    print("Breakdown by Party")
    parties = breakdownByParty(votes)
    print(len(parties))
    print("Breakdown by Result [Yea, Nay]")
    YeaNay = breakdownByResult(votes)
    print(len(YeaNay["Yea"]), len(YeaNay["Nay"]))
    print("Breakdown by Party - Yea")
    print(breakdownByParty(YeaNay["Yea"]))
    print("Breakdown by Party - Nay")
    print(breakdownByParty(YeaNay["Nay"]))
    for party in parties:
        print("Party:", party)
        print("Breakdown by Result [Yea, Nay]")
        res = breakdownByResult(parties[party])
        print(len(res["Yea"]), len(res["Nay"]))

if __name__ == "__main__":
    main()