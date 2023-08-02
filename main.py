from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os
import json
import datetime

class Control():
    def __init__(self, url):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla / 5.0 (Linux; Android  6.0)'})
        self.url = url

    def web_connect(self):
        self.r = self.session.get(self.url)
        soup = BeautifulSoup(self.r.text, features="lxml")
        return soup

    def web_status(self, soup):
        domain = urlparse(self.url).netloc
        print(domain)  # --> www.example.test

        match domain:
            case 'www.ebuyer.com':
                # Finance Available <div class="marketing-message finance_marketing_message top_left"></div>
                print(self.url)
                title = soup.find('h1', {'class': 'product-hero__title'}).text
                finbanner = soup.find('div', {'class': 'finance_marketing_message'})
                coming = soup.find('div', {'class': 'pre-order-coming-soon'})  # variant 1 - 'coming soon'
                print(title)
                if coming:
                    print('Coming soon!')
                else:
                    button = soup.find('input', {'class': 'button--add-to-basket'})
                    expected = soup.find('p', {'class': 'deliv-expected-date'})  # variant 2 - 'due on'
                    if expected:
                        print(expected.text)
                    stock = soup.find('div', {'class': 'purchase-info'}).find('h4')
                    if stock:
                        print(stock.findNextSibling('p').text)
                    here = soup.find('p', {'class': 'price'})
                    if here:
                        # checking, if the item was discounted
                        was = soup.find('p', {'class': 'price'}).findNextSibling('span')
                        if was:
                            print("Was: " + was.text)
                            print("Saving: " + was.findNextSibling('span').text.replace('save', '').strip())
                        price = soup.find('p', {'class': 'price'})
                        print("Price: " + "£" + price.text.replace('£', '').replace('inc. vat', '').strip())
                    if finbanner:
                        print("Finance available")
                    finance = soup.find('span', {'class': 'purchase-info__finance-link js-finance-hightlight'})
                    if finance:
                        print(finance.text.replace(' learn more', ''))

            case 'www.scan.co.uk':
                print(self.url)
                title = soup.find('h1', {'itemprop': 'name'}).text
                print(title)
                expected = soup.find('div', {'class': 'priceAvailability'}).findChild('span', {'class': 'stockStatus'})
                if expected:
                    print(expected.text)
                was = soup.find('div', {'class': 'priceAvailability'}).findChild('span', {'class': 'wasPrice'})
                if was:
                    print(was.text)
                price = soup.find('div', {'class': 'priceAvailability'}).findChild('span', {'class': 'price'})
                if price:
                    price = price.text
                    print("Price: " + price)
                    self.track_price_change(title, price)
                else:
                    print("Coming soon!")

            case 'www.halfords.com':
                print(self.url)
                sku = soup.find('h1', {'class': 'product-name'}).find('span').text
                title = soup.find('h1', {'class': 'product-name'}).text.replace(sku, '').strip()
                was = soup.find('span', {'class': 'b-price__regular'})
                price = soup.find('span', {'class': 'b-price__sale'})
                saving = soup.find('span', {'class': 'b-price__label'})
                prices = {}
                if was:
                    was = was.text.strip()
                    prices['Previous'] = was
                if saving:
                    saving = saving.text.strip()
                    prices['Saving'] = saving
                if price:
                    price = price.text.strip()
                    prices['Current'] = price
                print(title)
                for price in prices:
                    print(price + ": " + prices[price])

            case 'www.renaultpartsdirect.co.uk':
                print(self.url)
                title = soup.find('h1', {'class': 'product_title'})
                if title:
                    print(title.text)
                    price = soup.find('p', {'class': 'price'}).text
                    price = price.split(' ')
                    normal = price[0]
                    print(normal)
                    if len(price) > 1:
                        discount = price[1]
                        print(discount)
                else:
                    print("Renault Parts Website down for server maintenance. Back online asap.")

            case 'www.banggood.com':
                pass  # Your code for 'www.banggood.com'

            case _:
                pass  # Default case

    def web_check(self):
        res = self.web_connect()
        val = self.web_status(res)
        if val:
            print(val)

    def track_price_change(self, product_title, current_price):
        # Check if the file already exists
        if not os.path.isfile('price_data.json'):
            # Create a new dictionary for storing data
            data = {}
        else:
            # Load the existing data
            with open('price_data.json', 'r') as f:
                data = json.load(f)

        # Convert the current price to a float
        current_price_float = float(current_price.replace('\u00a3', ''))

        # Update the data
        if product_title not in data:
            data[product_title] = []  # Create a new list if this product title doesn't exist yet
        else:
            # Compare the current price with the last recorded price
            last_price = data[product_title][-1]['price']
            last_price_float = float(last_price.replace('\u00a3', ''))
            price_difference = current_price_float - last_price_float

            # Print a message if the price has changed
            if price_difference > 0:
                print(f"The price for {product_title} has increased by \u00a3{price_difference}.")
            elif price_difference < 0:
                print(f"The price for {product_title} has decreased by \u00a3{-price_difference}.")
            else:
                print(f"The price for {product_title} hasn't changed.")

        # Add the new price data to the list
        data[product_title].append({
            'timestamp': str(datetime.datetime.now()),
            'price': current_price
        })

        # Write the data back to the file
        with open('price_data.json', 'w') as f:
            json.dump(data, f)

        print(f"Price for {product_title} recorded in the JSON file.")


if __name__ == '__main__':
    urls = [
        "https://www.scan.co.uk/products/intel-nuc-11-extreme-kit-nuc11btmi9-beast-canyon-core-i9-11900kb-ddr4-so-dimm-m2-ssd-wi-fi-6e-bt-bar",
            ]
    for url in urls:
        Control(url).web_check()

