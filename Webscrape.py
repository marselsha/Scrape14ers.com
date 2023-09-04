pip install webdriver_manager

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome For Testing"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

allData_df = pd.DataFrame()
driver.implicitly_wait(4)  # waits up to 4 seconds

def get_data():
    num_links = len(driver.find_elements(By.XPATH, '//*[@id="routeResults"]/tbody/tr/td[3]/a'))
    allRoutes_df = pd.DataFrame()
    
    # Loop through each link by index
    for i in range(num_links):

        #scrape data to strings
        classElevationAndDistanceText = driver.find_element(By.XPATH, f'//*[@id="routeResults"]/tbody/tr[{i+2}]/td[3]/div').text
        routeNameText = driver.find_element(By.XPATH, f'//*[@id="routeResults"]/tbody/tr[{i+2}]/td[3]/a').text
        routeURL = driver.find_element(By.XPATH, f'//*[@id="routeResults"]/tbody/tr[{i+2}]/td[3]/a').get_attribute('href')
        mountainName = driver.find_element(By.XPATH, '//*[@id="breadcrumbwrap"]/ul/li[3]/a').text
        mountainRange = driver.find_element(By.XPATH, '//*[@id="sidebar"]/table/tbody/tr[2]/td/div/div[3]/span[2]').text
        try:
            latLongText = driver.find_element(By.XPATH, '//*[@id="sidebar"]/table/tbody/tr[2]/td/div/div[5]/span[2]/a').text
        except NoSuchElementException: 
            latLongText = driver.find_element(By.XPATH, '//*[@id="sidebar"]/table/tbody/tr[2]/td/div/div[4]/span[2]/a').text
        try:
            routeFlag = driver.find_element(By.XPATH, f'//*[@id="routeResults"]/tbody/tr[{i+2}]/td[2]/span').get_attribute('title')
        except NoSuchElementException:
            routeFlag = None

        # Extract values from strings, using regular expressions
        difficulty = re.search(r"Difficulty: (.+)", classElevationAndDistanceText).group(1)
        total_elevation_gain = re.search(r"Total Elevation Gain: ([\d,]+)'", classElevationAndDistanceText).group(1)
        round_trip_distance = re.search(r"Round-trip Distance: ([\d.]+) mi", classElevationAndDistanceText).group(1)

        # Convert extracted values to a dictionary
        data_dict = {
            'routeDifficulty': [difficulty],
            'routeTotalElevationGain': [total_elevation_gain],
            'routeRoundTripDistance': [round_trip_distance],
            'mountainName' : mountainName,
            'routeName' : routeNameText,
            'routeLink' : routeURL,
            'routeFlag' :routeFlag,
            'mountainLatLongText' :latLongText,
            'mountainRange' : mountainRange,
            'mountainURL' : url

        }

        # Convert dictionary to a pandas DataFrame
        df = pd.DataFrame(data_dict)
        allRoutes_df = pd.concat([allRoutes_df, df], ignore_index=True)
        
    #print (allRoutes_df)
    return allRoutes_df

# load url
driver.get('https://www.14ers.com/14ers')

# Loop through all the URLs based on the XPath pattern
for i in range(1, 59):  # 59 is exclusive, so it will loop from 1 to 58
    
    #generate URL for each Mountain
    xpath = f'//*[@id="tablePeaks"]/tbody/tr[{i}]/td[1]/a'
    element = driver.find_element(By.XPATH, xpath)
    url = element.get_attribute('href') + '?t=routes'
    
    # Now, visit the URL for each Mountain
    driver.get(url)
    
    df = get_data()
    allData_df = pd.concat([df, allData_df], ignore_index=True)
    
    #driver.back()

# Close the browser
driver.quit()

allData_df.to_csv('Downloads/14erdata.csv')
