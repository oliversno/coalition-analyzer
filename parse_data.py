#!/usr/bin/python
import sys
import os
import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

class Vote():
    def __init__(self):
        self.FirstName = ""
        self.LastName = ""
        self.Party = ""
        self.Constituency = ""
        self.ProvinceTerritory = ""
        self.IsVoteYea = False
        self.IsVoteNay = False
        self.DecisionAgreedTo = False

def parseXML(parliment, session, vote_num):
    print("VOTE:", parliment, session, vote_num)
    filename = 'data/' + str(parliment) + '_' + str(session) + '_' + str(vote_num) + '.xml'
    if not os.path.isfile(filename): # if file does not exist
        return None
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
    if len(sys.argv) != 3:
        print("Please Input Parliment# and Session#")
        return
    parliment = sys.argv[1]
    session = sys.argv[2]
    vote = 1
    votes = parseXML(parliment, session, vote)
    finalRes = {}
    while votes is not None:
        parties = breakdownByParty(votes)
        df_raw_counts = pd.DataFrame({}, index=["Yay", "Nay"])
        percentage = {}
        for party in parties:
            res = breakdownByResult(parties[party])
            df_raw_counts[party] = [len(res["Yea"]), len(res["Nay"])]
            total = len(res["Yea"]) + len(res["Nay"])
            percentage[party] = len(res["Yea"])/total

        try:
            chi, pval, dof, exp = chi2_contingency(df_raw_counts)
        except:
            print("Consensus on Vote, can't detect coalitions")
        else:
            print("Chi^2=", chi, "p=", pval, "dof=", dof)

            significance = 0.05
            print('p-value=%.6f, significance=%.2f\n' % (pval, significance))
            if pval < significance:
                print("""At %.2f level of significance, we reject the null hypotheses and accept H1."""% (significance)) 
                print("""They are not independent.""")
                partyGroups = {}
                for party in parties:
                    if party == "Independent":
                        continue
                    percent = percentage[party]
                    if percent <= 0.2:
                        partyGroups[party] = 1
                    elif percent >= 0.8:
                        partyGroups[party] = 2
                groupLiberal = partyGroups["Liberal"]
                groupConservative = partyGroups["Conservative"]
                print("Party Groups", partyGroups)
                for party in parties:
                    if party == "Liberal" or party == "Conservative" or party == "Independent":
                        continue
                    if party not in partyGroups:
                        print(party, "is split")
                        continue
                    groupParty = partyGroups[party]
                    if party not in finalRes:
                        finalRes[party] = []
                    # 4 options, vote with liberal but not conservative
                    if groupParty == groupLiberal and not groupParty == groupConservative:
                        print(party, "is Liberal but not Conservative")
                        finalRes[party].append('L')
                    # vote with conservative but not liberal
                    elif groupParty == groupConservative and not groupParty == groupLiberal:
                        print(party, "is Conservative but not Liberal")
                        finalRes[party].append('C')
                    # vote with both
                    elif groupParty == groupLiberal and groupParty == groupConservative:
                        print(party, "is both")
                        finalRes[party].append('B')
                    # vote with neither
                    elif not groupParty == groupLiberal and not groupParty == groupConservative:
                        print(party, "is neither")
                        finalRes[party].append('N')

            else:
                print("""At %.2f level of significance, we accept the null hypotheses."""% (significance))
                print("""They are independent.""")

        finally:
            vote += 1
            votes = parseXML(parliment, session, vote)
    print(finalRes)
    for party in finalRes:
        counts = Counter(finalRes[party])
        length = len(finalRes[party])
        print(party, "Voted Liberal", (counts['L']/length)*100, "% of the time")
        print(party, "Voted Conservative", (counts['C']/length)*100, "% of the time")
        print(party, "Voted Both", (counts['B']/length)*100, "% of the time")
        print(party, "Voted Neither", (counts['N']/length)*100, "% of the time")



if __name__ == "__main__":
    main()