from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH or provide the path to chromedriver

# Function to get detail links from the main search results page
def get_detail_links_from_page(url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    detail_links = []
    search_results_list = driver.find_element(By.ID, 'search-results-list')
    links = search_results_list.find_elements(By.TAG_NAME, 'a')
    for link in links:
        detail_url = link.get_attribute('href')
        detail_links.append(detail_url)
    
    return detail_links

# Function to get the next page URL
def get_next_page_url():
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'next.page-numbers')
        next_page_url = next_button.get_attribute('href')
        return next_page_url
    except:
        return None

# Function to scrape search results with pagination
def scrape_search_results(start_url):
    current_url = start_url
    all_links = []
    
    while current_url:
        detail_links = get_detail_links_from_page(current_url)
        all_links.extend(detail_links)
        
        # Get the next page URL
        current_url = get_next_page_url()
    
    return all_links

# Starting URL of the search results page
search_url = 'https://nc211.org/search/?keyword=food&location=Raleigh%20%20NC%20%20United%20States&distance=20&skip=0&top=100undefined&topic=Basic%20Needs&subtopic=Food&taxonomyCode='

# Scrape the search results
all_links = scrape_search_results(search_url)

# Write the href links to a JSON file
with open('nc211_food_hrefs.json', mode='w', encoding='utf-8') as file:
    json.dump(all_links, file, indent=4)

print(f"Data has been successfully written to nc211_food_hrefs.json")

# Close the Selenium WebDriver
driver.quit()
