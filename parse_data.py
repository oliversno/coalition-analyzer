#!/usr/bin/python
import xml.etree.ElementTree as ET
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
    parties = breakdownByParty(votes)
    df_raw_counts = pd.DataFrame({}, index=["Yay", "Nay"])
    df_percentage = pd.DataFrame({}, index=["Yay", "Nay"])
    for party in parties:
        res = breakdownByResult(parties[party])
        df_raw_counts[party] = [len(res["Yea"]), len(res["Nay"])]
        total = len(res["Yea"]) + len(res["Nay"])
        df_percentage[party] = [len(res["Yea"])/total, len(res["Nay"])/total]
    print(df_raw_counts)
    chi, pval, dof, exp = chi2_contingency(df_raw_counts)
    print("Chi^2=", chi, "p=", pval, "dof=", dof)

    significance = 0.05
    print('p-value=%.6f, significance=%.2f\n' % (pval, significance))
    if pval < significance:
        print("""At %.2f level of significance, we reject the null hypotheses and accept H1."""% (significance)) 
        print("""They are not independent.""")
    else:
        print("""At %.2f level of significance, we accept the null hypotheses."""% (significance))
        print("""They are independent.""")

    # Group by Yes and No
    #print(df_percentage)
    df = df_percentage.T
    df.plot(x=0, y=1, kind="scatter")
    plt.show()

if __name__ == "__main__":
    main()