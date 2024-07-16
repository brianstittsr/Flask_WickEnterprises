import requests
from bs4 import BeautifulSoup
import json

def get_detail_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    detail_links = []
    for link in soup.find_all('h3'):
        detail_url = link.find('a')['href']
        full_detail_url = 'https://books.toscrape.com/catalogue/' + detail_url.replace('../../../', '')
        detail_links.append(full_detail_url)
    
    return detail_links

def get_next_page_url(soup):
    next_button = soup.find('li', class_='next')
    if next_button:
        next_page_url = next_button.find('a')['href']
        full_next_page_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/' + next_page_url
        return full_next_page_url
    return None

def scrape_detail_page(detail_url):
    response = requests.get(detail_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting detail page information
    title = soup.find('h1').text.strip()
    price = soup.find('p', class_='price_color').text.strip()
    availability = soup.find('p', class_='instock availability').text.strip()
    description = soup.find('meta', {'name': 'description'})['content'].strip()
    upc = soup.find('th', text='UPC').find_next_sibling('td').text.strip()
    product_type = soup.find('th', text='Product Type').find_next_sibling('td').text.strip()
    price_excl_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text.strip()
    price_incl_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text.strip()
    tax = soup.find('th', text='Tax').find_next_sibling('td').text.strip()
    number_of_reviews = soup.find('th', text='Number of reviews').find_next_sibling('td').text.strip()

    details = {
        'Title': title,
        'Price': price,
        'Availability': availability,
        'Description': description,
        'UPC': upc,
        'Product Type': product_type,
        'Price (excl. tax)': price_excl_tax,
        'Price (incl. tax)': price_incl_tax,
        'Tax': tax,
        'Number of reviews': number_of_reviews
    }
    
    return details

def scrape_search_results(start_url):
    current_url = start_url
    all_details = []
    
    while current_url:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get detail links from the current page
        detail_links = get_detail_links_from_page(current_url)
        
        # Scrape details from each detail page
        for detail_url in detail_links:
            details = scrape_detail_page(detail_url)
            all_details.append(details)
        
        # Get the next page URL
        current_url = get_next_page_url(soup)
    
    return all_details

# Starting URL of the search results page
search_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

# Scrape the search results
all_details = scrape_search_results(search_url)

# Write the data to a JSON file
with open('bookstoscrape_travel.json', mode='w', encoding='utf-8') as file:
    json.dump(all_details, file, indent=4)

print(f"Data has been successfully written to bookstoscrape_travel.json")
