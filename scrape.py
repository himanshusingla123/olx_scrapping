import requests
import json
import os
import csv
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# take api and username from scrapebot website
username = os.getenv("SCRAPINGBOT_USERNAME")
apiKey = os.getenv("SCRAPINGBOT_APIKEY")

apiEndPoint = "http://api.scraping-bot.io/scrape/raw-html"

payload = json.dumps({
    "url": "https://www.olx.in/items/q-car-cover",
    "options": {
        "premiumProxy": False,
        "useChrome": True,
        "proxyCountry": "GB",
        "proxyState": "ny",
        "waitForNetworkRequests": True
    }
})

headers = {
    'Content-Type': "application/json"
}

response = requests.post(apiEndPoint, data=payload, auth=(username, apiKey), headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

listings = soup.find_all("li", {"data-aut-id": lambda x: x and x.startswith("itemBox")})

results = []

for item in listings:
    try:
        title = item.find("span", {"data-aut-id": "itemTitle"}).get_text(strip=True)
        price = item.find("span", {"data-aut-id": "itemPrice"}).get_text(strip=True)
        location = item.find("span", {"data-aut-id": "item-location"}).get_text(strip=True)
        url = "https://www.olx.in" + item.find("a")["href"]
        image_tag = item.find("img")
        image_url = image_tag["src"] if image_tag else None

        results.append({
            "Title": title,
            "Price": price,
            "Location": location,
            "URL": url,
            "Image URL": image_url
        })
    except Exception as e:
        print("Error parsing item:", e)

# Save results to CSV
csv_file = "olx_results.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Location", "URL", "Image URL"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Saved {len(results)} results to {csv_file}")

