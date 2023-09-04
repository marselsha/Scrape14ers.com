# Scrape14ers.com
14ers.com has a list of 14ers (mountains over 14,000ft in elevation). It also has routes/trails to hike up those 14ers. This code scrapes both the mountains and the routes into a csv file. I wrote this to help me visualize which 14ers I have hiked and help me plan which ones to do next. 

Here's a summary of what the code does and how it works:

1. **Dependencies**:
   - The code starts by installing the `webdriver_manager` package.
   - It then imports necessary modules from the `selenium` package, which is used for web scraping.
   - The `pandas` library is imported for data manipulation and storage.
   - The `re` module is imported for regular expression operations.

2. **Web Driver Setup**:
   - The code sets up a Chrome web driver using `webdriver.Chrome()`. The binary location for Chrome is specified, which seems to be a macOS path.

3. **Data Storage**:
   - An empty DataFrame `allData_df` is initialized to store the scraped data.

4. **Function `get_data()`**:
   - This function is responsible for scraping data from a single mountain's page.
   - It first determines the number of route links on the page.
   - For each route link, it extracts various details like route name, URL, mountain name, mountain range, latitude-longitude, and other route-specific details.
   - Regular expressions are used to extract specific details from the scraped text.
   - The extracted data is stored in a dictionary, which is then converted to a pandas DataFrame.
   - The function returns a DataFrame containing the details of all routes on the current mountain's page.

5. **Main Scraping Loop**:
   - The scraper first navigates to the main page listing all the mountains.
   - It then loops through each mountain link (from 1 to 58) based on a specific XPath pattern.
   - For each mountain, it generates the URL for that mountain's routes and navigates to that URL.
   - The `get_data()` function is called to scrape the route details for the current mountain.
   - The scraped data for the current mountain is appended to the main DataFrame `allData_df`.

6. **Final Steps**:
   - After scraping all the mountains, the browser is closed using `driver.quit()`.
   - The consolidated data in `allData_df` is saved to a CSV file named '14erdata.csv' in the 'Downloads' directory.

To summarize: this code navigates to 14ers.com, goes through each mountain's page, extracts details about various routes on that mountain, and saves the consolidated data to a CSV file.
