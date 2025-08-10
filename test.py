import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0")

try:
    driver = uc.Chrome(options=options)
    print("✅ Driver launched.")
    driver.get("https://www.yellowpages.com/")
    print("✅ Page loaded.")
    time.sleep(10)
    driver.quit()
except Exception as e:
    print("❌ Error occurred:", e)
