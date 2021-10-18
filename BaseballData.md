# Analyzing Baseball Data

__Bryton Petersen__
__02/19/2021__




## Elevator pitch

Baseball is the classic American pass time. Every year nearly 70 million MLB tickets are sold and hundreds of thousands of hours are spent watching live baseball games. With nearly 1,000 MLB players lined up in the rosters this year alone, getting every player's stats right can get a little hectic. Using SQL queries, I attempt to organize some of the data to make comprehensible tables that will help us better visualize salaries, batting averages, and overall win rates for some players and teams. 

## Technical Details

__Grand Question 1__  - Using SQL queries to 

Table 1 - Who pays BYU (I dont)


|    | playerID   |   salary | teamID   |   yearID | name_full                      |
|---:|:-----------|---------:|:---------|---------:|:-------------------------------|
|  0 | lindsma01  |  4000000 | CHA      |     2014 | Brigham Young University-Idaho |
|  1 | lindsma01  |  4000000 | CHA      |     2014 | Brigham Young University-Idaho |
|  2 | lindsma01  |  3600000 | BAL      |     2012 | Brigham Young University-Idaho |
|  3 | lindsma01  |  3600000 | BAL      |     2012 | Brigham Young University-Idaho |
|  4 | lindsma01  |  2800000 | COL      |     2011 | Brigham Young University-Idaho |


lindsma01 or Matt Lindstrom has been the highest payed baseball player that attended BYU Idaho. His 5 highest yearly salaries range between 4,000,000 and 2,800,000. Within this dataset there is no record of another BYU Idaho alumni making more than him playing baseball.



__Grand Question 2__ - Calculating batting averages


Part 1 - Using SQL to calculate the players with the highest recorded batting averages over all


Table 2.1 - Highest Recorded Batting Average

|    | playerID   |   yearID |   AB |   H |   BattingAverage |
|---:|:-----------|---------:|-----:|----:|-----------------:|
|  0 | snowch01   |     1874 |    1 |   1 |              100 |
|  1 | baldwki01  |     1884 |    1 |   1 |              100 |
|  2 | mccafsp01  |     1889 |    1 |   1 |              100 |
|  3 | gumbebi01  |     1893 |    1 |   1 |              100 |
|  4 | oconnfr01  |     1893 |    2 |   2 |              100 |


This feels like cheating a little bit. From this table we are able to see how those with the highest batting average aren't those with the most practice, but those with lower 'at bats'. By keeping their 'at bats' low these players have managed to keep their batting average at 100%. 


Part 2 - Use the same query as above, but only include players with more than 10 “at bats” that year


Table 2.2 - 2019 Batting Average for players with more than 10 'at bats'

|    | playerID   |   yearID |   AB |   H |   BattingAverage |
|---:|:-----------|---------:|-----:|----:|-----------------:|
|  0 | tayloty01  |     2019 |   10 |   4 |          40      |
|  1 | puellce01  |     2019 |   41 |  16 |          39.0244 |
|  2 | stevean01  |     2019 |   30 |  11 |          36.6667 |
|  3 | bonifjo01  |     2019 |   20 |   7 |          35      |
|  4 | sierrma01  |     2019 |   40 |  14 |          35      |

This looks a little better. We can see that in 2019 the player with the highest batting aberage who had more than 10 'at bats' was Tyrone Anthony - who managed to keep his batting average right at 40%. The top 5 batting averages for this year with 10 or more 'at bats' range from 35% to 40%.

Part 3 - Calculating the highest lifetime batting averages for players with more than 100 'at bats'


Table 2.3 - Lifetime Batting Average


|    | playerID   |   sum(ab) |   sum(h) |   BattingAverage |
|---:|:-----------|----------:|---------:|-----------------:|
|  0 | hazlebo01  |       134 |       54 |          40.2985 |
|  1 | daviscu01  |       105 |       40 |          38.0952 |
|  2 | fishesh01  |       254 |       95 |          37.4016 |
|  3 | woltery01  |       138 |       51 |          36.9565 |
|  4 | cobbty01   |     11436 |     4189 |          36.6299 |


In the table above we can find the players with the highest lifetime batting average with more than 100 at bats. In comparison with the 2019 table shown before, the batting averages are within the same range (between 20% and 40%)


__Grand Question 3__ - Comparing the overall win rate of two teams


Table 4 - Win to Loss Ratio for the Chicago Cubs (CHN) and the St. Louis Cardinals (SLN)


|    | teamID   |   sum(w) |   sum(l) |   Win Rate |
|---:|:---------|---------:|---------:|-----------:|
|  0 | CHN      |    10982 |    10404 |    51.3514 |
|  1 | SLN      |    10138 |     9631 |    51.2823 |


Chart 1 - Win to Loss Ratio for the Chicago Cubs (red) and the St. Louis Cardinals (green)

![](winrate_1.png)

In this chart where the Chicago Cubs are red and the St. Louis Cardinals are green we are able to compare their win to loss ratio of each team for every year over the course of their lifespan. In total, both teams have averaged around a 51% win ratio, but with the chart we are able to see how each better season is followed by a less successful season fairly regularly. The Chicago Cubs was initially one of the best teams in the league but over time greater compteition brought it's win to loss ratio lower.  

## APPENDIX A (PYTHON SCRIPT)

```python
# %%

#basic imports

import datadotworld as dw
import pandas as pd 
import altair as alt 
import numpy as np
import sqlite3

# %%

#getting the dataset

sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)

# %%

#Get a list of all the 

table = pd.read_sql_query("SELECT * FROM sqlite_master WHERE type = 'table'", con)
print(table.filter(['name']))

#%%

#Grand Question #1
#trying to get 5 highest salaries for 5 highest paid players not 5 highest salaries of highest paid player

salary = pd.read_sql_query("SELECT salaries.playerID, salaries.salary, salaries.teamID, salaries.yearID, schools.name_full FROM salaries, collegeplaying, schools WHERE (collegeplaying.playerID = salaries.playerID AND collegeplaying.schoolID = schools.schoolID AND schools.name_full = 'Brigham Young University-Idaho') GROUP BY collegeplaying.playerID ORDER BY salary DESC LIMIT 5", con)
salary_md = salary.convert_dtypes(convert_string = True).to_markdown()
print(salary_md)

# %%

#Grand Question #2 part 1

bat3d = pd.read_sql_query("SELECT playerID, yearID, ab, h, (CAST(h AS FLOAT) / CAST(ab AS FLOAT))*100 AS BattingAverage FROM batting where ab >= 1 ORDER BY BattingAverage DESC LIMIT 5", con)
bat_1_md = bat3d.convert_dtypes(convert_string = True).to_markdown()
print(bat_1_md)


# %%

#Grand Question #2 part 2

bat_2 = pd.read_sql_query("SELECT playerID, yearID, ab, h, (CAST(h AS FLOAT) / CAST(ab AS FLOAT))*100 AS BattingAverage FROM batting WHERE ab >= 10 AND yearID = 2019 ORDER BY BattingAverage DESC LIMIT 5", con)
bat_2_md = bat_2.convert_dtypes(convert_string = True).to_markdown()
print(bat_2_md)

# %%
#Grand Question #2 part 3
bat_3 = pd.read_sql_query("SELECT playerID, sum(ab), sum(h) , (CAST(sum(h) AS FLOAT) / CAST(sum(ab) AS FLOAT))*100 AS BattingAverage FROM batting WHERE ab >= 100 GROUP BY playerID ORDER BY BattingAverage DESC LIMIT 5", con)
bat_3_md = bat_3.convert_dtypes(convert_string = True).to_markdown()
print(bat_3_md)


# %%
#Grand Question #3
team_1 = pd.read_sql_query("SELECT yearid, teamid, w, l FROM Teams WHERE teamID = 'CHN'", con)
team_1['Win Rate CHN'] = team_1['W'] / (team_1['L'] + team_1['W']) * 100
team_2 = pd.read_sql_query("SELECT yearid, teamid, w, l FROM Teams WHERE teamID = 'SLN'", con)
team_2['Win Rate SLN'] = team_2['W'] / (team_2['L'] + team_2['W']) * 100
team_1_md = team_1.convert_dtypes(convert_string = True).to_markdown()
team_2_md = team_2.convert_dtypes(convert_string = True).to_markdown()


compa = pd.read_sql_query("SELECT teamid, sum(w), sum(l) FROM Teams WHERE teamID = 'CHN' OR teamID = 'SLN' GROUP BY teamID", con)
compa['Win Rate'] = compa['sum(w)'] / (compa['sum(l)'] + compa['sum(w)']) * 100
compa_md = compa.convert_dtypes(convert_string = True).to_markdown()
print(compa_md)


#Grand Question #3 - charts
# %%
team_1Ch = alt.Chart(team_1).mark_line().encode(
    x = 'yearID',
    y = 'Win Rate CHN',
    color = alt.value('red')
)

team_2Ch = alt.Chart(team_2).mark_line().encode(
    x = 'yearID',
    y = 'Win Rate SLN',
    color = alt.value("green")

)
winrate = team_1Ch + team_2Ch

# %%

```