# Web Scraper

This script is designed to scrape information from several specific websites and print out key details about products on those sites.

## How It Works

The script takes in a webpage URL, which it passes to Beautiful Soup to parse the HTML. It then checks the domain of the URL against a list of known domains for which it has specific scraping logic.

Depending on the domain, the script will look for certain HTML elements (such as product names, prices, stock statuses, etc.) and print out the values it finds.

Currently, the script supports the following domains:
- www.ebuyer.com (need to be tested)
- www.scan.co.uk
- www.halfords.com
- www.renaultpartsdirect.co.uk

## Requirements

- Python 3.10
- Beautiful Soup 4
- lxml
- requests

## Usage

To use the script, instantiate the scraper with the URL of the webpage you want to scrape, and then call the `web_status` method on the created object. For example:

```python
scraper = WebScraper("https://www.ebuyer.com/product")
scraper.web_status()

