from bs4 import BeautifulSoup
import requests
import json
import time
import random

def parse_krisha(base_url, start_page=1, end_page=None):
    properties_list = []

    current_id = 1
    current_page = start_page

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
        # "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.5", 
        "Referer": "https://www.google.com/", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0" 
    }

    while end_page is None or current_page <= end_page:
        url = f"{base_url}?page={current_page}"

        delay_seconds = random.uniform(5, 10)
        print(f"Setting a {delay_seconds:.2f} second delay.")
        time.sleep(delay_seconds)

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            property_containers = soup.find_all("div", class_="a-card__inc")
        
            print(f"Parsing page: {current_page}")

            for property_container in property_containers:
                price = property_container.find("div", class_="a-card__price").text.strip()
                bedrooms = property_container.find("a", class_="a-card__title").text.strip()[0]
                area = property_container.find("a", class_="a-card__title").text.strip().split(", ")[1]
                location = property_container.find("div", class_="a-card__subtitle").text.strip()

                property_link = property_container.find("a", class_="a-card__title").get("href")
                property_response = requests.get("https://krisha.kz" + property_link, headers=headers)

                if property_response.status_code == 200:
                    soup_property = BeautifulSoup(property_response.text, "html.parser")
                    description_tag = soup_property.find("div", class_="a-text")
                    if description_tag:
                        description = description_tag.get_text(strip=True, separator="\n")
                    else:
                        description = "No description"

                property_data = {
                    "id": current_id,
                    "price": price,
                    "bedrooms": bedrooms,
                    "area": area,
                    "location": location,
                    "description": description
                }

                properties_list.append(property_data)

                current_id += 1

            current_page += 1

        else:
            print(f"Error fetching page {current_page}")
            break;

    with open("krisha_properties.json", "w", encoding="utf-8") as json_file:
        json.dump(properties_list, json_file, ensure_ascii=False, indent=2)

        print("Data has been successfully written.")

base_url = "https://krisha.kz/prodazha/kvartiry/astana/"
parse_krisha(base_url, start_page=1, end_page=40)
