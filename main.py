import json
from httpx import Client
from dataclasses import dataclass
from selectolax.parser import HTMLParser
import csv
import os

@dataclass
class shopifyScraper:
    base_url: str

    def fetch(self, url):
        client = Client()
        response = client.get(url)
        client.close()
        return response.text

    def parser(self, html):
        tree = HTMLParser(html)
        products = tree.css('div#collection-content > div > div')
        urls = []
        for product in products:
            url = self.base_url + product.css_first('a').attributes['href']
            urls.append(url)
        return urls

    def detail_parser(self, html):
        tree = HTMLParser(html)
        item = None
        items = []
        product_json = json.loads(tree.css_first('script#product_json_ld').text())
        print(product_json)
        for i, variant in enumerate(product_json['offers']):
            try:
                title = product_json['name']
                handle = product_json['sku']
                vsku = variant['sku']
                img = product_json['image']
                price = float(variant['price'])
                description = product_json['description']
                details = tree.css('div.productdetails > div')
                for detail in details:
                    if 'Product Type' in detail.text():
                        product_type = detail.css_first('span:nth-of-type(1)').text(strip=True)
                        color = detail.css_first('span:nth-of-type(2)').text(strip=True)
                    elif 'Gender' in detail.text():
                        gender = detail.css_first('span').text(strip=True)
                product_category = 'Apparel & Accessories > Clothing'
                tags = "shirt, hoodies, sweaters, sweatshirts, t-shirts"
                size = variant['name']
                if gender == 'Children':
                    age_group = 'Kids'
                else:
                    age_group = 'Adult'
                if i == 0:
                    item = {
                        'Handle': handle, 'Title': title, 'Body (HTML)': description, 'Vendor': 'My Store',
                        'Product Category': product_category,
                        'Type': product_type, 'Tags': tags, 'Published': True, 'Option1 Name': 'color',
                        'Option1 Value': color, 'Option2 Name': 'gender',
                        'Option2 Value': gender, 'Option3 Name': 'size', 'Option3 Value': size, 'Variant SKU': vsku,
                        'Variant Grams': 200,
                        'Variant Inventory Tracker': 'shopify', 'Variant Inventory Qty': 10,
                        'Variant Inventory Policy': 'deny',
                        'Variant Fulfillment Service': 'manual', 'Variant Price': price,
                        'Variant Compare At Price': price,
                        'Variant Requires Shipping': True, 'Variant Taxable': True, 'Variant Barcode': '',
                        'Image Src': img,
                        'Image Position': 1, 'Image Alt Text': '', 'Gift Card': False, 'SEO Title': '',
                        'SEO Description': '',
                        'Google Shopping / Google Product Category': product_category,
                        'Google Shopping / Gender': gender,
                        'Google Shopping / Age Group': age_group, 'Google Shopping / MPN': '',
                        'Google Shopping / AdWords Grouping': product_type,
                        'Google Shopping / AdWords Labels': '',
                        'Google Shopping / Condition': 'New', 'Google Shopping / Custom Product': False,
                        'Google Shopping / Custom Label 0': '', 'Google Shopping / Custom Label 1': '',
                        'Google Shopping / Custom Label 2': '', 'Google Shopping / Custom Label 3': '',
                        'Google Shopping / Custom Label 4': '', 'Variant Image': '', 'Variant Weight Unit': 'g',
                        'Variant Tax Code': '', 'Cost per item': '', 'Price / International': '',
                        'Compare At Price / International': '',
                        'Status': 'active'}
                else:
                    item = {
                        'Handle': handle, 'Title': '', 'Body (HTML)': '', 'Vendor': '',
                        'Product Category': '',
                        'Type': '', 'Tags': '', 'Published': '', 'Option1 Name': '',
                        'Option1 Value': color, 'Option2 Name': '',
                        'Option2 Value': gender, 'Option3 Name': '', 'Option3 Value': size, 'Variant SKU': vsku,
                        'Variant Grams': 200,
                        'Variant Inventory Tracker': 'shopify', 'Variant Inventory Qty': 10,
                        'Variant Inventory Policy': 'deny',
                        'Variant Fulfillment Service': 'manual', 'Variant Price': price,
                        'Variant Compare At Price': price,
                        'Variant Requires Shipping': True, 'Variant Taxable': True, 'Variant Barcode': '',
                        'Image Src': '',
                        'Image Position': '', 'Image Alt Text': '', 'Gift Card': '', 'SEO Title': '',
                        'SEO Description': '',
                        'Google Shopping / Google Product Category': '',
                        'Google Shopping / Gender': '',
                        'Google Shopping / Age Group': '', 'Google Shopping / MPN': '',
                        'Google Shopping / AdWords Grouping': '',
                        'Google Shopping / AdWords Labels': '',
                        'Google Shopping / Condition': '', 'Google Shopping / Custom Product': '',
                        'Google Shopping / Custom Label 0': '', 'Google Shopping / Custom Label 1': '',
                        'Google Shopping / Custom Label 2': '', 'Google Shopping / Custom Label 3': '',
                        'Google Shopping / Custom Label 4': '', 'Variant Image': '', 'Variant Weight Unit': 'g',
                        'Variant Tax Code': '', 'Cost per item': '', 'Price / International': '',
                        'Compare At Price / International': '',
                        'Status': ''}
                items.append(item.copy())
            except Exception as e:
                print(f'Parsing is failure due to {e}')
        return items

    def to_csv(self, datas, filename):
        print(datas)
        try:
            for data in datas:
                for child in data:
                    try:
                        file_exists = os.path.isfile(filename)
                        with open(filename, 'a', newline='', encoding='utf-8') as f:
                            headers = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags',
                                       'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value',
                                       'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker',
                                       'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service',
                                       'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable',
                                       'Variant Barcode', 'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card',
                                       'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category',
                                       'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN',
                                       'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels',
                                       'Google Shopping / Condition', 'Google Shopping / Custom Product',
                                       'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1',
                                       'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3',
                                       'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit',
                                       'Variant Tax Code', 'Cost per item', 'Price / International', 'Compare At Price / International',
                                       'Status']
                            writer = csv.DictWriter(f, delimiter=',', fieldnames=headers)
                            if not file_exists:
                                writer.writeheader()
                            if child != None:
                                writer.writerow(child)
                            else:
                                pass
                    except Exception as e:
                        print(f'Writing data is failure due to {e}')
                        continue
        except Exception as e:
            print(f'Looping data is failure due to {e}')
            pass

if __name__ == '__main__':
    scraper = shopifyScraper('https://www.80stees.com')
    urls = [f'https://www.80stees.com/a/search?q=christmas&page={str(page)}' for page in range(1,3)]
    htmls = [scraper.fetch(url) for url in urls]
    detail_urls = []
    for html in htmls:
        detail_urls.extend(scraper.parser(html))
    detail_htmls = [scraper.fetch(url) for url in detail_urls]
    data = [scraper.detail_parser(html) for html in detail_htmls]
    scraper.to_csv(data, filename='result.csv')
