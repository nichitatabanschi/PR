import requests
from bs4 import BeautifulSoup


# Step 2: Make an HTTP GET request to the website
def fetch_car_listings():
    url = 'https://999.md/ru/list/transport/cars'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("Successfully fetched the webpage!")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {str(e)}")
        return None


# Step 3: Extract the name, price, and product link
def extract_car_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all('li', class_='ads-list-photo-item', attrs={'data-index': True})
    product_data = []

    print(f"Found {len(products)} products.")

    for product in products:
        try:
            # Extract car name
            name_tag = product.find('a', class_='js-item-ad')
            name = name_tag.text.strip() if name_tag else 'No Name Available'

            # Extract car price
            price_tag = product.find('div', class_='ads-list-photo-item-price')
            price = price_tag.text.strip() if price_tag else 'Price Not Listed'

            # Extract product link
            link = 'https://999.md' + name_tag['href'] if name_tag and name_tag.has_attr(
                'href') else 'No Link Available'

            product_data.append({'name': name, 'price': price, 'link': link})
        except Exception as e:
            print(f"An error occurred while extracting product information: {str(e)}")

    return product_data


# Step 4: Scrape additional data from the product link, including features
def scrape_additional_data(product_data):
    for product in product_data:
        try:
            if product['link'] != 'No Link Available':
                print(f"Scraping additional data for: {product['name']}")
                product_page = requests.get(product['link'])

                if product_page.status_code == 200:
                    product_soup = BeautifulSoup(product_page.text, 'html.parser')

                    # Extract description if available
                    description_tag = product_soup.find('div', class_='ads-text')
                    description = description_tag.text.strip() if description_tag else 'No description available'
                    product['description'] = description

                    # Extract features
                    features = {}
                    keys = product_soup.find_all('span', class_='adPage__content__features__key')
                    values = product_soup.find_all('span', class_='adPage__content__features__value')

                    for key, value in zip(keys, values):
                        features[key.text.strip()] = value.text.strip()

                    # Additionally, extract properties
                    property_items = product_soup.find_all('li', class_='m-value')
                    for item in property_items:
                        key_tag = item.find('span', class_='adPage__content__features__key')
                        value_tag = item.find('span', class_='adPage__content__features__value')
                        if key_tag and value_tag:
                            features[key_tag.text.strip()] = value_tag.text.strip()

                    product['features'] = features
                else:
                    print(f"Failed to fetch product page: {product['link']} (Status Code: {product_page.status_code})")
                    product['description'] = 'Error fetching description'
                    product['features'] = {}
            else:
                product['description'] = 'No description available'
                product['features'] = {}

        except Exception as e:
            print(f"An error occurred while scraping {product['link']}: {str(e)}")
            product['description'] = 'Error fetching description'
            product['features'] = {}

    return product_data


# Step 5: Add two validations to the data
def validate_product(product):
    if not product['name']:
        product['name'] = 'Unnamed Product'

    if ' ' in product['price']:
        price = product['price'].split(' ')[0].replace(',', '').replace('€', '').strip()
        product['price'] = float(price) if price.isdigit() else 0.0
    else:
        product['price'] = 0.0


# Main function to execute the tasks
def main():
    html_content = fetch_car_listings()
    if html_content is None:
        return

    product_data = extract_car_data(html_content)
    product_data = scrape_additional_data(product_data)

    for product in product_data:
        validate_product(product)

    # Output the results
    for product in product_data:
        print(
            f"Name: {product['name']}, Price: {product['price']}, Description: {product['description']}, Link: {product['link']}")
        print(f"Features: {product['features']}")


if __name__ == "__main__":
    main()
