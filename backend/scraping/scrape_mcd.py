from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from db.save_to_db import save_outlets # <- stores in DB
from utils.geocode import geocode_and_get_hours # <- gets lat, lon, hours

    
def scrape_mcd_kl():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.mcdonalds.com.my/locate-us")

    wait = WebDriverWait(driver, 10)

    # Select "Kuala Lumpur" from the dropdown
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "states")))
    dropdown.click()

    kl_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[text()='Kuala Lumpur']")))
    kl_option.click()
    time.sleep(2)

    all_outlets = []

    while True:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "addressTop")))
        outlets = driver.find_elements(By.CLASS_NAME, "addressTop")

        for outlet in outlets:
            try:
                name = outlet.find_element(By.CLASS_NAME, "addressTitle").text
                address = outlet.find_element(By.CLASS_NAME, "addressText").text
                try:
                    waze_link = outlet.find_element(By.PARTIAL_LINK_TEXT, "Waze").get_attribute("href")
                except:
                    waze_link = None
                results = geocode_and_get_hours(name)


                all_outlets.append({
                    "name": name,
                    "address": address,
                    "waze_link": waze_link,
                    "hours": results["hours"],
                    "longitude":results["longitude"],
                    "latitude":results["latitude"]
                })
                
            except Exception as e:
                print("Error parsing outlet:", e)

        # Handle pagination
        try:
            next_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
            if "disabled" in next_btn.get_attribute("class"):#type:ignore
                break
            next_btn.click()
            time.sleep(2)
        except:
            break

    driver.quit()
    return all_outlets

if __name__ == "__main__":
    data = scrape_mcd_kl()
    print(f"Scraped {len(data)} outlets.")
    # for d in data:
    #     print(d)
    save_outlets(data)
