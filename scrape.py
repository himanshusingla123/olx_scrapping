import requests
import json
import os
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

for item in listings:
    try:
        title = item.find("span", {"data-aut-id": "itemTitle"}).get_text(strip=True)
        price = item.find("span", {"data-aut-id": "itemPrice"}).get_text(strip=True)
        location = item.find("span", {"data-aut-id": "item-location"}).get_text(strip=True)
        url = "https://www.olx.in" + item.find("a")["href"]

        print("Title:", title)
        print("Price:", price)
        print("Location:", location)
        print("URL:", url)
        print("-" * 50)
    except Exception as e:
        print("Error parsing item:", e)
