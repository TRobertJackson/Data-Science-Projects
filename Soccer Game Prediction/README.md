# Who will be No. 1? <br>Predictions on the End of Season Points for Soccer Teams

## Objective
In this project, the objective is to predict the end of season points for soccer teams in La Liga, based on the team statistics, such as shots per game, interceptions per game, pass success and et al.   

La Liga is a Spanish soccer league and has been the top league in Europe for the last five years. There are 20 teams in La Liga. In one season, each team has to play with the other 19 teams twice, at home or away. Thus totally there are 380 matches in each season. If a team wins a match, it will gain 3 points while 0 point if it loses a match. If the match is a tie, each team will earn 1 point. At the end of each season, the accumulated points will determine the rank of the teams.  

As a super fan for Real Madrid, one of the top teams in La Liga, I am eager to know its final rank long before the season reaches the end. To predict the final points of the team, I need some stable indicators of the teams’ ability in both attacks and defenses. Therefore, I built a linear regression model to predict end of season points based on team statistics. 

## Data Source
The end-of-season points and team statistics for 20 teams in 7 seasons were web scrpaed from the website of whoscored.com using Selenium. 

## Data Analysis
Lasso regression with cross validation was performed to predict end-of-season points from team statistics.

## Findings
The final model has a R2 score of 0.765. The most important team stats to predict scores are: shots on target per game, tackles per game and offsides per game.
Details can be found in the Jupyter notebook. 

## Notebooks and Scripts
- [Soccer Game Prediction](https://github.com/tongwu21/Data-Science-Projects/blob/master/Soccer%20Game%20Prediction/Soccer%20Game%20Prediction_points.ipynb) - This notebook contains the code that I used to explore data and play with models. 

- [Regularization Functions Script](regularization_functions.py) - a python script that was used to perform the optimization of regularization parameters with cross validation.

- [Web Scraping Script](web_scraping.py) - a python script that contains the functions for web scraping using Selenium.

## Tools
Selenium, Statsmodels, Sklearn, Pandas, Numpy
