one file to log into strava and download all activities as CSV
another file to load it up and generate some plots - examples below

![Histogram of 7day distance by year](https://github.com/NiallHurley/StravaData/blob/master/imgs/Strava_Histogram_of_Rolling_colored_by_Year.png)
![Distance and 7-day distance](https://github.com/NiallHurley/StravaData/blob/master/imgs/Strava_Distance_and_7Day_distance.png)





# How to use:

1. Ensure webdriver file is in the path (ideally in the same folder as the code (see more below on webdriver) 
2. First execution of the code will create a 'StravaSettings.xml' file which will need to be populated with 
 * strava username & password
 * strava ClientID & ClientSecret
       * see  https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86




# Selenium setup

Your Chrome Driver version needs to match your Chrome Browser version. 

* Get you Chrome Browser version, by typing chrome://version
* Download Chrome Driver version that matches you Chrome Browser version, form this website https://chromedriver.chromium.org/downloads

﻿# Links

* https://developers.strava.com/docs/authentication/
* good for API walkthrough: https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86
* good for http POST request from API: https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde
	



