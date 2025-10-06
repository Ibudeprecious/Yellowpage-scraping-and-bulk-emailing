import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random


def get_details(service):
    print(f"Scraping details for {service} in Georgia...")

    options = uc.ChromeOptions()
    # Manual fix for the 'AttributeError'
    options.headless = False 
    print("Setting up Chrome options...")
    options.add_argument(r"	C:\Users\Precious\AppData\Local\Google\Chrome\User Data\Default") 
    options.add_argument(r'--profile-directory=Default')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    print("Done setting up Chrome options.")

    # CRITICAL CHANGE: Force a fresh download to bypass the old, cached binary
    driver = uc.Chrome(options=options)
    
    print("✅ Driver launched.")
    data = []

    for page in range(2, 5):  
        url = f"https://www.yellowpages.com/search?search_terms={service}&geo_location_terms=Georgia&page={page}"
        print(f"Loading page {page}...")
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "business-name"))
            )
        except Exception as e:
            print("Failed to load listings:", e)
            continue

        listings_links = driver.find_elements(By.CLASS_NAME, "business-name")
        detail_urls = [link.get_attribute("href") for link in listings_links]

        print(f"Found {len(detail_urls)} listings on page {page}...")

        for detail_url in detail_urls:
            name = ""
            email = ""
            website = ""
            phone = ""

            try:
                driver.get(detail_url)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h1'))
                )
                name = driver.find_element(By.TAG_NAME, 'h1').text.strip()

                try:
                    raw_email = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'email-business'))
                    ).get_attribute('href')
                    email = raw_email.split(':')[1].strip() if raw_email and ':' in raw_email else ""
                except:
                    email = ""

                try:
                    website = driver.find_element(By.CLASS_NAME, "website-link").get_attribute("href")
                except:
                    website = ""

                try:
                    phone = driver.find_element(By.CLASS_NAME, "phone").text.strip()
                except:
                    phone = ""

                data.append({
                    "Business Name": name.title(),
                    "Service": service.title(),
                    "Website": website,
                    "Phone": phone,
                    "Email": email
                })

                time.sleep(random.uniform(2, 4)) 

            except Exception as e:
                print(f"Error scraping {detail_url}: {e}")
                data.append({
                    "Business Name": name.title() if name else "Unknown",
                    "Service": service.title(),
                    "Website": "",
                    "Phone": "",
                    "Email": ""
                })
        print(f"Done Scraping page. Saving results...")
        df = pd.DataFrame(data)
        df.to_csv(f"{service} for Page {page}_details.csv", index=False)
        print(f"Saved {len(df)} results to {service} for Page {page}_details.csv")

    driver.quit()



get_details("Marketing Agencies")