
## useful docs:
#    https://selenium-python.readthedocs.io/getting-started.html#simple-usage

#%%
# import libs
import XMLSerializer
from XMLSerializer.Config import Config
from seleniumrequests import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time 
import os
from urllib.parse import parse_qsl
import json
import pandas as pd
import requests

# create an instance of the Config class (populated with default values for the attributes/variables
configData = Config()
#configData.SaveToFile('new.xml')
# display the information in 'configData'  
try:
    configData.ReadFromFile('StravaSettings.xml')
except:
    configData.SaveToFile('StravaSettings.xml')
    print(" ")
    print(" ")    
    print("ACTION REQUIRED: A settings file has been created: 'StravaSettings.xml' - Populate this and re-run")
    quit()

print(configData.ToPrintable())

#%%
def getWebdriver():
    chrome_options = Options()

    fileDownloadPath = os.path.abspath('.')

    # this is the preference we're passing
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1, 
            "download.default_directory": fileDownloadPath}

    chrome_options.add_experimental_option("prefs", prefs)
    driver = Chrome(options=chrome_options)
    return(driver)

def webdriverGetAuthorisedTokensJSON(webdriver,stravaUsername, stravaPassword,clientID,clientSecret):
    urlApproveToken = f"http://www.strava.com/oauth/authorize?client_id={clientID}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all"
    webdriver.get(urlApproveToken)
    time.sleep(5)

    elem = webdriver.find_element_by_name("email")
    elem.clear()
    elem.send_keys(stravaUsername)

    elem = webdriver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(stravaPassword)
    elem.send_keys(Keys.RETURN)
    time.sleep(7)

    elem = webdriver.find_element_by_id("authorize")
    elem.click()

    returnedURL = webdriver.current_url
    
    x = dict(parse_qsl(returnedURL))
    code = x['code']

    # POST request for read token with full read access
    response = webdriver.request('POST',
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': clientID,
                                'client_secret': clientSecret,
                                'code': code,
                                'grant_type': 'authorization_code'
                                }
                    )

    
    #Save json response as a variable
    strava_tokens = response.json()# Save tokens to file
    return(strava_tokens)

def activitiesToDataFrame(webdriver,strava_tokens):

    #Loop through all activities
    page = 1
    access_token = strava_tokens['access_token']# Create the dataframe ready for the API call to store your activity data
    activities = pd.DataFrame(
        columns = [
                "id",
                "name",
                "start_date_local",
                "type",
                "distance",
                "moving_time",
                "elapsed_time",
                "total_elevation_gain",
                "end_latlng",
                "external_id"
        ]
    )
    while True:
        # get page of activities from Strava
        urlActivities = "https://www.strava.com/api/v3/activities"
        r = webdriver.request('GET',urlActivities + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        #r = requests.get(urlActivities + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()
        
        # if no results then exit loop
        if (not r):
            break
        
        # otherwise add new data to dataframe
        for x in range(len(r)):
            activities.loc[x + (page-1)*200,'id'] = r[x]['id']
            activities.loc[x + (page-1)*200,'name'] = r[x]['name']
            activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
            activities.loc[x + (page-1)*200,'type'] = r[x]['type']
            activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
            activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
            activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
            activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
            activities.loc[x + (page-1)*200,'end_latlng'] = r[x]['end_latlng']
            activities.loc[x + (page-1)*200,'external_id'] = r[x]['external_id']    # increment page
        page += 1# Export your activities file as a csv 
    # to the folder you're running this script in
    return(activities)


stravaUsername = configData.stravaLogin.username
stravaPassword = configData.stravaLogin.password
clientID = configData.stravaAPIConfig.clientID
clientSecret = configData.stravaAPIConfig.clientSecret
csvFilename = configData.generalParams.csvFilename

driver = getWebdriver()
strava_tokens = webdriverGetAuthorisedTokensJSON(driver,stravaUsername, stravaPassword,clientID,clientSecret)
activities = activitiesToDataFrame(driver,strava_tokens)
activities.to_csv(csvFilename)
print('All done!')


