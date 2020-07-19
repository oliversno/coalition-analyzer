# coalition-analyzer
A tool to analyze how political parties form coalitions in the Canadian House of Commons using data provided by the House of Commons at https://www.ourcommons.ca/en/open-data

## Statistics 
To determine if political parties vote independantly I used a Chi-Squared Test for Independance.
Assumptions:
1. The sum of all cell frequencies in the table must be the same as the number of subjects in the experiment. This is valid because each MP belongs to one political party (I ignore independants) and votes exactly once either Yay or Nay (I ignore MPs who abstain from a vote).
2. The total number of subjects is at least 20.
