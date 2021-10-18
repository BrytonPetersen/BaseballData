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

salary = pd.read_sql_query("SELECT salaries.playerID, salaries.salary, salaries.teamID, salaries.yearID, schools.name_full FROM salaries, collegeplaying, schools WHERE (collegeplaying.playerID = salaries.playerID AND collegeplaying.schoolID = schools.schoolID AND schools.name_full = 'Brigham Young University-Idaho') ORDER BY salary DESC LIMIT 5", con)
salary_md = salary.convert_dtypes(convert_string = True).to_markdown()
print(salary_md)
"""salary = pd.read_sql_query("SELECT salaries.playerID, salaries.salary, salaries.teamID, salaries.yearID, schools.name_full FROM salaries, collegeplaying, schools WHERE (collegeplaying.playerID = salaries.playerID AND collegeplaying.schoolID = schools.schoolID AND schools.name_full = 'Brigham Young University-Idaho') ORDER BY salary DESC LIMIT 5", con)
SELECT salaries.playerID, salaries.salary, salaries.teamID, salaries.yearID, schools.name_full FROM salaries, collegeplaying, schools WHERE (collegeplaying.playerID = salaries.playerID AND collegeplaying.schoolID = schools.schoolID AND schools.name_full = 'Brigham Young University-Idaho') GROUP BY collegeplaying.playerID ORDER BY salary DESC LIMIT 5
salary_md = salary.convert_dtypes(convert_string = True).to_markdown()
print(salary_md)"""

# %%

#Grand Question #2 part 1

bat3d = pd.read_sql_query("SELECT playerID, yearID, ab, h, (CAST(h AS FLOAT) / CAST(ab AS FLOAT))*100 AS BattingAverage FROM batting where ab >= 1 ORDER BY BattingAverage DESC LIMIT 5", con)
bat_1_md = bat3d.convert_dtypes(convert_string = True).to_markdown()
print(bat_1_md)
\


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
