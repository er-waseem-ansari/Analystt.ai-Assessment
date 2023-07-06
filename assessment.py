import requests
from bs4 import BeautifulSoup
import pandas as pd


num_pages = 20

num_product_urls = 200

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

params = {
    'k': 'bags',
    'crid': '2M096C61O4MLT',
    'qid': '1653308124',
    'sprefix': 'ba,aps,283',
    'ref': 'sr_pg_'
}

data = []

for page in range(1, num_pages+1):
    params['ref'] = 'sr_pg_' + str(page)

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_items = soup.find_all('div', {'data-component-type': 's-search-result'})

    for item in product_items:
        product_url = item.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')
        
        if not product_url.startswith('http'):
            product_url = 'https://www.amazon.in' + product_url
        
        product_name = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        
        product_price = item.find('span', {'class': 'a-offscreen'}).text.strip()
        
        rating = item.find('span', {'class': 'a-icon-alt'}).text.split()[0]
        
        num_reviews = item.find('span', {'class': 'a-size-base'}).text.strip()

        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        description_elem = soup.find('div', {'id': 'feature-bullets'})
        description = description_elem.text.strip() if description_elem else ''
        
        asin_elem = soup.find('th', text='ASIN')
        asin = asin_elem.find_next_sibling('td').text.strip() if asin_elem else ''
        
        product_desc_elem = soup.find('div', {'id': 'productDescription'})
        product_description = product_desc_elem.text.strip() if product_desc_elem else ''
        
        manufacturer_elem = soup.find('a', {'id': 'bylineInfo'})
        manufacturer = manufacturer_elem.text.strip() if manufacturer_elem else ''

        data.append({
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': rating,
            'Number of Reviews': num_reviews,
            'Description': description,
            'ASIN': asin,
            'Product Description': product_description,
            'Manufacturer': manufacturer
        })

        if len(data) == num_product_urls:
            break

    if len(data) == num_product_urls:
        break

df = pd.DataFrame(data)

# Export the data to CSV
df.to_csv('scraped_data.csv', index=False)

print('Data scraped and exported successfully.')
