This folder contains Jupyter notebooks and presentations for my first project at Metis.

## Problem Statement
The fictional organization WomenTechWomenYes (WTWY) asked helps from us to strategize for their volunteers to send out the tickets to their fundraising gala. We based our analysis based on three factors: the MTA data, the tech company map and the demographic stats.


First, we give insights into which stations and days of the week have the most foot-traffic to optimize voluteer placement for outreach. Our analysis even highlight the specific turnstiles/control areas and peak hours within the top 5 popular stations.


Furthermore, we find out the nearby large tech companies around the top stations to make suggestions on which entries/exits the volunteers should go.


Last, we combine with the census data to give further insights into to diversity of people the volunteers should expect around the popular stations.


## Data Wrangling and Analysis 
1. MTA Data  
The gala will be held on May 30th. We wish to give WTWY 2 weeks in order to implement our findings. In order to use the latest results, we used MTA data that relates to 3 weeks prior to the 2 week implementation process.  
We downloaded the turnstile traffic data files for 170429, 170506 and 170513 from the [MTA website](http://web.mta.info/developers/turnstile.html), combined them into one dataframe, and clean up the headers. We computed the entries and exits for each turnstile in all the time ranges, which allows us to figure our the popular stations and time ranges. 


2. Top Largest Tech Company Locations  
We obtained the headcount and locations for the largest tech companies in NYC from the [Tech Crunch websites](https://techcrunch.com/2017/05/21/examining-the-nyc-footprints-of-global-tech-titans/).

3. Demographic Stats  
The demographic stats around the top popular stations were obtained from the [NYC Census Fact Find website](http://maps.nyc.gov/census/).

