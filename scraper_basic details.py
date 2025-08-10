from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # ✅ This is key
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_details(service):
    print(f"Scraping details for {service} in Georgia...")

    options = Options()
    #options.add_argument("--headless")  # Run Chrome in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Properly pass the Service object here
    service_obj = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service_obj, options=options)

    data = []
    for page in range(1, 2):  # Only page 1 for now
        url = f"https://www.yellowpages.com/search?search_terms={service}&geo_location_terms=Georgia&page={page}"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(5)  # Let JS load

        listings = driver.find_elements(By.CLASS_NAME, "info")

        print(f"Scraping {len(listings)} listings on page {page}...")
        for listing in listings:
            try:
                name = listing.find_element(By.CLASS_NAME, "business-name").text.strip()
            except:
                name = ""

            try:
                website = listing.find_element(By.CLASS_NAME, "track-visit-website").get_attribute("href")
            except:
                website = ""

            try:
                phone = listing.find_element(By.CLASS_NAME, "phones").text.strip()
            except:
                phone = ""

            data.append({
                "Business Name": name.title(),
                "Service": service.title(),
                "Website": website,
                "Phone": phone
            })

        time.sleep(3)  # Be polite

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv(f"{service}_details.csv", index=False)
    print(f"Saved {len(df)} results to {service}_details.csv")

get_details("plumber")
