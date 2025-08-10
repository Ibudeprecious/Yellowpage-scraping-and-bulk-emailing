from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import seleniumwire.undetected_chromedriver as uc
import undetected_chromedriver as uc_classic

# Assuming your proxy details are stored in variables from your data dump
proxy_ip = "92.114.93.42"
proxy_port = "42034"
proxy_user = "MfO2ufLac0yCtjc"
proxy_pass = "obk3AT1PkpYdPUO"
proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"

def get_details(service):
    print(f"Scraping details for {service} in Georgia...")

    # Configure selenium-wire options for the authenticated proxy
    # The 'proxy' key requires a dictionary with 'http' and 'https' entries
    seleniumwire_options = {
        'proxy': {
            'http': proxy_url,
            'https': proxy_url,
            'no_proxy': 'localhost,127.0.0.1' # Optional: bypass proxy for local traffic
        }
    }

    # Set up Chrome options as before
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    # ... other options like 'start-maximized', 'no-sandbox', etc.
    # Note: Undetected_chromedriver handles a lot of these for you, so you might not need all of them.

    # Initialize the WebDriver using selenium-wire's version of Chrome
    # You can also use undetected_chromedriver with selenium-wire.
    # Since you mentioned undetected_chromedriver wasn't working,
    # let's try a direct selenium-wire approach first.
    try:
        service_obj = Service(ChromeDriverManager().install())
        driver = uc_classic.Chrome(service=service_obj, options=options, seleniumwire_options=seleniumwire_options)
    except:
        # Fallback to a standard Selenium approach if uc fails.
        # This will require the proxy authentication to be handled by an extension or other means.
        # But for selenium-wire, the above is the correct way.
        print("undetected_chromedriver failed. Reverting to standard Selenium with a proxy extension is the next step if this doesn't work.")
        return

    data = []
    
    for page in range(2, 3):  # Only page 1 for now
        url = f"https://www.yellowpages.com/search?search_terms={service}&geo_location_terms=Georgia&page={page}"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(5)  # Let JS load

        # It's crucial to get the URLs of the business links first.
        # This prevents the StaleElementReferenceException.
        listings_links = driver.find_elements(By.CLASS_NAME, "business-name")
        detail_urls = [link.get_attribute("href") for link in listings_links]

        print(f"Scraping details for {len(detail_urls)} listings on page {page}...")

        for detail_url in detail_urls:
            name = ""
            email = ""
            website = ""
            phone = ""

            try:
                # Navigate to the detail page using the collected URL
                driver.get(detail_url)

                # Wait for the page to load by looking for the business name element
                name_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h1'))
                )
                name = name_element.text.strip()
                
                # Now, find other elements on the detail page
                try:
                    raw_email = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'email-business'))).get_attribute('href')
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
            
            except Exception as e:
                print(f"Error scraping details for {detail_url}: {e}")
                # Append a row with empty data for failed scrapes
                data.append({
                    "Business Name": name.title() if name else "Unknown",
                    "Service": service.title(),
                    "Website": "",
                    "Phone": "",
                    "Email": ""
                })

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv(f"{service}{page}_details.csv", index=False)
    print(f"Saved {len(df)} results to {service}_details.csv")

get_details("plumbers")