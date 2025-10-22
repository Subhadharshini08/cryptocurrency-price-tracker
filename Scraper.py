from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time

# Initialize Chrome WebDriver
chrome_service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")

print("Launching browser...")
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get("https://coinmarketcap.com/")

# Wait until the crypto table is visible
print("Waiting for data to load...")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

# Find all table rows
table_body = driver.find_element(By.TAG_NAME, "tbody")
crypto_rows = table_body.find_elements(By.TAG_NAME, "tr")

crypto_data = []

print("Extracting Top 10 Cryptocurrency Details...\n")

for i, row in enumerate(crypto_rows[:10], start=1):
    try:
        columns = row.find_elements(By.TAG_NAME, "td")
        coin_name = columns[2].find_elements(By.TAG_NAME, "p")[0].text
        coin_symbol = columns[2].find_elements(By.TAG_NAME, "p")[1].text
        current_price = columns[3].text
        daily_change = columns[6].text
        market_value = columns[7].text
        image_src = columns[2].find_element(By.TAG_NAME, "img").get_attribute("src")

        crypto_data.append({
            "Rank": i,
            "Name": coin_name,
            "Symbol": coin_symbol,
            "Price": current_price,
            "24h Change": daily_change,
            "Market Cap": market_value,
            "Logo URL": image_src
        })

        print(f"{i}. {coin_name} ({coin_symbol}) — {current_price}")

    except Exception as e:
        print(f"Skipped one row due to error: {e}")
        continue

time.sleep(2)
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(crypto_data)

# Add timestamp to filenames for uniqueness
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"Top10_Crypto_{timestamp}.csv"
excel_file = f"Top10_Crypto_{timestamp}.xlsx"

# Save files
df.to_csv(csv_file, index=False)
df.to_excel(excel_file, index=False)

print("\n Extraction Completed Successfully!")
print(f"Data saved as: {csv_file} and {excel_file}")
print("\nPreview:")
print(df)