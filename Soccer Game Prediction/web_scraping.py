import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def Laliga_click(driver):
    '''
    this function is used to click for Laliga on the website of whoscored.com
    '''
    Laliga = driver.find_element_by_xpath('//a[@title="Spain"]')
    Laliga.click()
    time.sleep(5);

    return

def season_click(driver, season_num):
    '''
    function to select season
    '''
    season = driver.find_element_by_xpath('//*[@id="seasons"]/option[%d]' %(8-season_num))
    try:
        season.click()
    except WebDriverException:
        pass
    time.sleep(5)

    return

def Season_Point_Results(driver, season_num):
    '''
    function to collect the end-of-season points for 20 teams in Laliga
    '''
    print('season: 201%d - 201%d' %((season_num - 1), (season_num - 0)))

    #select the season
    season_click(driver, season_num)
    time.sleep(5);

    #find the end-of-season point table
    table = driver.find_element_by_css_selector("*[class^='ws-panel stat-table tournament-standings-table']")

    #initialize end-of-season point dataframe
    results = pd.DataFrame(columns = ['season','team', 'points'])

    #append each row to point dataframe
    allrows = table.find_elements_by_tag_name('tr')
    for row in allrows:
        cell = row.find_elements_by_tag_name('td')
        if len(cell) >9:
            results = results.append(pd.DataFrame([['201%d - 201%d' %((season_num - 1), (season_num - 0)), cell[1].text, cell[9].text]], columns = ['season','team', 'points']))

    return results

def Team_Statistics_click(driver):
    '''
    function to select team statistics tab on the website
    '''
    Team_Statistics = driver.find_element_by_xpath('//*[@id="sub-navigation"]/ul/li[3]/a')
    while True:
        try:
            Team_Statistics.click()
            break
        except:
            time.sleep(2);
    time.sleep(5);

    return

def Summary_in_Team_Statistics_click(driver):
    '''
    function to select the summary stats tab
    '''
    Summary = driver.find_element_by_xpath('//*[@id="stage-team-stats-options"]/li[1]/a')
    try:
        Summary.click()
    except:
        time.sleep(2);
    time.sleep(5);

    return

def Defensive_in_Team_Statistics_click(driver):
    '''
    function to select the defensive stats tab
    '''
    Defensive = driver.find_element_by_xpath('//*[@id="stage-team-stats-options"]/li[2]/a')
    try:
        Defensive.click()
    except:
        time.sleep(1);
    time.sleep(5);

    return

def Offensive_in_Team_Statistics_click(driver):
    '''
    function to select the offensive stats tab
    '''
    Offensive = driver.find_element_by_xpath('//*[@id="stage-team-stats-options"]/li[3]/a')
    while True:
        try:
            Offensive.click()
            break
        except:
            time.sleep(1);
    time.sleep(5);

    return


def Season_Team_Statistics(driver, season_num, stat_option):
    '''
    function to prepare the team stats dataframes
    '''
    #select the season
    season_click(driver, season_num)
    time.sleep(5);
    print(season_num)

    #select the team statistic tab
    Team_Statistics_click(driver)  #select Team Statistics Tab
    time.sleep(5);

    #select the summary(or defensive, or offensive) stats tab
    #find the stats table
    if stat_option == 'summary':
        columns = ['season', 'R', 'team','shots_pg', 'discipline_yellow', 'discipline_red', 'possession', 'pass_success', 'aerials_won', 'rating']
        Summary_in_Team_Statistics_click()
        time.sleep(5);
        table = driver.find_element_by_xpath('//*[@id="statistics-team-table-summary"]')

    elif stat_option == 'defensive':
        columns = ['season', 'R', 'team','shots_pg', 'tackles_pg', 'interceptions_pg', 'fouls_pg', 'offsides_pg', 'rating']
        Defensive_in_Team_Statistics_click(driver) #select defensive statistics
        time.sleep(5);
        table = driver.find_element_by_xpath('//*[@id="statistics-team-table-defensive"]')

    elif stat_option == 'offensive':
        columns = ['season', 'R', 'team','shots_pg', 'shots_ot_pg', 'dribbles_pg', 'fouled_pg', 'rating']
        Offensive_in_Team_Statistics_click(driver) #select offensive statistics
        time.sleep(5);
        table = driver.find_element_by_xpath('//*[@id="statistics-team-table-offensive"]')

    #initialize team stats dataframe
    team_statistic = pd.DataFrame(columns = columns)

    #add each row to the team stats dataframe
    allrows = table.find_elements_by_tag_name('tr')
    for row in allrows:
        cell = row.find_elements_by_tag_name('td')
        data = ['201%d - 201%d' %((season_num - 1), (season_num - 0))]
        if len(cell) != 0:
            for element in cell:
                Card = element.find_elements_by_tag_name('span')
                if len(Card) != 0:
                    for card in Card:
                        data.append(card.text)
                else:
                    data.append(element.text)
            team_statistic = team_statistic.append(pd.DataFrame([data], columns = columns))

    return team_statistic
